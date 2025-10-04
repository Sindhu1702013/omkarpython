"""
Unit tests for the BankAccount class.

This module demonstrates comprehensive testing for the improved BankAccount class,
including edge cases, error conditions, and business logic validation.
"""

import pytest
from decimal import Decimal
import sys
import os

# Add the parent directory to the path to import the BankAccount class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from OOP.P09_BankAccount import BankAccount, InsufficientFundsError, InvalidAmountError


class TestBankAccountInitialization:
    """Test cases for BankAccount initialization."""
    
    def test_basic_initialization(self):
        """Test basic account creation with valid parameters."""
        account = BankAccount("John Doe", 1000)
        assert account.name == "John Doe"
        assert account.balance == Decimal('1000')
        assert account.account_number >= 1000
    
    def test_initialization_with_zero_balance(self):
        """Test account creation with zero initial balance."""
        account = BankAccount("Jane Smith")
        assert account.name == "Jane Smith"
        assert account.balance == Decimal('0')
    
    def test_initialization_with_float_balance(self):
        """Test account creation with float initial balance."""
        account = BankAccount("Bob Johnson", 123.45)
        assert account.balance == Decimal('123.45')
    
    def test_initialization_with_string_balance(self):
        """Test account creation with string representation of number."""
        account = BankAccount("Alice Brown", "500.75")
        assert account.balance == Decimal('500.75')
    
    def test_unique_account_numbers(self):
        """Test that each account gets a unique account number."""
        account1 = BankAccount("Person 1", 100)
        account2 = BankAccount("Person 2", 200)
        assert account1.account_number != account2.account_number
        assert account2.account_number > account1.account_number
    
    def test_name_whitespace_handling(self):
        """Test that whitespace in names is properly handled."""
        account = BankAccount("  John Doe  ", 100)
        assert account.name == "John Doe"
    
    def test_invalid_name_empty_string(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Account holder name must be a non-empty string"):
            BankAccount("", 100)
    
    def test_invalid_name_whitespace_only(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Account holder name must be a non-empty string"):
            BankAccount("   ", 100)
    
    def test_invalid_name_non_string(self):
        """Test that non-string name raises ValueError."""
        with pytest.raises(ValueError, match="Account holder name must be a non-empty string"):
            BankAccount(123, 100)
    
    def test_negative_initial_balance(self):
        """Test that negative initial balance raises ValueError."""
        with pytest.raises(ValueError, match="Initial balance cannot be negative"):
            BankAccount("John Doe", -100)
    
    def test_invalid_initial_balance_type(self):
        """Test that invalid balance type raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Invalid initial balance"):
            BankAccount("John Doe", "invalid")


class TestBankAccountDeposit:
    """Test cases for deposit functionality."""
    
    @pytest.fixture
    def account(self):
        """Fixture providing a sample account for testing."""
        return BankAccount("Test User", 100)
    
    def test_valid_deposit_integer(self, account):
        """Test deposit with integer amount."""
        new_balance = account.deposit(50)
        assert new_balance == Decimal('150')
        assert account.balance == Decimal('150')
    
    def test_valid_deposit_float(self, account):
        """Test deposit with float amount."""
        new_balance = account.deposit(25.75)
        assert new_balance == Decimal('125.75')
        assert account.balance == Decimal('125.75')
    
    def test_valid_deposit_decimal(self, account):
        """Test deposit with Decimal amount."""
        new_balance = account.deposit(Decimal('33.33'))
        assert new_balance == Decimal('133.33')
        assert account.balance == Decimal('133.33')
    
    def test_valid_deposit_string(self, account):
        """Test deposit with string representation of number."""
        new_balance = account.deposit("75.25")
        assert new_balance == Decimal('175.25')
        assert account.balance == Decimal('175.25')
    
    def test_multiple_deposits(self, account):
        """Test multiple consecutive deposits."""
        account.deposit(25)
        account.deposit(30)
        final_balance = account.deposit(45)
        assert final_balance == Decimal('200')
        assert account.balance == Decimal('200')
    
    def test_deposit_zero_amount(self, account):
        """Test that depositing zero raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Deposit amount must be positive"):
            account.deposit(0)
    
    def test_deposit_negative_amount(self, account):
        """Test that depositing negative amount raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Deposit amount must be positive"):
            account.deposit(-50)
    
    def test_deposit_invalid_type(self, account):
        """Test that depositing invalid type raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Invalid deposit amount"):
            account.deposit("invalid")


class TestBankAccountWithdrawal:
    """Test cases for withdrawal functionality."""
    
    @pytest.fixture
    def account(self):
        """Fixture providing a sample account for testing."""
        return BankAccount("Test User", 1000)
    
    def test_valid_withdrawal_integer(self, account):
        """Test withdrawal with integer amount."""
        new_balance = account.withdraw(200)
        assert new_balance == Decimal('800')
        assert account.balance == Decimal('800')
    
    def test_valid_withdrawal_float(self, account):
        """Test withdrawal with float amount."""
        new_balance = account.withdraw(150.50)
        assert new_balance == Decimal('849.50')
        assert account.balance == Decimal('849.50')
    
    def test_valid_withdrawal_decimal(self, account):
        """Test withdrawal with Decimal amount."""
        new_balance = account.withdraw(Decimal('333.33'))
        assert new_balance == Decimal('666.67')
        assert account.balance == Decimal('666.67')
    
    def test_withdrawal_exact_balance(self, account):
        """Test withdrawal of exact balance amount."""
        new_balance = account.withdraw(1000)
        assert new_balance == Decimal('0')
        assert account.balance == Decimal('0')
    
    def test_multiple_withdrawals(self, account):
        """Test multiple consecutive withdrawals."""
        account.withdraw(100)
        account.withdraw(200)
        final_balance = account.withdraw(300)
        assert final_balance == Decimal('400')
        assert account.balance == Decimal('400')
    
    def test_withdrawal_insufficient_funds(self, account):
        """Test withdrawal exceeding balance raises InsufficientFundsError."""
        with pytest.raises(InsufficientFundsError, match="Insufficient funds"):
            account.withdraw(1500)
    
    def test_withdrawal_zero_amount(self, account):
        """Test that withdrawing zero raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Withdrawal amount must be positive"):
            account.withdraw(0)
    
    def test_withdrawal_negative_amount(self, account):
        """Test that withdrawing negative amount raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Withdrawal amount must be positive"):
            account.withdraw(-100)
    
    def test_withdrawal_invalid_type(self, account):
        """Test that withdrawing invalid type raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Invalid withdrawal amount"):
            account.withdraw("invalid")


class TestBankAccountTransfer:
    """Test cases for transfer functionality."""
    
    @pytest.fixture
    def accounts(self):
        """Fixture providing two sample accounts for testing."""
        sender = BankAccount("Alice", 1000)
        receiver = BankAccount("Bob", 500)
        return sender, receiver
    
    def test_valid_transfer(self, accounts):
        """Test valid transfer between accounts."""
        sender, receiver = accounts
        sender_balance, receiver_balance = sender.transfer_to(receiver, 200)
        
        assert sender_balance == Decimal('800')
        assert receiver_balance == Decimal('700')
        assert sender.balance == Decimal('800')
        assert receiver.balance == Decimal('700')
    
    def test_transfer_exact_balance(self, accounts):
        """Test transfer of sender's entire balance."""
        sender, receiver = accounts
        sender_balance, receiver_balance = sender.transfer_to(receiver, 1000)
        
        assert sender_balance == Decimal('0')
        assert receiver_balance == Decimal('1500')
    
    def test_transfer_insufficient_funds(self, accounts):
        """Test transfer exceeding sender's balance."""
        sender, receiver = accounts
        with pytest.raises(InsufficientFundsError):
            sender.transfer_to(receiver, 1500)
    
    def test_transfer_invalid_destination(self, accounts):
        """Test transfer to non-BankAccount object."""
        sender, _ = accounts
        with pytest.raises(TypeError, match="Transfer destination must be a BankAccount instance"):
            sender.transfer_to("not_an_account", 100)
    
    def test_transfer_invalid_amount(self, accounts):
        """Test transfer with invalid amount."""
        sender, receiver = accounts
        with pytest.raises(InvalidAmountError):
            sender.transfer_to(receiver, -100)


class TestBankAccountUtilityMethods:
    """Test cases for utility methods."""
    
    @pytest.fixture
    def account(self):
        """Fixture providing a sample account for testing."""
        return BankAccount("Test User", 500.75)
    
    def test_get_balance(self, account):
        """Test get_balance method."""
        balance = account.get_balance()
        assert balance == Decimal('500.75')
        assert isinstance(balance, Decimal)
    
    def test_get_account_info(self, account):
        """Test get_account_info method."""
        info = account.get_account_info()
        
        assert isinstance(info, dict)
        assert info['name'] == "Test User"
        assert info['balance'] == Decimal('500.75')
        assert isinstance(info['account_number'], int)
        assert info['account_number'] >= 1000
    
    def test_str_representation(self, account):
        """Test string representation."""
        str_repr = str(account)
        assert "BankAccount" in str_repr
        assert "Test User" in str_repr
        assert "500.75" in str_repr
    
    def test_repr_representation(self, account):
        """Test detailed string representation."""
        repr_str = repr(account)
        assert "BankAccount" in repr_str
        assert "account_number=" in repr_str
        assert "name='Test User'" in repr_str
        assert "balance=500.75" in repr_str
    
    def test_equality_same_account_number(self):
        """Test equality comparison with same account number."""
        # This is tricky since account numbers auto-increment
        # We'll test the equality logic by creating accounts and comparing
        account1 = BankAccount("User 1", 100)
        account2 = BankAccount("User 2", 200)
        
        # They should not be equal (different account numbers)
        assert account1 != account2
        
        # An account should be equal to itself
        assert account1 == account1
    
    def test_equality_different_types(self, account):
        """Test equality comparison with different object types."""
        assert account != "not_an_account"
        assert account != 123
        assert account != None


class TestBankAccountEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_very_large_amounts(self):
        """Test operations with very large amounts."""
        account = BankAccount("Rich Person", Decimal('999999999.99'))
        
        # Should handle large deposits
        account.deposit(Decimal('0.01'))
        assert account.balance == Decimal('1000000000.00')
        
        # Should handle large withdrawals
        account.withdraw(Decimal('500000000.00'))
        assert account.balance == Decimal('500000000.00')
    
    def test_precision_handling(self):
        """Test decimal precision in calculations."""
        account = BankAccount("Precise Person", Decimal('100.00'))
        
        # Test operations that might cause precision issues with floats
        account.deposit(Decimal('0.01'))
        account.deposit(Decimal('0.02'))
        account.withdraw(Decimal('0.01'))
        
        assert account.balance == Decimal('100.02')
    
    def test_account_state_after_errors(self):
        """Test that account state remains unchanged after failed operations."""
        account = BankAccount("Test User", 100)
        original_balance = account.balance
        
        # Try invalid operations
        try:
            account.withdraw(200)  # Should fail
        except InsufficientFundsError:
            pass
        
        try:
            account.deposit(-50)  # Should fail
        except InvalidAmountError:
            pass
        
        # Balance should remain unchanged
        assert account.balance == original_balance
    
    def test_concurrent_operations_simulation(self):
        """Test multiple operations in sequence to simulate concurrent access."""
        account = BankAccount("Busy Person", 1000)
        
        # Simulate multiple rapid operations
        operations = [
            ('deposit', 100),
            ('withdraw', 50),
            ('deposit', 25),
            ('withdraw', 75),
            ('deposit', 200)
        ]
        
        expected_balance = Decimal('1000')
        for operation, amount in operations:
            if operation == 'deposit':
                account.deposit(amount)
                expected_balance += Decimal(str(amount))
            else:
                account.withdraw(amount)
                expected_balance -= Decimal(str(amount))
        
        assert account.balance == expected_balance


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])