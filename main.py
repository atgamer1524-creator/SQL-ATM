import customtkinter as ctk
from tkinter import messagebox

import database
import transfers
import security


database.initialize_db()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ModernATMGUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Modern SQL ATM System")
        self.root.geometry("500x650")
        self.root.minsize(450, 600)
        self.root.resizable(True, True)

        self.current_account = None

        self.show_login_screen()

    # =========================================================
    # UTILITY
    # =========================================================

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================================================
    # LOGIN
    # =========================================================

    def show_login_screen(self):
        self.clear_screen()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=40
        )

        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="SQL ATM PORTAL",
            font=("Arial", 26, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(40, 30),
            sticky="ew"
        )

        ctk.CTkLabel(
            frame,
            text="Account Number",
            font=("Arial", 13)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=40,
            pady=(10, 0)
        )

        self.acc_entry = ctk.CTkEntry(
            frame,
            height=40,
            placeholder_text="Enter your account number"
        )

        self.acc_entry.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=40,
            pady=(5, 15)
        )

        ctk.CTkLabel(
            frame,
            text="PIN",
            font=("Arial", 13)
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=40,
            pady=(5, 0)
        )

        self.pin_entry = ctk.CTkEntry(
            frame,
            height=40,
            show="*",
            placeholder_text="Enter 4-digit PIN"
        )

        self.pin_entry.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=40,
            pady=(5, 30)
        )

        ctk.CTkButton(
            frame,
            text="Login",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.handle_login
        ).grid(
            row=5,
            column=0,
            sticky="ew",
            padx=40,
            pady=10
        )

        ctk.CTkButton(
            frame,
            text="Create New Account",
            height=40,
            fg_color="transparent",
            border_width=2,
            command=self.show_register_screen
        ).grid(
            row=6,
            column=0,
            sticky="ew",
            padx=40,
            pady=10
        )

        self.acc_entry.focus()

    def handle_login(self):

        acc = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not acc or not pin:
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits."
            )
            return

        try:
            user_name = database.check_login(
                acc,
                pin
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return

        if user_name:
            self.current_account = acc

            messagebox.showinfo(
                "Success",
                f"Welcome back, {user_name}!"
            )

            self.show_dashboard()

        else:
            messagebox.showerror(
                "Error",
                "Invalid Account Number or PIN."
            )

    # =========================================================
    # REGISTER
    # =========================================================

    def show_register_screen(self):

        self.clear_screen()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=40
        )

        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="REGISTER ACCOUNT",
            font=("Arial", 22, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(25, 20),
            sticky="ew"
        )

        fields = [
            ("Account Number", "reg_acc", None),
            ("4-Digit PIN", "reg_pin", "*"),
            ("Full Name", "reg_name", None),
            ("10-Digit Mobile", "reg_mob", None),
            ("Initial Deposit (₹)", "reg_dep", None)
        ]

        row = 1

        for label, attribute, mask in fields:

            entry = ctk.CTkEntry(
                frame,
                height=35,
                placeholder_text=label,
                show=mask
            )

            entry.grid(
                row=row,
                column=0,
                sticky="ew",
                padx=40,
                pady=6
            )

            setattr(
                self,
                attribute,
                entry
            )

            row += 1

        ctk.CTkButton(
            frame,
            text="Submit Registration",
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.handle_registration
        ).grid(
            row=row,
            column=0,
            sticky="ew",
            padx=40,
            pady=(20, 10)
        )

        ctk.CTkButton(
            frame,
            text="Back to Login",
            height=35,
            fg_color="transparent",
            border_width=1,
            command=self.show_login_screen
        ).grid(
            row=row + 1,
            column=0,
            sticky="ew",
            padx=40,
            pady=5
        )

        self.reg_acc.focus()

    def handle_registration(self):

        acc = self.reg_acc.get().strip()
        pin = self.reg_pin.get().strip()
        name = self.reg_name.get().strip()
        mobile = self.reg_mob.get().strip()
        deposit_text = self.reg_dep.get().strip()

        if not all([
            acc,
            pin,
            name,
            mobile,
            deposit_text
        ]):
            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        if not acc.isdigit():
            messagebox.showerror(
                "Error",
                "Account number must contain only digits."
            )
            return

        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits."
            )
            return

        if len(mobile) != 10 or not mobile.isdigit():
            messagebox.showerror(
                "Error",
                "Mobile number must be exactly 10 digits."
            )
            return

        try:
            deposit = float(deposit_text)

            if deposit < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Initial deposit must be a valid number."
            )
            return

        try:
            created = database.create_account(
                acc,
                pin,
                name,
                deposit,
                mobile
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return

        if not created:
            messagebox.showerror(
                "Error",
                "Account number already exists."
            )
            return

        messagebox.showinfo(
            "Success",
            "Account created successfully!\n\n"
            "Please log in."
        )

        self.show_login_screen()

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_screen()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=40
        )

        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="ATM DASHBOARD",
            font=("Arial", 22, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(30, 20),
            sticky="ew"
        )

        buttons = [
            ("Check Balance", self.check_balance),
            ("Deposit Money", self.deposit_money),
            ("Withdraw Money", self.withdraw_money),
            ("Transfer Funds", self.transfer_funds),
            ("Transaction History", self.show_transaction_history)
        ]

        row = 1

        for text, command in buttons:

            ctk.CTkButton(
                frame,
                text=text,
                height=42,
                command=command
            ).grid(
                row=row,
                column=0,
                sticky="ew",
                padx=40,
                pady=6
            )

            row += 1

        ctk.CTkButton(
            frame,
            text="Logout",
            height=42,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Arial", 14, "bold"),
            command=self.logout
        ).grid(
            row=row,
            column=0,
            sticky="ew",
            padx=40,
            pady=(20, 10)
        )

    def logout(self):
        self.current_account = None
        self.show_login_screen()

    # =========================================================
    # BALANCE
    # =========================================================

    def check_balance(self):

        try:
            balance = database.get_balance(
                self.current_account
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return

        messagebox.showinfo(
            "Balance",
            f"Your current available balance is:\n\n"
            f"₹{balance:,.2f}"
        )

    # =========================================================
    # DEPOSIT
    # =========================================================

    def deposit_money(self):

        self.show_input_dialog(
            "Deposit Funds",
            "Enter amount to deposit (₹):",
            self.handle_deposit
        )

    def handle_deposit(
        self,
        amount_text,
        window
    ):

        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid positive amount."
            )
            return

        try:
            new_balance = database.update_balance(
                self.current_account,
                amount,
                "Cash Deposit"
            )

        except Exception as e:
            messagebox.showerror(
                "Deposit Failed",
                str(e)
            )
            return

        mobile = database.get_mobile(
            self.current_account
        )

        if mobile:
            sms_service_message = (
                "Cash Deposit"
            )

            import sms_service

            sms_service.send_transaction_sms(
                mobile,
                self.current_account,
                sms_service_message,
                amount,
                new_balance
            )

        window.destroy()

        messagebox.showinfo(
            "Success",
            f"Deposit successful!\n\n"
            f"New balance: ₹{new_balance:,.2f}"
        )

    # =========================================================
    # WITHDRAWAL
    # =========================================================

    def withdraw_money(self):

        self.show_input_dialog(
            "Withdraw Funds",
            "Enter amount to withdraw (₹):",
            self.handle_withdrawal
        )

    def handle_withdrawal(
        self,
        amount_text,
        window
    ):

        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid positive amount."
            )
            return

        balance = database.get_balance(
            self.current_account
        )

        if amount > balance:
            messagebox.showerror(
                "Error",
                "Insufficient available funds."
            )
            return

        if amount > 50000:

            otp = security.generate_otp()

            if not self.ask_for_otp(otp):
                messagebox.showwarning(
                    "Cancelled",
                    "Withdrawal cancelled."
                )
                return

        try:
            new_balance = database.update_balance(
                self.current_account,
                -amount,
                "Cash Withdrawal"
            )

        except Exception as e:
            messagebox.showerror(
                "Withdrawal Failed",
                str(e)
            )
            return

        import sms_service

        mobile = database.get_mobile(
            self.current_account
        )

        if mobile:
            sms_service.send_transaction_sms(
                mobile,
                self.current_account,
                "Cash Withdrawal",
                amount,
                new_balance
            )

        window.destroy()

        messagebox.showinfo(
            "Success",
            f"Withdrawal successful!\n\n"
            f"New balance: ₹{new_balance:,.2f}"
        )

    # =========================================================
    # TRANSFER
    # =========================================================

    def transfer_funds(self):

        window = ctk.CTkToplevel(self.root)

        window.title("Transfer Funds")
        window.geometry("380x320")
        window.minsize(340, 280)

        window.transient(self.root)
        window.grab_set()

        window.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            window,
            text="Recipient Account Number",
            font=("Arial", 12)
        ).grid(
            row=0,
            column=0,
            pady=(20, 2),
            sticky="w",
            padx=40
        )

        recipient_entry = ctk.CTkEntry(window)

        recipient_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=40,
            pady=5
        )

        ctk.CTkLabel(
            window,
            text="Amount to Transfer (₹)",
            font=("Arial", 12)
        ).grid(
            row=2,
            column=0,
            pady=(10, 2),
            sticky="w",
            padx=40
        )

        amount_entry = ctk.CTkEntry(window)

        amount_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=40,
            pady=5
        )

        def process():

            recipient = recipient_entry.get().strip()
            amount_text = amount_entry.get().strip()

            if not recipient:
                messagebox.showerror(
                    "Error",
                    "Recipient account number is required."
                )
                return

            if not recipient.isdigit():
                messagebox.showerror(
                    "Error",
                    "Recipient account number must contain "
                    "only digits."
                )
                return

            try:
                amount = float(amount_text)

                if amount <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Enter a valid positive amount."
                )
                return

            if recipient == self.current_account:
                messagebox.showerror(
                    "Error",
                    "You cannot transfer money to your "
                    "own account."
                )
                return

            success, message = transfers.execute_transfer(
                self.current_account,
                recipient,
                amount,
                otp_verifier=self.ask_for_otp
            )

            if success:
                window.destroy()

                messagebox.showinfo(
                    "Transfer Successful",
                    message
                )

            else:
                messagebox.showerror(
                    "Transfer Failed",
                    message
                )

        ctk.CTkButton(
            window,
            text="Confirm Transfer",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=process
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            padx=40,
            pady=25
        )

        recipient_entry.focus()

    # =========================================================
    # TRANSACTION HISTORY
    # =========================================================

    def show_transaction_history(self):

        history = database.get_transaction_history(
            self.current_account
        )

        window = ctk.CTkToplevel(self.root)

        window.title("Transaction History")
        window.geometry("600x450")

        window.transient(self.root)
        window.grab_set()

        frame = ctk.CTkFrame(
            window,
            corner_radius=10
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            frame,
            text="TRANSACTION HISTORY",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(20, 15)
        )

        if not history:

            ctk.CTkLabel(
                frame,
                text="No transactions found.",
                font=("Arial", 14)
            ).pack(pady=30)

        else:

            textbox = ctk.CTkTextbox(
                frame,
                width=520,
                height=300
            )

            textbox.pack(
                fill="both",
                expand=True,
                padx=15,
                pady=10
            )

            for tx_type, amount, timestamp in history:

                textbox.insert(
                    "end",
                    f"[{timestamp}]\n"
                    f"{tx_type}\n"
                    f"Amount: ₹{amount:,.2f}\n"
                    f"{'-' * 45}\n"
                )

            textbox.configure(
                state="disabled"
            )

        ctk.CTkButton(
            window,
            text="Close",
            command=window.destroy
        ).pack(
            pady=(0, 15)
        )

    # =========================================================
    # OTP
    # =========================================================

    def ask_for_otp(self, correct_otp):

        otp_window = ctk.CTkToplevel(self.root)

        otp_window.title("Security Verification")
        otp_window.geometry("380x280")

        otp_window.transient(self.root)
        otp_window.grab_set()

        otp_window.grid_columnconfigure(
            0,
            weight=1
        )

        messagebox.showwarning(
            "Security Alert",
            "High-value transaction detected "
            "(> ₹50,000)!\n\n"
            "[Simulated SMS]\n"
            f"Your 6-digit OTP is: {correct_otp}"
        )

        ctk.CTkLabel(
            otp_window,
            text="Enter 6-Digit OTP",
            font=("Arial", 14, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        otp_entry = ctk.CTkEntry(
            otp_window,
            height=40,
            font=("Arial", 16, "bold"),
            justify="center"
        )

        otp_entry.grid(
            row=1,
            column=0,
            padx=60,
            pady=5,
            sticky="ew"
        )

        attempts = 3
        verified = ctk.BooleanVar(
            value=False
        )

        def verify():

            nonlocal attempts

            entered = otp_entry.get().strip()

            if entered == str(correct_otp):

                verified.set(True)
                otp_window.destroy()
                return

            attempts -= 1

            if attempts <= 0:

                messagebox.showerror(
                    "Security Error",
                    "Too many incorrect attempts.\n"
                    "Transaction blocked."
                )

                otp_window.destroy()
                return

            messagebox.showerror(
                "Invalid OTP",
                f"Incorrect OTP.\n"
                f"{attempts} attempts remaining."
            )

            otp_entry.delete(
                0,
                "end"
            )

        ctk.CTkButton(
            otp_window,
            text="Verify OTP",
            height=40,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=verify
        ).grid(
            row=2,
            column=0,
            padx=60,
            pady=20,
            sticky="ew"
        )

        otp_entry.focus()

        self.root.wait_window(
            otp_window
        )

        return verified.get()

    # =========================================================
    # INPUT DIALOG
    # =========================================================

    def show_input_dialog(
        self,
        title,
        label_text,
        callback
    ):

        window = ctk.CTkToplevel(
            self.root
        )

        window.title(title)
        window.geometry("360x180")

        window.transient(
            self.root
        )

        window.grab_set()

        window.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            window,
            text=label_text,
            font=("Arial", 13)
        ).grid(
            row=0,
            column=0,
            pady=(25, 5)
        )

        entry = ctk.CTkEntry(
            window
        )

        entry.grid(
            row=1,
            column=0,
            padx=40,
            pady=5,
            sticky="ew"
        )

        def submit():
            callback(
                entry.get().strip(),
                window
            )

        ctk.CTkButton(
            window,
            text="Submit",
            height=35,
            command=submit
        ).grid(
            row=2,
            column=0,
            padx=40,
            pady=20,
            sticky="ew"
        )

        entry.bind(
            "<Return>",
            lambda event: submit()
        )

        entry.focus()


# =============================================================
# START APPLICATION
# =============================================================

if __name__ == "__main__":

    main_window = ctk.CTk()

    app = ModernATMGUI(
        main_window
    )

    main_window.mainloop()
