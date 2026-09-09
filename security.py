import random


def generate_otp():
    return f"{random.randint(0, 999999):06d}"


def verify_2fa_otp(correct_otp):
    """
    Terminal-based OTP verification.

    GUI should use its own graphical OTP dialog.
    """

    print(
        "\n⚠️ [SECURITY ALERT]: "
        "High-value transaction detected (> ₹50,000)!"
    )

    print(
        f"📱 [Simulated SMS Sent]: "
        f"Your One-Time Password (OTP) is: {correct_otp}"
    )

    attempts = 3

    while attempts > 0:

        user_otp = input(
            f"Enter the 6-digit OTP "
            f"({attempts} attempts remaining): "
        ).strip()

        if user_otp == str(correct_otp):
            print("✅ 2FA Verification Successful!")
            return True

        attempts -= 1
        print("❌ Invalid OTP.")

    print(
        "🔒 Transaction Blocked: "
        "Too many failed OTP attempts."
    )

    return False
