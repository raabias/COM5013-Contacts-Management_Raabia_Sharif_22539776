"""Contacts manager demonstrating hashing and merge sort."""
from dataclasses import dataclass
import re


@dataclass
class Contact:
    name: str
    phone: str
    email: str
    address: str = ""


class ContactManager:
    def __init__(self):
        self.contacts = {}  # email -> Contact

    def add(self, contact):
        key = contact.email.strip().lower()
        if not key or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", key):
            raise ValueError("Enter a valid email address")
        if not contact.name.strip() or not contact.phone.strip():
            raise ValueError("Name and phone are required")
        if key in self.contacts:
            raise ValueError("Email already exists")
        contact.email = key
        self.contacts[key] = contact

    def find_by_email(self, email):
        return self.contacts.get(email.strip().lower())

    def find_by_name(self, text):
        query = text.casefold().strip()
        return [c for c in self.contacts.values() if query in c.name.casefold()]

    def update(self, email, name=None, phone=None, address=None):
        contact = self.find_by_email(email)
        if contact is None:
            return False
        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            contact.name = name.strip()
        if phone is not None:
            if not phone.strip():
                raise ValueError("Phone cannot be empty")
            contact.phone = phone.strip()
        if address is not None:
            contact.address = address.strip()
        return True

    def delete(self, email):
        return self.contacts.pop(email.strip().lower(), None) is not None

    @staticmethod
    def merge_sort(items):
        if len(items) <= 1:
            return items
        mid = len(items) // 2
        left = ContactManager.merge_sort(items[:mid])
        right = ContactManager.merge_sort(items[mid:])
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if (left[i].name.casefold(), left[i].email) <= (right[j].name.casefold(), right[j].email):
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:]); result.extend(right[j:])
        return result

    def sorted_contacts(self):
        return self.merge_sort(list(self.contacts.values()))


def show(contacts):
    if not contacts:
        print("No matching contacts.")
    for c in contacts:
        print(f"Name: {c.name} | Phone: {c.phone} | Email: {c.email} | Address: {c.address}")


def main():
    manager = ContactManager()
    while True:
        print("\n1 Add  2 Search email  3 Search name  4 Update  5 Delete  6 List sorted  7 Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                manager.add(Contact(input("Name: ").strip(), input("Phone: ").strip(), input("Email: ").strip(), input("Address: ").strip()))
                print("Added.")
            elif choice == "2":
                result = manager.find_by_email(input("Email: "))
                show([result] if result else [])
            elif choice == "3":
                show(manager.find_by_name(input("Name contains: ")))
            elif choice == "4":
                email = input("Existing email: ")
                if manager.find_by_email(email) is None:
                    print("Not found.")
                else:
                    name = input("New name (blank to keep): ").strip()
                    phone = input("New phone (blank to keep): ").strip()
                    address = input("New address (blank to keep): ").strip()
                    manager.update(email, name=name or None, phone=phone or None, address=address or None)
                    print("Updated.")
            elif choice == "5":
                print("Deleted." if manager.delete(input("Email: ")) else "Not found.")
            elif choice == "6":
                show(manager.sorted_contacts())
            elif choice == "7":
                break
            else:
                print("Choose a number from 1 to 7.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
