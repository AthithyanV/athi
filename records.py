"""Record management module with add, access, and insert functionality."""


class RecordManager:
    """Manages a collection of records with add, access, and insert operations."""

    def __init__(self):
        self._records = []

    def add_record(self, record):
        """Add a record to the end of the collection.

        Args:
            record: A dictionary representing the record to add.

        Returns:
            The index of the newly added record.

        Raises:
            TypeError: If record is not a dictionary.
        """
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")
        self._records.append(record)
        return len(self._records) - 1

    def access_record(self, index):
        """Access a record by its index.

        Args:
            index: The index of the record to access.

        Returns:
            The record at the given index.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._records):
            raise IndexError(f"Record index {index} out of range")
        return self._records[index]

    def insert_record(self, index, record):
        """Insert a record at a specific position.

        Args:
            index: The position at which to insert the record.
            record: A dictionary representing the record to insert.

        Raises:
            TypeError: If record is not a dictionary.
            IndexError: If the index is out of range.
        """
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")
        if index < 0 or index > len(self._records):
            raise IndexError(f"Insert index {index} out of range")
        self._records.insert(index, record)

    def all_records(self):
        """Return a list of all records.

        Returns:
            A list of all records.
        """
        return list(self._records)

    def count(self):
        """Return the number of records.

        Returns:
            The number of records in the collection.
        """
        return len(self._records)


def input_record():
    """Prompt the user for record fields and return a record dictionary.

    Returns:
        A dictionary with 'name', 'age', and 'email' fields.
    """
    name = input("Enter name: ")
    age = input("Enter age: ")
    email = input("Enter email: ")
    return {"name": name, "age": age, "email": email}


def main():
    """Interactive loop for managing records."""
    manager = RecordManager()

    while True:
        print("\n--- Record Manager ---")
        print("1. Add record")
        print("2. Insert record at position")
        print("3. Access record by index")
        print("4. View all records")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            record = input_record()
            idx = manager.add_record(record)
            print(f"Record added at index {idx}.")
        elif choice == "2":
            try:
                pos = int(input("Enter position to insert at: "))
                record = input_record()
                manager.insert_record(pos, record)
                print(f"Record inserted at position {pos}.")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                idx = int(input("Enter index: "))
                record = manager.access_record(idx)
                print(f"Record: {record}")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
        elif choice == "4":
            records = manager.all_records()
            if records:
                for i, rec in enumerate(records):
                    print(f"  [{i}] {rec}")
            else:
                print("No records.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
