from atm_api import ATMController, Card
from bank_api import Bank
from typing import List, Tuple, Optional, Dict

def test_atm_flow_basic_operations():
    print("[UNIT-TEST] === Starting ATM Flow Test ===")
    bank = Bank(file_path='dummy_data.csv', operator="atm")

    # customer-001
    card = Card("1111-2222-3333-4444", "1234")

    atm = ATMController(bank)

    # Insert card and authenticate
    print("[UNIT-TEST] Inserting card and authenticating...")
    auth_success = atm.insert_card(card)
    assert auth_success, "Authentication failed!"

    # Check available accounts for card
    accounts = list(atm.accounts_for_card.keys())
    print("[UNIT-TEST] Available accounts linked to card:", accounts)
    assert len(accounts) > 0, "No accounts found for card!"

    # Choose first account
    atm.choose_account(accounts[0])
    print(f"[UNIT-TEST] Selected account {accounts[0]}")

    # Check balance (should be integer)
    balance = atm.get_current_balance()
    print(f"[UNIT-TEST] Current balance: ${balance}")
    assert isinstance(balance, int), "Balance should be integer"

    # Deposit 100 dollars
    atm.make_deposit(100)
    new_balance = atm.get_current_balance()
    print(f"[UNIT-TEST] Balance after deposit: ${new_balance}")
    assert new_balance == balance + 100, "Deposit amount not added correctly"

    # Withdraw 50 dollars
    atm.make_withdrawal(50)
    final_balance = atm.get_current_balance()
    print(f"[UNIT-TEST]  Balance after withdrawal: ${final_balance}")
    assert final_balance == new_balance - 50, "Withdrawal amount not deducted correctly" 

    # End session
    atm.end_session()
    print("[UNIT-TEST] === ATM Flow Test Completed ===")

def test_bank_pin_validation():
    print("[UNIT-TEST] === Starting Bank PIN Validation Test ===")
    bank = Bank(file_path='dummy_data.csv', operator="banker")

    # Valid card + pin
    valid_card_num = "1111-2222-3333-4444"
    valid_pin = "1234"
    accounts = bank.verify_card_pin(valid_card_num, valid_pin)
    print(f"[UNIT-TEST] Accounts for valid card+pin: {accounts}")
    assert len(accounts) > 0, "Valid card+pin did not return accounts"

    # Invalid pin
    invalid_pin = "0000"
    no_accounts = bank.verify_card_pin(valid_card_num, invalid_pin)
    print(f"[UNIT-TEST] Accounts for invalid pin: {no_accounts}")
    assert len(no_accounts) == 0, "Invalid pin should not return accounts"

    print("[UNIT-TEST] === Bank PIN Validation Test Completed ===")

if __name__ == "__main__":
    test_bank_pin_validation()
    test_atm_flow_basic_operations()