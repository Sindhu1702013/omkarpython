"""
Author: OMKAR PATHAK
This module demonstrates Object-Oriented Programming concepts with a BankAccount class.

The BankAccount class showcases:
- Class and instance attributes
- Method definitions with proper error handling
- Type hints and comprehensive documentation
- Custom exceptions for domain-specific errors
"""

from typing import Union, Optional
from decimal import Decimal, InvalidOperation


class InsufficientFundsError(Exception):
    """Raised when attempting to withdraw more money than available in account."""
    pass


class InvalidAmountError(Exception):
    """Raised when an invalid amount is provided for transactions."""
    pass


class BankAccount:
    """
    A bank account class demonstrating OOP concepts with proper error handling.
    
    This class manages a bank account with deposit, withdrawal, and balance inquiry
    functionality. It includes proper validation and error handling for all operations.
    
    Class Attributes:
        _next_account_number (int): Counter for generating unique account numbers
        
    Instance Attributes:
        name (str): Account holder's name
        balance (Decimal): Current account balance
        account_number (int): Unique account identifier
    """
    
    _next_account_number: int = 1000  # Start account numbers from 1000
    
    def __init__(self, name: str, initial_balance: Union[int, float, Decimal] = 0) -> None:
        """
        Initialize a new bank account.
        
        Args:
            name: The account holder's name (must be non-empty)
            initial_balance: Starting balance (must be non-negative)
            
        Raises:
            ValueError: If name is empty or initial_balance is negative
            InvalidAmountError: If initial_balance is not a valid number
            
        Examples:
            >>> account = BankAccount("John Doe", 1000)
            >>> account.name
            'John Doe'
            >>> account.balance
            Decimal('1000')
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Account holder name must be a non-empty string")
            
        try:
            balance_decimal = Decimal(str(initial_balance))
            if balance_decimal < 0:
                raise ValueError("Initial balance cannot be negative")
        except (InvalidOperation, TypeError) as e:
            raise InvalidAmountError(f"Invalid initial balance: {initial_balance}") from e
            
        self.name = name.strip()
        self.balance = balance_decimal
        self.account_number = BankAccount._next_account_number
        BankAccount._next_account_number += 1
    
    def deposit(self, amount: Union[int, float, Decimal]) -> Decimal:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Returns:
            Decimal: New account balance after deposit
            
        Raises:
            InvalidAmountError: If amount is not positive or not a valid number
            
        Examples:
            >>> account = BankAccount("Jane Doe", 100)
            >>> account.deposit(50)
            Decimal('150')
            >>> account.balance
            Decimal('150')
        """
        try:
            deposit_amount = Decimal(str(amount))
            if deposit_amount <= 0:
                raise InvalidAmountError("Deposit amount must be positive")
        except (InvalidOperation, TypeError) as e:
            raise InvalidAmountError(f"Invalid deposit amount: {amount}") from e
            
        self.balance += deposit_amount
        return self.balance
    
    def withdraw(self, amount: Union[int, float, Decimal]) -> Decimal:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw (must be positive and not exceed balance)
            
        Returns:
            Decimal: New account balance after withdrawal
            
        Raises:
            InvalidAmountError: If amount is not positive or not a valid number
            InsufficientFundsError: If amount exceeds current balance
            
        Examples:
            >>> account = BankAccount("Bob Smith", 100)
            >>> account.withdraw(30)
            Decimal('70')
            >>> account.withdraw(100)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            InsufficientFundsError: Insufficient funds...
        """
        try:
            withdrawal_amount = Decimal(str(amount))
            if withdrawal_amount <= 0:
                raise InvalidAmountError("Withdrawal amount must be positive")
        except (InvalidOperation, TypeError) as e:
            raise InvalidAmountError(f"Invalid withdrawal amount: {amount}") from e
            
        if withdrawal_amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds. Attempted to withdraw {withdrawal_amount}, "
                f"but balance is only {self.balance}"
            )
            
        self.balance -= withdrawal_amount
        return self.balance
    
    def get_balance(self) -> Decimal:
        """
        Get the current account balance.
        
        Returns:
            Decimal: Current account balance
            
        Examples:
            >>> account = BankAccount("Alice Johnson", 250.50)
            >>> account.get_balance()
            Decimal('250.50')
        """
        return self.balance
    
    def get_account_info(self) -> dict:
        """
        Get comprehensive account information.
        
        Returns:
            dict: Dictionary containing account details
            
        Examples:
            >>> account = BankAccount("Charlie Brown", 500)
            >>> info = account.get_account_info()
            >>> info['name']
            'Charlie Brown'
            >>> info['balance']
            Decimal('500')
        """
        return {
            'account_number': self.account_number,
            'name': self.name,
            'balance': self.balance
        }
    
    def transfer_to(self, other_account: 'BankAccount', amount: Union[int, float, Decimal]) -> tuple[Decimal, Decimal]:
        """
        Transfer money to another bank account.
        
        Args:
            other_account: The destination BankAccount instance
            amount: Amount to transfer
            
        Returns:
            tuple[Decimal, Decimal]: (sender_new_balance, receiver_new_balance)
            
        Raises:
            TypeError: If other_account is not a BankAccount instance
            InvalidAmountError: If amount is invalid
            InsufficientFundsError: If insufficient funds for transfer
            
        Examples:
            >>> sender = BankAccount("Alice", 1000)
            >>> receiver = BankAccount("Bob", 500)
            >>> sender.transfer_to(receiver, 200)
            (Decimal('800'), Decimal('700'))
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("Transfer destination must be a BankAccount instance")
            
        # Withdraw from this account (includes validation)
        self.withdraw(amount)
        
        # Deposit to other account
        other_account.deposit(amount)
        
        return self.balance, other_account.balance
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"BankAccount(#{self.account_number}, {self.name}, Balance: ${self.balance})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"BankAccount(account_number={self.account_number}, name='{self.name}', balance={self.balance})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on account number."""
        if not isinstance(other, BankAccount):
            return False
        return self.account_number == other.account_number


if __name__ == '__main__':
    # Demonstration of the improved BankAccount class
    print("=== BankAccount Class Demo ===")
    
    # Create accounts
    account1 = BankAccount('Alice Johnson', 1000)
    account2 = BankAccount('Bob Smith', 500)
    
    print(f"Created accounts:")
    print(f"  {account1}")
    print(f"  {account2}")
    
    # Perform transactions
    print(f"\nPerforming transactions...")
    
    # Deposit
    new_balance = account1.deposit(250)
    print(f"Alice deposited $250. New balance: ${new_balance}")
    
    # Withdraw
    new_balance = account1.withdraw(150)
    print(f"Alice withdrew $150. New balance: ${new_balance}")
    
    # Transfer
    alice_balance, bob_balance = account1.transfer_to(account2, 300)
    print(f"Alice transferred $300 to Bob.")
    print(f"  Alice's balance: ${alice_balance}")
    print(f"  Bob's balance: ${bob_balance}")
    
    # Demonstrate error handling
    print(f"\nDemonstrating error handling...")
    
    try:
        account1.withdraw(2000)  # Should fail - insufficient funds
    except InsufficientFundsError as e:
        print(f"Caught expected error: {e}")
    
    try:
        account1.deposit(-50)  # Should fail - negative amount
    except InvalidAmountError as e:
        print(f"Caught expected error: {e}")
    
    try:
        BankAccount("", 100)  # Should fail - empty name
    except ValueError as e:
        print(f"Caught expected error: {e}")
