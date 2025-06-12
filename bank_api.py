import csv
import os
from typing import List, Tuple, Optional, Dict

class Card:
    def __init__(self, card_number: str, pin: str) -> None:
        self.card_number: str = card_number
        self.pin: str = pin

class Account:
    """
    Keeps track of one account type: Checking or Saving.
    """
    def __init__(self, acc_id: str, acc_type: str, bal: int = 0, tier: str = 'Standard', overdraft: int = 0) -> None:
        self.acc_id: str = acc_id
        self.acc_type: str = acc_type
        self.balance: int = bal
        self.tier: str = tier
        self.overdraft_limit: int = overdraft

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise Exception("Amount to deposit should be > 0")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise Exception("Amount to withdraw should be > 0")
        if self.balance + self.overdraft_limit < amount:
            raise Exception("Not enough funds including overdraft")
        self.balance -= amount

    def get_balance(self) -> int:
        return self.balance

class Bank:
    """
    Bank maintains accounts as a nested dict:
    account_id -> account_type -> {'account': Account, 'cards': {card_num: pin}}
    """
    accounts: Dict[str, Dict[str, Dict[str, object]]] = {}

    def __init__(self, file_path: str = 'dummy_data.csv', operator: str = "banker") -> None:
        allowed_operators = {'banker', 'atm'}
        if operator not in allowed_operators:
            raise ValueError(f"Invalid operator '{operator}'. Must be one of {allowed_operators}")

        self.file_path: str = file_path
        self.operator: str = operator
        self._load_data()

    def _load_data(self) -> None:
        if not os.path.isfile(self.file_path):
            # No file found, start fresh
            return
        with open(self.file_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc_id: str = row.get('account_id', '')
                acc_type: str = row.get('account_type', '')
                balance: int = int(row.get('balance') or 0)
                tier: str = row.get('tier') or 'Standard'
                card: str = row.get('card_number', '')
                pin: str = row.get('pin', '')

                overdraft: int = self._determine_overdraft(tier)

                if acc_id not in Bank.accounts:
                    Bank.accounts[acc_id] = {}

                if acc_type not in Bank.accounts[acc_id]:
                    Bank.accounts[acc_id][acc_type] = {
                        'account': Account(acc_id, acc_type, balance, tier, overdraft),
                        'cards': {}
                    }
                Bank.accounts[acc_id][acc_type]['cards'][card] = pin

    def _determine_overdraft(self, tier: str) -> int:
        if tier == 'Gold':
            return 500
        elif tier == 'Platinum':
            return 1000
        else:
            return 0

    def _save_data(self) -> None:
        with open(self.file_path, 'w', newline='') as f:
            fieldnames = ['account_id', 'account_type', 'balance', 'tier', 'card_number', 'pin']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for acc_id, types in Bank.accounts.items():
                for acc_type, data in types.items():
                    acct: Account = data['account']
                    bal: int = acct.get_balance()
                    tier: str = acct.tier
                    for card_num, pin in data['cards'].items():
                        writer.writerow({
                            'account_id': acc_id,
                            'account_type': acc_type,
                            'balance': bal,
                            'tier': tier,
                            'card_number': card_num,
                            'pin': pin
                        })

    def verify_card_pin(self, card_num: str, pin_code: str) -> List[Tuple[str, str]]:
        """
        Returns list of tuples (account_id, account_type) where card+pin match.
        """
        found_accounts: List[Tuple[str, str]] = []
        for acc_id, types in Bank.accounts.items():
            for acc_type, data in types.items():
                if card_num in data['cards'] and data['cards'][card_num] == pin_code:
                    found_accounts.append((acc_id, acc_type))
        return found_accounts

    def get_account(self, acc_id: str, acc_type: str) -> Optional[Account]:
        return Bank.accounts.get(acc_id, {}).get(acc_type, {}).get('account')

    def create_account(self, acc_id: str, acc_type: str, initial_balance: int, tier: str, card_num: str, pin: str) -> None:
        if acc_id in Bank.accounts and acc_type in Bank.accounts[acc_id]:
            raise Exception(f"Account {acc_id} with type {acc_type} already exists!")

        overdraft: int = self._determine_overdraft(tier)
        if acc_id not in Bank.accounts:
            Bank.accounts[acc_id] = {}

        Bank.accounts[acc_id][acc_type] = {
            'account': Account(acc_id, acc_type, initial_balance, tier, overdraft),
            'cards': {card_num: pin}
        }
        self._save_data()

    def add_card_to_account(self, acc_id: str, acc_type: str, card_num: str, pin: str) -> None:
        if acc_id not in Bank.accounts or acc_type not in Bank.accounts[acc_id]:
            raise Exception("No such account exists.")
        Bank.accounts[acc_id][acc_type]['cards'][card_num] = pin
        self._save_data()

    def save_all(self) -> None:
        self._save_data()

    def validate_pin(self, card_data: Card) -> bool:
        for acc_id, account_types in Bank.accounts.items():
            for acc_type, data in account_types.items():
                if card_data.card_number in data['cards']:
                    if data['cards'][card_data.card_number] == card_data.pin:
                        return True
        return False

    def get_accounts(self, card_number: str) -> Dict[Tuple[str, str], Account]:
        accessible_accounts: Dict[Tuple[str, str], Account] = {}
        for acc_id, account_types in Bank.accounts.items():
            for acc_type, data in account_types.items():
                if card_number in data['cards']:
                    accessible_accounts[(acc_id, acc_type)] = data['account']
        return accessible_accounts


if __name__ == '__main__':
    bank = Bank(file_path='dummy_data.csv', operator="banker")

    # create accounts for testing (may fail if already exists)
    try:
        bank.create_account("customer-100", "Checking", 1500, "Gold", "1111-2222-3333-4444", "1234")
    except Exception as e:
        print(f"Note: {e}")

    try:
        bank.create_account("customer-100", "Saving", 3000, "Gold", "5555-6666-7777-8888", "4321")
    except Exception as e:
        print(f"Note: {e}")

    # link extra cards
    try:
        bank.add_card_to_account("customer-100", "Checking", "9999-0000-1111-2222", "1234")
        bank.add_card_to_account("customer-100", "Saving", "8888-7777-6666-5555", "4321")
    except Exception as e:
        print(f"Failed to link card: {e}")

    # check pins
    result = bank.verify_card_pin("9999-0000-1111-2222", "1234")
    print("Accounts accessible with card+pin:", result)

    # operate on account
    acct = bank.get_account("customer-100", "Checking")
    if acct:
        try:
            acct.deposit(500)
            print(f"New balance for customer-100 Checking: {acct.get_balance()}")
            bank.save_all()
        except Exception as e:
            print(f"Operation failed: {e}")
    else:
        print("Account not found")