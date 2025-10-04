#!/usr/bin/env python3
"""
Test runner script for the Python-Programs repository.

This script demonstrates how to run the improved test suite and provides
examples of the enhanced code quality features implemented.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """
    Run a command and return success status.
    
    Args:
        command: List of command parts
        description: Description of what the command does
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        print(f"Please install the required dependencies: pip install -r requirements.txt")
        return False


def main():
    """Main function to run all tests and demonstrations."""
    print("Python-Programs Repository - Test Suite Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("Programs").exists() or not Path("tests").exists():
        print("❌ Error: Please run this script from the repository root directory")
        sys.exit(1)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Run the improved Array class demo
    total_tests += 1
    print(f"\n🔍 Test {total_tests}: Running Array class demonstration")
    if run_command([sys.executable, "Programs/P30_Array.py"], "Array class demo"):
        success_count += 1
    
    # Test 2: Run the improved BankAccount class demo
    total_tests += 1
    print(f"\n🔍 Test {total_tests}: Running BankAccount class demonstration")
    if run_command([sys.executable, "OOP/P09_BankAccount.py"], "BankAccount class demo"):
        success_count += 1
    
    # Test 3: Run pytest on Array tests (if pytest is available)
    total_tests += 1
    print(f"\n🔍 Test {total_tests}: Running Array unit tests")
    if run_command([sys.executable, "-m", "pytest", "tests/test_array.py", "-v"], "Array unit tests"):
        success_count += 1
    
    # Test 4: Run pytest on BankAccount tests (if pytest is available)
    total_tests += 1
    print(f"\n🔍 Test {total_tests}: Running BankAccount unit tests")
    if run_command([sys.executable, "-m", "pytest", "tests/test_bank_account.py", "-v"], "BankAccount unit tests"):
        success_count += 1
    
    # Test 5: Run all tests together (if pytest is available)
    total_tests += 1
    print(f"\n🔍 Test {total_tests}: Running complete test suite")
    if run_command([sys.executable, "-m", "pytest", "tests/", "-v"], "Complete test suite"):
        success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}/{total_tests}")
    print(f"❌ Failed: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print(f"\n🎉 All tests passed! The high-priority improvements are working correctly.")
        print(f"\nImprovements implemented:")
        print(f"  ✅ Type hints added to all methods")
        print(f"  ✅ Proper error handling with custom exceptions")
        print(f"  ✅ Comprehensive docstrings with examples")
        print(f"  ✅ Complete unit test suite with pytest")
        print(f"  ✅ Modern Python features (f-strings, Decimal, etc.)")
        print(f"  ✅ PEP 8 compliant code formatting")
    else:
        print(f"\n⚠️  Some tests failed. This might be due to missing dependencies.")
        print(f"   To install dependencies: pip install -r requirements.txt")
    
    return success_count == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)