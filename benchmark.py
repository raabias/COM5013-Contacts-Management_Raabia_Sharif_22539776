
"""Measure performance of the Contacts Management Application."""

import random
import time

from contacts_app import Contact, ContactManager

SIZES = [1_000, 10_000, 100_000]
REPEATS = 3


def best_of(func, repeats=REPEATS):
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        func()
        best = min(best, time.perf_counter() - start)
    return best


def build(n, rng):
    manager = ContactManager()
    for i in range(n):
        manager.add(
            Contact(
                f"Person {rng.random()}",
                "123",
                f"p{i}@example.com"
            )
        )
    return manager


def main():
    rng = random.Random(42)

    print(
        f"{'n':>9} | {'merge sort (s)':>14} | {'sorted() (s)':>12} | "
        f"{'name search (ms)':>16} | {'email lookup (us)':>17}"
    )
    print("-" * 82)

    for n in SIZES:
        manager = build(n, rng)
        items = list(manager.contacts.values())

        key = lambda contact: (contact.name.casefold(), contact.email)

        t_merge = best_of(
            lambda: ContactManager.merge_sort(items)
        )
        t_builtin = best_of(
            lambda: sorted(items, key=key)
        )
        t_search = best_of(
            lambda: manager.find_by_name("zzz-no-match")
        )

        target = f"p{n // 2}@example.com"
        loops = 10_000

        t_lookup = best_of(
            lambda: [
                manager.find_by_email(target)
                for _ in range(loops)
            ]
        ) / loops

        print(
            f"{n:>9,} | {t_merge:>14.4f} | {t_builtin:>12.4f} | "
            f"{t_search * 1000:>16.3f} | {t_lookup * 1e6:>17.3f}"
        )


if __name__ == "__main__":
    main()
