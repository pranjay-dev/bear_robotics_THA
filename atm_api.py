from bank_api import Bank, Card
from typing import List, Tuple, Optional, Dict

class ATMController:
    """
    A simple controller to manage ATM sessions for a user.
    Handles card input, PIN auth, account selection, and transactions.
    """
    def __init__(self, bank: Bank) -> None:
        self.bank: Bank = bank
        self._reset_session()

    def _reset_session(self) -> None:
        self.card: Optional[Card] = None
        self.is_authenticated: bool = False
        self.accounts_for_card: Dict[Tuple[str, str], object] = {}
        self.active_account: Optional[object] = None

    def insert_card(self, card: Card) -> bool:
        self._reset_session()
        self.card = card
        print(f"[DEBUG] Card inserted")

        # validate_pin returns bool, so customer_id was misleading, treat as bool
        valid: bool = self.bank.validate_pin(self.card)
        if not valid:
            print("[ATM] PIN validation failed.")
            print("[DEBUG] PIN validation failed.")
            return False

        self.is_authenticated = True
        self.accounts_for_card = self.bank.get_accounts(self.card.card_number)
        print(f"[DEBUG] Auth successful")
        return True

    def choose_account(self, account_id: Tuple[str, str]) -> None:
        if not self.is_authenticated:
            raise PermissionError("User must be authenticated to select account.")

        if account_id not in self.accounts_for_card:
            raise LookupError(f"Account ID not found. Interbank transactions not supported")

        self.active_account = self.accounts_for_card[account_id]
        print(f"[ATM] Account '{account_id}' selected.")

    def get_current_balance(self) -> int:
        if not self.active_account:
            raise RuntimeError("No account is currently active.")
        return self.active_account.get_balance()

    def make_deposit(self, amount: int) -> None:
        if not self.active_account:
            raise RuntimeError("Deposit failed: No active account.")
        try:
            self.active_account.deposit(amount)
            print(f"[ATM] Deposited ${amount}. New balance: ${self.active_account.get_balance()}")
        except ValueError as e:
            print(f"[ATM] Deposit error: {e}")
            raise

    def make_withdrawal(self, amount: int) -> None:
        if not self.active_account:
            raise RuntimeError("Withdrawal failed: No active account.")
        try:
            self.active_account.withdraw(amount)
            print(f"[ATM] Withdrew ${amount}. Remaining balance: ${self.active_account.get_balance()}")
        except ValueError as e:
            print(f"[ATM] Withdrawal error: {e}")
            raise

    def end_session(self) -> None:
        if self.card:
            print(f"[ATM] Card {self.card.card_number} ejected. Session ended.")
        self._reset_session()

if __name__ == "__main__":
    bank = Bank(operator="atm")
    atm = ATMController(bank)

    # Insert Card and enter PIN
    card = Card("1234-0000-0000-5678", "4321")
    
    atm.insert_card(card)
    
    # Authentication
    if atm.is_authenticated :
        accounts = list(atm.accounts_for_card.keys())
        print("[DEBUG] Available accounts:", accounts)
        print("[DEBUG] Choosing the first account, in case of multiple accounts by same customer")
        atm.choose_account(accounts[0])
        print("[ATM] Balance:", atm.get_current_balance())
        atm.make_deposit(100)
        atm.make_withdrawal(50)
    else:
        print("Failed to authenticate.")

    atm.end_session()