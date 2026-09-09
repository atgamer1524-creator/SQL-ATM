# SQL-ATM Simulator 🏦✨

A desktop ATM simulation application built with **Python**, featuring a sleek user interface and a robust **SQL database** backend to manage banking operations safely.

## 🚀 Features

* **Secure Authentication:** User log-in verification managed securely via `security.py`.
* **Core Banking Operations:** Smooth deposit, withdrawal, and fund transfer systems handling live database updates via `transfers.py`.
* **Database Integration:** Centralized data storage managing account details and credentials via `database.py`.
* **SMS Notifications:** Live transactional alerts simulated seamlessly via `sms_service.py`.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database:** SQL (MySQL / SQLite)
* **Libraries:** Used for GUI layout, hashing, and database connectivity.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd SQL-ATM
   ```

2. **Configure your SQL database:**
   * Set up your local SQL server and ensure your configuration matches the connection details in `database.py`.

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🤝 License

Distributed under the MIT License. See `LICENSE` for more information.
