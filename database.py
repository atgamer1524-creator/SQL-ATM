import sqlite3
from datetime import datetime

DB_NAME = "atm_system.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            mobile TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (account_number)
                REFERENCES accounts(account_number)
                ON DELETE CASCADE
        )
    """)

    # Demo account
    cursor.execute("""
        INSERT OR IGNORE INTO accounts
        (account_number, pin, name, balance, mobile)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "12345",
        "1111",
        "Alice",
        5000.0,
        "9876543210"
    ))

    conn.commit()
    conn.close()


def create_account(account_num, pin, name, initial_deposit, mobile):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO accounts
            (account_number, pin, name, balance, mobile)
            VALUES (?, ?, ?, ?, ?)
        """, (
            account_num,
            pin,
            name,
            initial_deposit,
            mobile
        ))

        if initial_deposit > 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                account_num,
                "Initial Deposit",
                initial_deposit,
                now
            ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        conn.rollback()
        return False

    finally:
        conn.close()


def check_login(account_num, pin):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM accounts
            WHERE account_number = ?
              AND pin = ?
        """, (
            account_num,
            pin
        ))

        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        conn.close()


def get_balance(account_num):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = ?
        """, (account_num,))

        result = cursor.fetchone()

        return float(result[0]) if result else 0.0

    finally:
        conn.close()


def get_mobile(account_num):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mobile
            FROM accounts
            WHERE account_number = ?
        """, (account_num,))

        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        conn.close()


def account_exists(account_num):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM accounts
            WHERE account_number = ?
        """, (account_num,))

        return cursor.fetchone() is not None

    finally:
        conn.close()


def update_balance(account_num, amount, tx_type):
    """
    Updates an account balance and records the transaction.

    amount can be positive or negative.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = ?
        """, (account_num,))

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Account does not exist.")

        current_balance = float(result[0])
        new_balance = current_balance + float(amount)

        if new_balance < 0:
            raise ValueError("Insufficient funds.")

        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_number = ?
        """, (
            new_balance,
            account_num
        ))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO transactions
            (account_number, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            account_num,
            tx_type,
            abs(float(amount)),
            now
        ))

        conn.commit()

        return new_balance

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def transfer_balance(sender_acc, receiver_acc, amount):
    """
    Performs sender deduction and receiver credit atomically.

    Returns:
        (sender_new_balance, receiver_new_balance)
    """
    amount = float(amount)

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    if sender_acc == receiver_acc:
        raise ValueError(
            "You cannot transfer money to your own account."
        )

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Check sender
        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = ?
        """, (sender_acc,))

        sender_result = cursor.fetchone()

        if sender_result is None:
            raise ValueError("Sender account does not exist.")

        # Check receiver
        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = ?
        """, (receiver_acc,))

        receiver_result = cursor.fetchone()

        if receiver_result is None:
            raise ValueError(
                "Recipient account number does not exist."
            )

        sender_balance = float(sender_result[0])
        receiver_balance = float(receiver_result[0])

        if amount > sender_balance:
            raise ValueError(
                "Insufficient funds for this transfer."
            )

        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount

        # Deduct sender
        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_number = ?
        """, (
            new_sender_balance,
            sender_acc
        ))

        # Credit receiver
        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_number = ?
        """, (
            new_receiver_balance,
            receiver_acc
        ))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sender transaction
        cursor.execute("""
            INSERT INTO transactions
            (account_number, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            sender_acc,
            f"Transfer to {receiver_acc}",
            amount,
            now
        ))

        # Receiver transaction
        cursor.execute("""
            INSERT INTO transactions
            (account_number, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            receiver_acc,
            f"Transfer from {sender_acc}",
            amount,
            now
        ))

        conn.commit()

        return new_sender_balance, new_receiver_balance

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def log_transaction(account_num, tx_type, amount):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO transactions
            (account_number, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            account_num,
            tx_type,
            abs(float(amount)),
            now
        ))

        conn.commit()

    finally:
        conn.close()


def get_transaction_history(account_num):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT transaction_type, amount, timestamp
            FROM transactions
            WHERE account_number = ?
            ORDER BY id DESC
        """, (account_num,))

        return cursor.fetchall()

    finally:
        conn.close()
