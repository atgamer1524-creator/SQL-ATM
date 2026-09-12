from datetime import datetime


def send_transaction_sms(
    mobile,
    account_num,
    tx_type,
    amount,
    current_balance
):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "\n"
        "========================================\n"
        f"[SMS SENT TO {mobile}]\n"
        f"Bank Alert - A/c {account_num}\n"
        f"Transaction: {tx_type}\n"
        f"Amount: ₹{amount:,.2f}\n"
        f"Available Balance: ₹{current_balance:,.2f}\n"
        f"Time: {now}\n"
        "========================================\n"
    )

    with open(
        "sms_logs.txt",
        "a",
        encoding="utf-8"
    ) as file:
        file.write(message)

    print(
        f"\n📱 [Simulated SMS sent successfully "
        f"to {mobile}]"
    )
