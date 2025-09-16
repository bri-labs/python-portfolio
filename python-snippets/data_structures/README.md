# 🧠 Data Structures Overview

This folder contains modular Python implementations of core and advanced data structures.  
Each file is designed to be clean, testable, and well-documented with doctest examples or unit tests where appropriate.

Use this as a quick reference to explore what's available.

---

## 📦 Core Containers

| Module         | Description                                 |
|----------------|---------------------------------------------|
| `lists.py`     | List utilities: chunking, copying, flattening, searching |
| `dicts.py`     | Dictionary operations: merging, filtering, key/value access |
| `sets.py`      | Set operations: unions, intersections, membership tests |
| `tuples.py`    | Tuple manipulation and conversion utilities |
| `namedtuples.py` | Using `collections.namedtuple` for structured records |

---

## 🧰 Enhanced Containers

| Module             | Description                                 |
|--------------------|---------------------------------------------|
| `defaultdicts.py`  | Auto-initializing dictionaries via `defaultdict` |
| `counters.py`      | Frequency counting with `collections.Counter` |
| `deque_collections.py` | Double-ended queues with fast append/pop |
| `dataclasses.py`   | Lightweight, structured data containers using `@dataclass` |
| `enum_structures.py` | Enumerated constants with `Enum` |

---

## 📚 Linear Structures

| Module           | Description                                 |
|------------------|---------------------------------------------|
| `stacks.py`      | LIFO stack implementation and utilities     |
| `queues.py`      | FIFO queue implementation and variations    |
| `arrays_numpy.py`| Array operations using NumPy                |

---

## 📊 Tabular Structures

| Module               | Description                                 |
|----------------------|---------------------------------------------|
| `dataframes_pandas.py` | DataFrame manipulation using Pandas       |
| `dataframes_polars.py` | Fast DataFrame operations using Polars    |

---

## 🌲 Hierarchical Structures

| Module         | Description                                 |
|----------------|---------------------------------------------|
| `heaps.py`     | Min/max heap operations using `heapq`       |
| `trees.py`     | Generic tree structure and traversal        |
| `bst.py`       | Binary search tree implementation           |
| `trie.py`      | Prefix tree for string matching             |

---

## 🔗 Linked Structures

| Module                  | Description                                 |
|-------------------------|---------------------------------------------|
| `linked_list.py`        | Singly linked list with basic operations    |
| `doubly_linked_list.py` | Doubly linked list with bidirectional traversal |
| `circular_list.py`      | Circular linked list for round-robin logic  |

---

## 🔍 Graph Structures

| Module             | Description                                 |
|--------------------|---------------------------------------------|
| `graphs.py`        | Graph representation using adjacency lists  |
| `graph_algorithms.py` | BFS, DFS, Dijkstra, and other algorithms |

---

## 🧬 Functional & Typed Structures

| Module             | Description                                 |
|--------------------|---------------------------------------------|
| `typing_examples.py` | Type hints and generic containers          |
| `generics.py`      | Generic classes and functions using `TypeVar` |
| `frozensets.py`    | Immutable set operations                    |

---

## 🧪 Utilities

| Module             | Description                                 |
|--------------------|---------------------------------------------|
| `test_utils.py`    | Shared test helpers and fixtures            |
| `benchmarking.py`  | Performance comparisons across structures   |

---

## 🛠️ Usage Notes

- Most modules include **doctest examples** for quick validation.
- More complex modules include **unit tests** in separate `test_*.py` files.
- Dependencies: Only standard library unless noted (e.g., NumPy, Pandas, Polars).

---

This folder is part of a larger Python portfolio project focused on clean architecture, modular design, and practical data structure implementations.



# TO DO:
core
- [x] lists.py
- [ ] dicts.py
- [ ] sets.py
- [ ] tuples.py
- [ ] namedtuples.py
- [ ] fronzesets.py

enhanced
- [ ] defaultdicts.py
- [ ] counters.py
- [ ] deque_collections.py
- [ ] enum_structures.py
- [ ] dataclasses.py

linear
- [ ] queues.py
- [ ] stacks.py
- [ ] arrays_numpy.py

tabular
- [ ] dataframes_pandas.py
- [ ] dataframers_polars.py

hieararchichal
- [ ] heaps.py
- [ ] tres.py
- [ ] binary_search_tree.py
- [ ] trie.py (prefix trees for string matching)

graph
- [ ] graphs.py
- [ ] graph_algorithms.py

linked_structures
- [ ] linked_list.py
- [ ] doubly_linked_list.py
- [ ] circular_list.py

utils
- [ ] test_utils.py
- [ ] benchmarking.py

## Specialized Methods to Include:
data_structures/
lists.py
- sort_list(lst)
- reverse_list(lst)
- slice_list(lst, start, end)
- filterlist(lst, conditionfn)
dicts.py
- get_keys(d)

- get_values(d)
- merge_dicts(d1, d2)
- invert_dict(d)
sets.py
- union_sets(s1, s2)
- intersect_sets(s1, s2)
- difference_sets(s1, s2)
dataframes_pandas.py
- loaddataframe(filepath)
- filter_dataframe(df, condition)
- group_dataframe(df, column)
- exportdataframe(df, filepath)
