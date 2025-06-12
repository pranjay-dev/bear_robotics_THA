# Banking ATM System

## Overview

This project implements a simple banking system with an ATM controller, supporting basic operations such as card authentication, account selection, deposits, and withdrawals. The system includes support for account tiers with overdraft limits and maintains data persistence via CSV files.


## NOTES 
- I didnot enable overdraft withdrawls and leave it as future work.
- CSV data file (dummy_data.csv) is used for persistent storage of client information but is not encrypted or secure for production use.
---

## Architecture

### `bank_api.py`

- **Classes:**
  - **`Card`**  
    Represents a bank card with a card number and PIN.
  
  - **`Account`**  
    Represents a single bank account with attributes such as account ID, type (Checking or Saving), balance, tier, and overdraft limit.  
    - Methods:  
      - `deposit(amount)` — deposits money into the account.  
      - `withdraw(amount)` — withdraws money, considering overdraft limits.  
      - `get_balance()` — returns the current balance.
  
  - **`Bank`**  
    Manages multiple accounts, cards, and their data persistence. It stores accounts in a nested dictionary keyed by account ID and account type, mapping to the `Account` objects and associated cards.  
    - Key Methods:  
      - `_load_data()` and `_save_data()` — load/save account data from/to CSV file.  
      - `verify_card_pin(card_num, pin_code)` — returns matching accounts for a card and PIN.  
      - `get_account(acc_id, acc_type)` — retrieves an account object.  
      - `create_account()` and `add_card_to_account()` — for account and card management.  
      - `validate_pin(card_data)` — validates a card’s PIN across all accounts.  
      - `get_accounts(card_number)` — returns accessible accounts for a given card number.

---

### `atm_api.py`

- **Class:**
  - **`ATMController`**  
    Controls the ATM user session and operations. Manages card insertion, PIN authentication, account selection, deposits, and withdrawals.  
    - Attributes:  
      - `bank` — instance of `Bank`.  
      - `card` — current inserted card.  
      - `is_authenticated` — boolean authentication status.  
      - `accounts_for_card` — dict of accessible accounts for the inserted card.  
      - `active_account` — currently selected account for transactions.  
    - Key Methods:  
      - `insert_card(card)` — authenticates card and loads accounts.  
      - `choose_account(account_id)` — selects active account.  
      - `get_current_balance()` — fetches balance of active account.  
      - `make_deposit(amount)` — deposits money into active account.  
      - `make_withdrawal(amount)` — withdraws money from active account.  
      - `end_session()` — ends current ATM session and ejects card.

---

## Unit Test Cases (`unit_test.py`)

- **`test_bank_pin_validation()`**  
  Tests card number and PIN validation logic.  
  - Valid PIN returns accounts successfully.  
  - Invalid PIN returns no accounts.

- **`test_atm_flow_basic_operations()`**  
  Tests a basic ATM flow:  
  - Insert card and authenticate.  
  - Retrieve accessible accounts.  
  - Select an account.  
  - Check balance type correctness.  
  - Deposit and verify balance increase.  
  - Withdraw and verify balance decrease.  
  - End session cleanly.

---

## Process Flow

1. **Initialization:**  
   Bank data is loaded from a CSV file (`dummy_data.csv`). If the file doesn't exist, fresh data structures are initialized.

2. **Card Insertion & Authentication:**  
   ATM controller accepts a `Card` instance (card number + PIN).  
   Authentication validates PIN against stored cards and retrieves linked accounts.

3. **Account Selection:**  
   User selects one of the accessible accounts linked to the card.

4. **Transactions:**  
   - Deposits and withdrawals are executed on the selected account.  
   - Withdrawal respects overdraft limits based on account tier.

5. **Session End:**  
   Card is ejected, and session data reset.

---

## Print Statements

To streamline output without generating or managing log files, the system uses bracketed prefixes (e.g., `[ATM]`, `[DEBUG]`, `[UNIT-TEST]`) to differentiate the audience.

- `[ATM]` is shown to the **end-user** during ATM interactions, such as confirmations for deposits, withdrawals, or card ejection.
- `[DEBUG]` is used by **developers** to trace internal logic flow, including authentication success or failure, and account selection events.
- `[UNIT-TEST]` is reserved for **unit testing**, allowing automated test frameworks to validate expected behavior through clearly tagged outputs.

## Usage

Run unit tests:

```bash
python unit_test.py

```

## Running the `bank_api.py` and `atm_api.py` Files

To test and interact with the banking system, two main files are provided:

- `bank_api.py`: Implements the core banking backend, including account creation, card management, balance tracking, and PIN validation.
- `atm_api.py`: Acts as a front-end simulation of an ATM interface, using `bank_api` to perform operations like deposits and withdrawals.


## TECHNOLOGICAL DEBT

Despite offering core banking and ATM simulation functionality, several areas of the system currently carry **technological debt** that should be addressed in future iterations:

### 1. Logging
- There is no structured logging system or log-level control.

### 2. Overdraft
- Though limits are computed and stored, overdraft withdrawals are **not allowed** at runtime.

### 3. Secure Information Exchange
- No encryption, hashing, or secure handling of sensitive data.
