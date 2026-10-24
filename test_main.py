import unittest
from main import read_csv, clean_rows, write_csv
import tempfile
import csv
from pathlib import Path


class TestRowCleaning(unittest.TestCase):

    def test_duplicate_removal(self):
        test_input = [
            ["Alice", "25"],
            ["Bob", "30"],
            ["Alice", "25"],
        ]
        
        test_output = [
            ["Alice", "25"],
            ["Bob", "30"],
        ]
        self.assertEqual(clean_rows(test_input), test_output)

    def test_whitespace_removal(self):
        test_input = [
            [" Alice ", "25"],
            ["Bob", "30 "],
        ]
        
        test_output = [
            ["Alice", "25"],
            ["Bob", "30"],
        ]
        self.assertEqual(clean_rows(test_input), test_output)

    def test_empty_input(self):
        self.assertEqual(clean_rows([]), [])

    def test_no_duplicates(self):
        test_input = [
            [" Alice ", "25"],
            ["Bob", "30"],
        ]

        test_output = [
            ["Alice", "25"],
            ["Bob", "30"],
        ]

        self.assertEqual(clean_rows(test_input), test_output)

    def test_empty_cells(self):
        self.assertEqual(clean_rows([["", " "]]), [["", ""]])


class TestReadCSV(unittest.TestCase):

    def test_read_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_data.csv"

            rows = [
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            with open(file_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            self.assertEqual(read_csv(file_path), rows)

    def test_read_empty_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_data.csv"

            with open(file_path, 'w', newline='', encoding="utf-8") as file:
                pass

            self.assertEqual(read_csv(file_path), [])

    def test_read_missing_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "does_not_exist.csv"

            with self.assertRaises(FileNotFoundError):
                read_csv(file_path)


class TestWriteCSV(unittest.TestCase):

    def test_write_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            write_csv(file_path, rows)

            self.assertEqual(read_csv(file_path), rows)

    def test_write_csv_with_commas(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Smith, John", "50"],
            ]

            write_csv(file_path, rows)

            self.assertEqual(read_csv(file_path), rows)


if __name__ == '__main__':
    unittest.main()