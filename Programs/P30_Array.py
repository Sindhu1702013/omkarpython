"""
Author: OMKAR PATHAK
This module implements a custom Array class with fixed size and various operations.
"""

from typing import List, Optional, Union, Any


class ArrayError(Exception):
    """Custom exception for Array operations."""
    pass


class Array:
    """
    A fixed-size array implementation with various manipulation methods.
    
    This class provides a static array implementation similar to arrays in other
    programming languages, with bounds checking and various insertion/deletion methods.
    
    Attributes:
        size (int): The maximum capacity of the array
        items (List[Any]): The internal list storing array elements
    """
    
    def __init__(self, size: int, default_value: Optional[Union[List[Any], Any]] = None) -> None:
        """
        Initialize a new Array with specified size and optional default values.
        
        Args:
            size: The fixed size of the array (must be positive)
            default_value: Either a single value to fill the array, or a list of initial values
            
        Raises:
            ValueError: If size is not positive or if default_value list is larger than size
            TypeError: If size is not an integer
            
        Examples:
            >>> arr = Array(5)  # Creates array of size 5 filled with None
            >>> arr = Array(3, 0)  # Creates array [0, 0, 0]
            >>> arr = Array(4, [1, 2])  # Creates array [1, 2, None, None]
        """
        if not isinstance(size, int):
            raise TypeError(f"Size must be an integer, got {type(size).__name__}")
        if size <= 0:
            raise ValueError(f"Size must be positive, got {size}")
            
        self.size = size
        self.items: List[Any] = []
        
        if default_value is None:
            # Initialize all elements as None
            self.items = [None] * size
        elif isinstance(default_value, list):
            # User provided a list of initial values
            if len(default_value) > size:
                raise ValueError(f"Initial values list length ({len(default_value)}) "
                               f"exceeds array size ({size})")
            
            # Copy provided values and fill remaining with None
            self.items = default_value.copy()
            self.items.extend([None] * (size - len(default_value)))
        else:
            # Single default value for all elements
            self.items = [default_value] * size

    def get_length(self) -> int:
        """
        Calculate the number of non-None elements in the array.
        
        Returns:
            int: Count of initialized elements (non-None values)
            
        Examples:
            >>> arr = Array(5, [1, 2, None, 3])
            >>> arr.get_length()
            3
        """
        return sum(1 for item in self.items if item is not None)

    def insert_first(self, element: Any) -> None:
        """
        Insert an element at the beginning of the array.
        
        Shifts all existing elements one position to the right.
        
        Args:
            element: The element to insert
            
        Raises:
            ArrayError: If the array is full
            
        Examples:
            >>> arr = Array(3, [1, 2])
            >>> arr.insert_first(0)
            >>> print(arr.items)
            [0, 1, 2]
        """
        if self.get_length() >= self.size:
            raise ArrayError("Cannot insert: array is full")
            
        # Shift elements to the right
        for i in range(self.get_length(), 0, -1):
            self.items[i] = self.items[i - 1]
        self.items[0] = element

    def insert_at_index(self, index: int, element: Any) -> None:
        """
        Insert an element at the specified index.
        
        Args:
            index: The position to insert at (0-based)
            element: The element to insert
            
        Raises:
            ArrayError: If the array is full
            IndexError: If index is out of bounds
            
        Examples:
            >>> arr = Array(4, [1, 3])
            >>> arr.insert_at_index(1, 2)
            >>> print(arr.items)
            [1, 2, 3, None]
        """
        if self.get_length() >= self.size:
            raise ArrayError("Cannot insert: array is full")
        if index < 0 or index > self.get_length():
            raise IndexError(f"Index {index} out of bounds for array length {self.get_length()}")
            
        # Shift elements to the right from the insertion point
        for i in range(self.get_length(), index, -1):
            self.items[i] = self.items[i - 1]
        self.items[index] = element

    def insert_after_index(self, index: int, element: Any) -> None:
        """
        Insert an element after the specified index.
        
        Args:
            index: The position after which to insert
            element: The element to insert
            
        Raises:
            ArrayError: If the array is full
            IndexError: If index is out of bounds
            
        Examples:
            >>> arr = Array(4, [1, 2])
            >>> arr.insert_after_index(0, 1.5)
            >>> print(arr.items)
            [1, 1.5, 2, None]
        """
        if self.get_length() >= self.size:
            raise ArrayError("Cannot insert: array is full")
        if index < 0 or index >= self.get_length():
            raise IndexError(f"Index {index} out of bounds for array length {self.get_length()}")
            
        # Insert at index + 1
        self.insert_at_index(index + 1, element)

    def insert_before_index(self, index: int, element: Any) -> None:
        """
        Insert an element before the specified index.
        
        Args:
            index: The position before which to insert
            element: The element to insert
            
        Raises:
            ArrayError: If the array is full
            IndexError: If index is out of bounds
            
        Examples:
            >>> arr = Array(4, [1, 3])
            >>> arr.insert_before_index(1, 2)
            >>> print(arr.items)
            [1, 2, 3, None]
        """
        if self.get_length() >= self.size:
            raise ArrayError("Cannot insert: array is full")
        if index < 0 or index > self.get_length():
            raise IndexError(f"Index {index} out of bounds for array length {self.get_length()}")
            
        # Insert at index (which shifts everything at index and after)
        self.insert_at_index(index, element)

    def delete(self, element: Any) -> bool:
        """
        Delete the first occurrence of an element from the array.
        
        Args:
            element: The element to delete
            
        Returns:
            bool: True if element was found and deleted, False otherwise
            
        Examples:
            >>> arr = Array(3, [1, 2, 3])
            >>> arr.delete(2)
            True
            >>> print(arr.items)
            [1, None, 3]
        """
        try:
            index = self.items.index(element)
            self.items[index] = None
            return True
        except ValueError:
            return False

    def search(self, element: Any) -> Optional[int]:
        """
        Search for an element in the array and return its position.
        
        Args:
            element: The element to search for
            
        Returns:
            Optional[int]: The index of the element if found, None otherwise
            
        Examples:
            >>> arr = Array(3, [1, 2, 3])
            >>> arr.search(2)
            1
            >>> arr.search(4) is None
            True
        """
        try:
            return self.items.index(element)
        except ValueError:
            return None

    def __str__(self) -> str:
        """Return a string representation of the array."""
        return f"Array(size={self.size}, items={self.items})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the array."""
        return f"Array(size={self.size}, length={self.get_length()}, items={self.items})"

if __name__ == '__main__':
    # Example usage demonstrating the improved Array class
    print("=== Array Class Demo ===")
    
    # Create array with initial values
    my_array = Array(5, [1])
    print(f"Initial: {my_array}")  # Array with [1, None, None, None, None]
    
    # Insert at beginning
    my_array.insert_first(3)
    print(f"After insert_first(3): {my_array}")
    
    # Insert after index
    my_array.insert_after_index(1, 4)
    print(f"After insert_after_index(1, 4): {my_array}")
    
    # Insert before index
    my_array.insert_before_index(3, 5)
    print(f"After insert_before_index(3, 5): {my_array}")
    
    # Delete element
    deleted = my_array.delete(5)
    print(f"After delete(5) - success: {deleted}, array: {my_array}")
    
    # Search for element
    position = my_array.search(4)
    print(f"Position of element 4: {position}")
    
    # Demonstrate error handling
    try:
        # Try to insert when array is full
        my_array.insert_first(99)
        my_array.insert_first(100)  # This should raise an error
    except ArrayError as e:
        print(f"Caught expected error: {e}")
    
    try:
        # Try invalid index
        my_array.insert_at_index(10, 999)
    except IndexError as e:
        print(f"Caught expected error: {e}")
