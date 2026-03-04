"""Tests for the records module."""

import pytest
from records import RecordManager, input_record


class TestRecordManager:
    """Tests for RecordManager class."""

    def test_add_record(self):
        manager = RecordManager()
        idx = manager.add_record({"name": "Alice", "age": "30", "email": "alice@example.com"})
        assert idx == 0
        assert manager.count() == 1

    def test_add_multiple_records(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice"})
        idx = manager.add_record({"name": "Bob"})
        assert idx == 1
        assert manager.count() == 2

    def test_add_record_invalid_type(self):
        manager = RecordManager()
        with pytest.raises(TypeError):
            manager.add_record("not a dict")

    def test_access_record(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice", "age": "30", "email": "alice@example.com"})
        record = manager.access_record(0)
        assert record["name"] == "Alice"
        assert record["age"] == "30"
        assert record["email"] == "alice@example.com"

    def test_access_record_out_of_range(self):
        manager = RecordManager()
        with pytest.raises(IndexError):
            manager.access_record(0)

    def test_access_record_negative_index(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice"})
        with pytest.raises(IndexError):
            manager.access_record(-1)

    def test_insert_record(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice"})
        manager.add_record({"name": "Charlie"})
        manager.insert_record(1, {"name": "Bob"})
        assert manager.count() == 3
        assert manager.access_record(0)["name"] == "Alice"
        assert manager.access_record(1)["name"] == "Bob"
        assert manager.access_record(2)["name"] == "Charlie"

    def test_insert_record_at_beginning(self):
        manager = RecordManager()
        manager.add_record({"name": "Bob"})
        manager.insert_record(0, {"name": "Alice"})
        assert manager.access_record(0)["name"] == "Alice"
        assert manager.access_record(1)["name"] == "Bob"

    def test_insert_record_at_end(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice"})
        manager.insert_record(1, {"name": "Bob"})
        assert manager.access_record(1)["name"] == "Bob"

    def test_insert_record_invalid_type(self):
        manager = RecordManager()
        with pytest.raises(TypeError):
            manager.insert_record(0, "not a dict")

    def test_insert_record_out_of_range(self):
        manager = RecordManager()
        with pytest.raises(IndexError):
            manager.insert_record(5, {"name": "Alice"})

    def test_insert_record_negative_index(self):
        manager = RecordManager()
        with pytest.raises(IndexError):
            manager.insert_record(-1, {"name": "Alice"})

    def test_all_records(self):
        manager = RecordManager()
        manager.add_record({"name": "Alice"})
        manager.add_record({"name": "Bob"})
        records = manager.all_records()
        assert len(records) == 2
        assert records[0]["name"] == "Alice"
        assert records[1]["name"] == "Bob"

    def test_all_records_empty(self):
        manager = RecordManager()
        assert manager.all_records() == []

    def test_count(self):
        manager = RecordManager()
        assert manager.count() == 0
        manager.add_record({"name": "Alice"})
        assert manager.count() == 1


class TestInputRecord:
    """Tests for input_record function."""

    def test_input_record(self, monkeypatch):
        inputs = iter(["Alice", "30", "alice@example.com"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        record = input_record()
        assert record == {"name": "Alice", "age": "30", "email": "alice@example.com"}
