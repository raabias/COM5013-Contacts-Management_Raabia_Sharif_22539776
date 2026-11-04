import unittest
from contacts_app import Contact, ContactManager


class TestContactManager(unittest.TestCase):
    def setUp(self):
        self.m = ContactManager()

    def test_empty(self):
        self.assertEqual(self.m.sorted_contacts(), [])
        self.assertIsNone(self.m.find_by_email('none@example.com'))
        self.assertFalse(self.m.delete('none@example.com'))

    def test_add_search_case_insensitive(self):
        self.m.add(Contact('Alice', '123', 'ALICE@example.com'))
        self.assertEqual(self.m.find_by_email('alice@EXAMPLE.COM').name, 'Alice')

    def test_duplicate_rejected(self):
        self.m.add(Contact('Alice', '123', 'a@example.com'))
        with self.assertRaises(ValueError):
            self.m.add(Contact('Other', '456', 'A@example.com'))

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.m.add(Contact('Alice', '123', 'invalid'))

    def test_name_search(self):
        self.m.add(Contact('Alice Smith', '123', 'a@example.com'))
        self.assertEqual(len(self.m.find_by_name('SMITH')), 1)

    def test_update(self):
        self.m.add(Contact('Alice', '123', 'a@example.com'))
        self.assertTrue(self.m.update('a@example.com', phone='999'))
        self.assertEqual(self.m.find_by_email('a@example.com').phone, '999')

    def test_delete(self):
        self.m.add(Contact('Alice', '123', 'a@example.com'))
        self.assertTrue(self.m.delete('a@example.com'))
        self.assertIsNone(self.m.find_by_email('a@example.com'))

    def test_sort_stability(self):
        for name, email in [('Zoe', 'z@example.com'), ('amy', 'b@example.com'), ('Amy', 'a@example.com')]:
            self.m.add(Contact(name, '123', email))
        self.assertEqual([c.email for c in self.m.sorted_contacts()], ['a@example.com', 'b@example.com', 'z@example.com'])

    def test_1000_contacts(self):
        for i in range(1000):
            self.m.add(Contact(f'Person {i}', '123', f'p{i}@example.com'))
        self.assertEqual(len(self.m.sorted_contacts()), 1000)


if __name__ == '__main__':
    unittest.main()
