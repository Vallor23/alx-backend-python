# access_nested_map

A utility function to access values in a deeply nested dictionary using a list of keys.

## 📁 File

- `utils.py` – contains the `access_nested_map` function
- `test_utils.py` – contains unit tests

## 📥 Installation

Download or clone this repository:

```bash
git clone https://github.com/your-username/access_nested_map.git
cd access_nested_map
```

No external dependencies required.

## ✅ Usage

```python
from utils import access_nested_map

nested = {"a": {"b": {"c": 42}}}
path = ["a", "b", "c"]
print(access_nested_map(nested, path))  # Output: 42
```

## ⚠️ Exceptions

Raises `KeyError` if:

- A key does not exist
- A non-dict is accessed before the path ends

Example:

```python
access_nested_map({"a": {"b": 2}}, ["a", "b", "c"])
# Raises KeyError: 'c'
```

## 🧪 Running Tests

The test file uses `unittest` and `parameterized`.

Install test dependency:

```bash
pip install parameterized
```

Run tests:

```bash
python3 -m unittest test_utils.py
```

## 🔍 Example Test Case (using parameterized)

```python
from parameterized import parameterized

@parameterized.expand([
    ({"a": {"b": {"c": 1}}}, ["a", "b", "c"], 1),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```
