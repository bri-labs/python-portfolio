"""
Lists Utilities Module

A collection of minimalistic functions for working with Python lists/
Function includes doctest-style examples for clarity and quick validation

Run doctests to verify all examples:

Minimal mode: 
    python -m doctest lists.py

Verbose mode (shows passing tests too):
    python -m doctest -v lists.py

"""
import copy


def chunk_list(in_list: list, size: int) -> list:
    """
    Splits a list into chunks of a specified size

    Args:
        in_list (list): List of elements
        size (int): Chunk size
    
    Returns:
        list: List of chunked sublists
    
    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [in_list[i:i + size] for i in range(0, len(in_list), size)]

def clear_list(in_list:list) -> list:
    """
    Removes all elements from a list
    
    Args:
        in_list (list): List of elements
    
    Returns:
        list: Empty list

    Example:
        >>> clear_list([1, 2, 3, 4, 5])
        []
    """
    in_list.clear()
    return in_list

def copy_deep(in_list: list) -> list:
    """
    Creates a deep copy of a list (with no ties, think copy by value)

    Args: 
        in_list (list): List of elements
    
    Returns:
        list: Deep Copy of original list
    
    Example:
        >>> original = [1, 2, 3, 4, 5]
        >>> clone = copy_deep(original)
        >>> clone.append(6)
        >>> original
        [1, 2, 3, 4, 5]
        >>> clone
        [1, 2, 3, 4, 5, 6]
    """
    return copy.deepcopy(in_list)

def copy_shallow(in_list: list) -> list:
    """
    Creates a shallow copy of a list (mutable objects will have ties, think copy by reference)
    
    - Mutable elements are still referenced; changes to them affect both lists

    Args:
        in_list (list): List of elements
    
    Returns:
        list: Shallow copy of original list
    
    Example:
        >>> original = [[1, 2], [3, 4]]
        >>> clone = copy_shallow(original)
        >>> clone[0][0] = 99
        >>> original
        [[99, 2], [3, 4]]
        >>> clone
        [[99, 2], [3, 4]]
    """
    return in_list.copy()

def count_element_frequency(in_list: list, target_element:any) -> int:
    """
    Counts the number of times a specific element appears in a list
    
    Args:
        in_list (list): List of elements
        target_element: Element to count
    
    Return:
        int: Number of occurrences of the element
    
    Example:
        >>> count_element_frequency(['pink', 'blue', 'pink', 'cherry', 'lime'], 'pink')
        2
    """
    return in_list.count(target_element)

def element_append(in_list:list, element) -> list:
    """
    Adds an element to the end of a list

    - Modifies list in-place
    - Time Complexity: O(1)

    Args: 
        in_list (list): List of elements
        element: Element to append
    
    Returns:
        list: Same list with new element added
    
    Example:
        >>> element_append(['coke', 'fanta'], 'sprite')
        ['coke', 'fanta', 'sprite']
    """
    in_list.append(element)
    return in_list

def element_index(in_list:list, element:any) -> int:
    """
    Retrieves index of specified element
    
    Args:
        in_list (list): List of elements
        element: Target element to locase
    
    Returns:
        int: Index of element
    
    Example:
        >>> element_index(['coke', 'fanta', 'sprite'], 'fanta')
        1
    """
    try:
        return in_list.index(element)
    except ValueError:
        return None
    
def element_insert(in_list:list, pos:int, element) -> list:
    """
    Inserts an element at the specified index
    
    - Does not overwrite an element; instead elements shifted
    - Modified in-place
    
    Args:
        in_list (list): List of elements
        pos (int): Index to insert an element
        element: Element to insert
    
    Returns:
        list: Contains inserted element
    
    Example:
        >>> element_insert(['coke', 'fanta', 'sprite'], 0, 'lemonade')
        ['lemonade', 'coke', 'fanta', 'sprite']
    """
    in_list.insert(pos, element)
    return in_list

def element_pop(in_list: list, pos:int) -> tuple[list, any]:
    """
    Removes an element by a specified position
    
    - Modified in-place
    
    Args:
        in_list (list): List of elements
        pos (int): Index of the element to remove
    
    Returns:
        tuple: (Modified list, removed element)
    
    Example:
        >>> element_pop(['coke', 'fanta', 'sprite'], 1)
        (['coke', 'sprite'], 'fanta')
    """
    removed = in_list.pop(pos)
    return in_list, removed

def element_remove(in_list:list, element) -> list:
    """
    Removes first occurrence of a specified element
    
    - Modified in-place

    Args:
        in_list (list): List of elements
        element: Element to remove
    
    Returns:
        list: Modified list 
    
    Example:
        >>> element_remove(['pink', 'blue', 'pink', 'cherry', 'lime'], 'pink')
        ['blue', 'pink', 'cherry', 'lime']
    """
    in_list.remove(element)
    return in_list
    

def extend_list(list1: list, list2: list) -> list:
    """
    Extends a list by appending elements from another list

    - Modifies list in-place
    
    Args:
        list1 (list): Original list of elements
        list2 (list): Additinl list of elements

    Return:
        list: Combined list with elemets from both

    Example:
        >>> extend_list([1, 2, 3], ['coke', 'fanta', 'sprite'])
        [1, 2, 3, 'coke', 'fanta', 'sprite']
    """
    list1.extend(list2)
    return list1

def reverse_list(in_list:list) -> list:
    """
    Reverses the order of a list

    - Modifies list in-place
    
    Args:
        in_list(list): List of elements
    
    Returns:
        list: List in reverse

    Example:
        >>> original = [1, 2, 3]
        >>> reversed = reverse_list(original)
        >>> (original, reversed)
        ([3, 2, 1], [3, 2, 1])
    """
    in_list.reverse()
    return in_list

def reverse_list_copy(in_list:list) -> list:
    """
    Reverses order of a list by creating a copy

    - Does NOT modify original list
    
    Args:
        in_list(list): List of elements
    
    Returns:
        list: New list in reverse
    
    Example:
    >>> original = [1, 2, 3]
    >>> reversed = reverse_list_copy(original)
    >>> (original, reversed)
    ([1, 2, 3], [3, 2, 1])
    """
    return in_list[::-1]

def sort_by_reference(in_list:list) -> list:
    """
    Sorts a list in ascending order using Python's built-in `sort()` method
    
    - Perform in-place sort; original list modified
    - Memory efficient for large lists        
    - Time Complexity: O(n log n)

    Args:
        in_list (list): List of comparible elements
    
    Returns:
        list: original list now sorted
    
    Example:
        >>> original = [3, 1, 6, 4]
        >>> sorted = sort_by_reference(original)
        >>> (original, sorted)
        ([1, 3, 4, 6], [1, 3, 4, 6])
    """
    in_list.sort()
    return in_list


def sort_by_value(in_list:list) -> list:
    """
    Sorts a list in ascending order using Python's built-in `sorted()` method
    
    - Returns a new list; original remains unchanged
    - Not memory-efficient for large lists
    - Time Complexity: O(n log n)

    Args:
        in_list (list): List of comparible elements

    Returns:
        list: Sorted list

    Example:
        >>> original = [3, 1, 6, 4]
        >>> sorted = sort_by_value(original)
        >>> (original, sorted)
        ([3, 1, 6, 4], [1, 3, 4, 6])
    """
    return sorted(in_list)

def unique_elements(in_list:list) -> list:
    """
    Removes duplicate elements while preserving order

    Args:
        in_list (list): List of elements
    
    Returns:
        list: List with duplicates removed
    
    Example:
        >>> unique_elements([3, 1, 3, 6, 4, 4])
        [3, 1, 6, 4]
    """
    seen = set()
    return [x for x in in_list if not (x in seen or seen.add(x))]


def zip_lists(list1:list, list2:list) -> list:
    """
    Zips two lists into a list of paired tuples

    - Stops at the shortest list

    Args:
        list1 (list): First list of elements
        list2 (list): Second list of elements
    
    Returns:
        list: List of tuples pairing elements from both lists
    
    Example:
        >>> zip_lists([1, 2, 3], ['coke', 'fanta', 'sprite'])
        [(1, 'coke'), (2, 'fanta'), (3, 'sprite')]
    """
    return list(zip(list1, list2))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)







    
    