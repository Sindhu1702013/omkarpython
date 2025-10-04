"""
Unit tests for the Array class.

This module demonstrates comprehensive testing using pytest framework
with proper test organization, fixtures, and edge case coverage.
"""

import pytest
from typing import Any
import sys
import os

# Add the parent directory to the path to import the Array class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Programs.P30_Array import Array, ArrayError


class TestArrayInitialization:
    """Test cases for Array initialization."""
    
    def test_empty_array_creation(self):
        """Test creating an empty array with default None values."""
        arr = Array(5)
        assert arr.size == 5
        assert arr.items == [None, None, None, None, None]
        assert arr.get_length() == 0
    
    def test_array_with_single_default_value(self):
        """Test creating an array with a single default value."""
        arr = Array(3, 0)
        assert arr.size == 3
        assert arr.items == [0, 0, 0]
        assert arr.get_length() == 3
    
    def test_array_with_list_initialization(self):
        """Test creating an array with a list of initial values."""
        arr = Array(5, [1, 2, 3])
        assert arr.size == 5
        assert arr.items == [1, 2, 3, None, None]
        assert arr.get_length() == 3
    
    def test_array_with_full_list_initialization(self):
        """Test creating an array with a complete list of values."""
        arr = Array(3, [1, 2, 3])
        assert arr.size == 3
        assert arr.items == [1, 2, 3]
        assert arr.get_length() == 3
    
    def test_invalid_size_type(self):
        """Test that non-integer size raises TypeError."""
        with pytest.raises(TypeError, match="Size must be an integer"):
            Array("5")
        
        with pytest.raises(TypeError, match="Size must be an integer"):
            Array(5.5)
    
    def test_invalid_size_value(self):
        """Test that non-positive size raises ValueError."""
        with pytest.raises(ValueError, match="Size must be positive"):
            Array(0)
        
        with pytest.raises(ValueError, match="Size must be positive"):
            Array(-1)
    
    def test_oversized_initial_list(self):
        """Test that initial list larger than size raises ValueError."""
        with pytest.raises(ValueError, match="Initial values list length .* exceeds array size"):
            Array(2, [1, 2, 3, 4])


class TestArrayInsertion:
    """Test cases for Array insertion methods."""
    
    @pytest.fixture
    def sample_array(self):
        """Fixture providing a sample array for testing."""
        return Array(5, [1, 2])
    
    def test_insert_first_success(self, sample_array):
        """Test successful insertion at the beginning."""
        sample_array.insert_first(0)
        assert sample_array.items == [0, 1, 2, None, None]
        assert sample_array.get_length() == 3
    
    def test_insert_first_full_array(self):
        """Test insertion when array is full."""
        arr = Array(2, [1, 2])
        with pytest.raises(ArrayError, match="Cannot insert: array is full"):
            arr.insert_first(0)
    
    def test_insert_at_index_success(self, sample_array):
        """Test successful insertion at specific index."""
        sample_array.insert_at_index(1, 1.5)
        assert sample_array.items == [1, 1.5, 2, None, None]
        assert sample_array.get_length() == 3
    
    def test_insert_at_index_beginning(self, sample_array):
        """Test insertion at index 0."""
        sample_array.insert_at_index(0, 0)
        assert sample_array.items == [0, 1, 2, None, None]
    
    def test_insert_at_index_end(self, sample_array):
        """Test insertion at the end of current elements."""
        sample_array.insert_at_index(2, 3)
        assert sample_array.items == [1, 2, 3, None, None]
    
    def test_insert_at_invalid_index(self, sample_array):
        """Test insertion at invalid indices."""
        with pytest.raises(IndexError, match="Index .* out of bounds"):
            sample_array.insert_at_index(-1, 0)
        
        with pytest.raises(IndexError, match="Index .* out of bounds"):
            sample_array.insert_at_index(10, 0)
    
    def test_insert_after_index_success(self, sample_array):
        """Test successful insertion after specific index."""
        sample_array.insert_after_index(0, 1.5)
        assert sample_array.items == [1, 1.5, 2, None, None]
    
    def test_insert_after_invalid_index(self, sample_array):
        """Test insertion after invalid index."""
        with pytest.raises(IndexError, match="Index .* out of bounds"):
            sample_array.insert_after_index(5, 0)
    
    def test_insert_before_index_success(self, sample_array):
        """Test successful insertion before specific index."""
        sample_array.insert_before_index(1, 1.5)
        assert sample_array.items == [1, 1.5, 2, None, None]


class TestArrayDeletion:
    """Test cases for Array deletion methods."""
    
    @pytest.fixture
    def sample_array(self):
        """Fixture providing a sample array for testing."""
        return Array(5, [1, 2, 3, 2])
    
    def test_delete_existing_element(self, sample_array):
        """Test deletion of existing element."""
        result = sample_array.delete(2)
        assert result is True
        assert sample_array.items == [1, None, 3, 2, None]  # First occurrence deleted
        assert sample_array.get_length() == 3
    
    def test_delete_nonexistent_element(self, sample_array):
        """Test deletion of non-existent element."""
        result = sample_array.delete(99)
        assert result is False
        assert sample_array.items == [1, 2, 3, 2, None]  # No change
        assert sample_array.get_length() == 4
    
    def test_delete_none_element(self):
        """Test deletion of None element."""
        arr = Array(3, [1, None, 2])
        result = arr.delete(None)
        assert result is True
        assert arr.get_length() == 2


class TestArraySearch:
    """Test cases for Array search methods."""
    
    @pytest.fixture
    def sample_array(self):
        """Fixture providing a sample array for testing."""
        return Array(5, [1, 2, 3, 2])
    
    def test_search_existing_element(self, sample_array):
        """Test searching for existing element."""
        result = sample_array.search(2)
        assert result == 1  # First occurrence
    
    def test_search_nonexistent_element(self, sample_array):
        """Test searching for non-existent element."""
        result = sample_array.search(99)
        assert result is None
    
    def test_search_none_element(self):
        """Test searching for None element."""
        arr = Array(3, [1, None, 2])
        result = arr.search(None)
        assert result == 1


class TestArrayUtilityMethods:
    """Test cases for Array utility methods."""
    
    def test_get_length_empty_array(self):
        """Test length calculation for empty array."""
        arr = Array(5)
        assert arr.get_length() == 0
    
    def test_get_length_partial_array(self):
        """Test length calculation for partially filled array."""
        arr = Array(5, [1, 2, None, 3])
        assert arr.get_length() == 3
    
    def test_get_length_full_array(self):
        """Test length calculation for full array."""
        arr = Array(3, [1, 2, 3])
        assert arr.get_length() == 3
    
    def test_str_representation(self):
        """Test string representation of array."""
        arr = Array(3, [1, 2])
        expected = "Array(size=3, items=[1, 2, None])"
        assert str(arr) == expected
    
    def test_repr_representation(self):
        """Test detailed string representation of array."""
        arr = Array(3, [1, 2])
        expected = "Array(size=3, length=2, items=[1, 2, None])"
        assert repr(arr) == expected


class TestArrayEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_single_element_array(self):
        """Test operations on single-element array."""
        arr = Array(1, [42])
        assert arr.get_length() == 1
        
        # Should not be able to insert more
        with pytest.raises(ArrayError):
            arr.insert_first(0)
        
        # Should be able to delete and search
        assert arr.search(42) == 0
        assert arr.delete(42) is True
        assert arr.get_length() == 0
    
    def test_operations_on_empty_array(self):
        """Test operations on completely empty array."""
        arr = Array(3)
        
        # Insert should work
        arr.insert_first(1)
        assert arr.items == [1, None, None]
        
        # Search for non-existent should return None
        assert arr.search(99) is None
        
        # Delete non-existent should return False
        assert arr.delete(99) is False
    
    def test_mixed_data_types(self):
        """Test array with mixed data types."""
        arr = Array(4, [1, "hello", 3.14])
        assert arr.get_length() == 3
        
        arr.insert_first([1, 2, 3])  # Insert a list
        assert arr.items[0] == [1, 2, 3]
        
        assert arr.search("hello") == 2  # String should be found
        assert arr.search(3.14) == 3    # Float should be found


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])