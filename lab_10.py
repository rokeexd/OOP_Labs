import unittest
from parameterized import parameterized
from unittest.mock import Mock

# --- 1. MathTool ---
class MathTool:
    def add(self, a, b): return a + b
    def sub(self, a, b): return a - b
    def mul(self, a, b): return a * b
    def div(self, a, b):
        if b == 0: raise ValueError("Ділення на нуль")
        return a / b

# --- 2. LibraryItem ---
class LibraryItem:
    def __init__(self, title, author, year):
        self.title, self.author, self.year = title, author, year
    def details(self):
        return f"{self.title} by {self.author}, {self.year}"

# --- 3. Взаємодія класів (Mock) ---
class NotificationService:
    def send(self, message): pass # Реальний виклик API

class UserManager:
    def __init__(self, service):
        self.service = service
    def notify_user(self, msg):
        self.service.send(msg)

# --- 4. Функція для параметризованого тесту ---
def check_even(number):
    return number % 2 == 0

# --- ЮНІТ-ТЕСТИ ---
class TestLab10(unittest.TestCase):
    
    # 1. Тести для MathTool
    def test_math(self):
        m = MathTool()
        self.assertEqual(m.add(2, 3), 5)
        self.assertEqual(m.sub(5, 3), 2)
        self.assertEqual(m.mul(2, 4), 8)
        self.assertEqual(m.div(10, 2), 5)
        with self.assertRaises(ValueError):
            m.div(10, 0)

    # 2. Тести для LibraryItem
    def test_library(self):
        item = LibraryItem("Кобзар", "Шевченко", 1840)
        self.assertEqual(item.details(), "Кобзар by Шевченко, 1840")

    # 3. Тест з Mock
    def test_notify(self):
        mock_service = Mock(spec=NotificationService)
        manager = UserManager(mock_service)
        manager.notify_user("Hello!")
        mock_service.send.assert_called_once_with("Hello!")

    # 4. Параметризований тест
    @parameterized.expand([
        ("even_pos", 2, True),
        ("odd_pos", 3, False),
        ("zero", 0, True),
        ("even_neg", -2, True),
        ("odd_neg", -3, False),
    ])
    def test_check_even(self, name, val, expected):
        self.assertEqual(check_even(val), expected)

if __name__ == "__main__":
    unittest.main()
