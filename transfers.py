import database
import sms_service
import security


HIGH_VALUE_LIMIT = 50000


def account_exists(account_num):
    return database.account_exists(account_num)


def execute_transfer(
    sender_acc,
    receiver_acc,
    amount,
    otp_verifier=None
):
    """
    Execute a transfer.

    otp_verifier:
        Optional callback used by the GUI.

        Example:
            otp_verifier = lambda otp: gui.ask_for_otp(otp)

        If omitted, terminal security.verify_2fa_otp()
        is used for high-value transfers.
    """

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return False, "Invalid transfer amount."

    if amount <= 0:
        return False, "Transfer amount must be greater than zero."

    if sender_acc == receiver_acc:
        return False, (
            "You cannot transfer money to your own account."
        )

    if not account_exists(receiver_acc):
        return False, (
            "Recipient account number does not exist."
        )

    # High-value transfer security
    if amount > HIGH_VALUE_LIMIT:

        otp = security.generate_otp()

        if otp_verifier is not None:
            verified = otp_verifier(otp)
        else:
            verified = security.verify_2fa_otp(otp)

        if not verified:
            return False, (
                "Transaction cancelled due to "
                "failed 2FA verification."
            )

    try:
        sender_new_balance, receiver_new_balance = (
            database.transfer_balance(
                sender_acc,
                receiver_acc,
                amount
            )
        )

    except ValueError as e:
        return False, str(e)

    except Exception as e:
        return False, (
            f"Transfer failed due to a database error: {e}"
        )

    sender_mobile = database.get_mobile(sender_acc)
    receiver_mobile = database.get_mobile(receiver_acc)

    if sender_mobile:
        sms_service.send_transaction_sms(
            sender_mobile,
            sender_acc,
            f"Transfer to A/c {receiver_acc}",
            amount,
            sender_new_balance
        )

    if receiver_mobile:
        sms_service.send_transaction_sms(
            receiver_mobile,
            receiver_acc,
            f"Transfer from A/c {sender_acc}",
            amount,
            receiver_new_balance
        )

    return True, (
        f"Successfully transferred "
        f"₹{amount:,.2f} to account {receiver_acc}."
    )
