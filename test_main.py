import unittest
from main import read_csv, clean_rows, write_csv, main
import tempfile
import csv
from pathlib import Path
from unittest.mock import patch


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

            with open(file_path, 'w', newline='', encoding="utf-8"):
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


class TestMain(unittest.TestCase):

    def test_missing_input_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.csv"

            with patch("builtins.input", return_value=str(file_path)) as user_input:
                with patch("builtins.print") as mock_print:
                    main()

                    user_input.assert_called_once_with("What is your file name/path? ")
                    mock_print.assert_called_once_with(f"Error: The input file '{file_path}' could not be found.")

    def test_successful_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25 "],
                [" Bob", "30"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(output_path)]):
                with patch("builtins.print") as mock_print:
                    main()

            self.assertTrue(output_path.exists())
            self.assertEqual(read_csv(output_path), expected_output)
            mock_print.assert_any_call("CSV cleaning complete!")
            mock_print.assert_any_call(f"Data rows processed: 3")
            mock_print.assert_any_call(f"Duplicate rows removed: 1")
            mock_print.assert_any_call(f"Data rows written: 2")
            mock_print.assert_any_call(f"Output saved to: {output_path.resolve()}")

    def test_invalid_header_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with patch("builtins.input", side_effect=[str(input_path), "maybe", "Y ", str(output_path)]) as mock_input:
                with patch("builtins.print") as mock_print:
                    main()

            self.assertEqual(mock_input.call_count, 4)
            mock_print.assert_any_call("Please enter a valid answer.")
            self.assertEqual(read_csv(output_path), expected_output)

    def test_decline_overwrite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"
            existing_output_path = Path(temp_dir) / "existing_output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25 "],
                [" Bob", "30"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            existing_data = [
                ["Old data."]
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with open(existing_output_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(existing_data)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(existing_output_path), "n", str(output_path)]) as mock_input:
                main()

            self.assertEqual(mock_input.call_count, 5)
            self.assertEqual(read_csv(existing_output_path), existing_data)
            self.assertEqual(read_csv(output_path), expected_output)

    def test_approve_overwrite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            existing_output_path = Path(temp_dir) / "existing_output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25 "],
                [" Bob", "30"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            existing_data = [
                ["Old data."]
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with open(existing_output_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(existing_data)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(existing_output_path), "y"]) as mock_input:
                main()

            self.assertEqual(mock_input.call_count, 4)
            self.assertEqual(read_csv(existing_output_path), expected_output)

    def test_invalid_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            existing_output_path = Path(temp_dir) / "existing_output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25 "],
                [" Bob", "30"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
                ["Bob", "30"],
            ]

            existing_data = [
                ["Old data."]
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with open(existing_output_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(existing_data)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(existing_output_path), "maybe", "y"]) as mock_input:
                with patch("builtins.print") as mock_print:
                    main()

            self.assertEqual(mock_input.call_count, 5)
            mock_print.assert_any_call("Please enter a valid answer.")
            self.assertEqual(read_csv(existing_output_path), expected_output)

    def test_same_input_output_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Name", "Age"],
                ["Alice", "25"],
            ]

            expected_output = [
                ["Name", "Age"],
                ["Alice", "25"],
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(input_path), str(output_path)]) as mock_input:
                with patch("builtins.print") as mock_print:
                    main()

            self.assertEqual(mock_input.call_count, 4)
            mock_print.assert_any_call("Output file cannot be the same as input file.")
            self.assertEqual(read_csv(output_path), expected_output)
            self.assertEqual(read_csv(input_path), rows)

    def test_header_only_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"

            rows = [
                ["Name ", "Age"],
            ]

            expected_output = [
                ["Name", "Age"],
            ]

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            with patch("builtins.input", side_effect=[str(input_path), "y", str(output_path)]):
                with patch("builtins.print") as mock_print:
                    main()

            self.assertTrue(output_path.exists())
            self.assertEqual(read_csv(output_path), expected_output)
            mock_print.assert_any_call("CSV cleaning complete!")
            mock_print.assert_any_call(f"Data rows processed: 0")
            mock_print.assert_any_call(f"Duplicate rows removed: 0")
            mock_print.assert_any_call(f"Data rows written: 0")
            mock_print.assert_any_call(f"Output saved to: {output_path.resolve()}")

    def test_empty_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            output_path = Path(temp_dir) / "output.csv"

            with open(input_path, 'w', newline='', encoding="utf-8") as file:
                pass

            with patch("builtins.input", side_effect=[str(input_path), "y", str(output_path)]):
                with patch("builtins.print") as mock_print:
                    main()

            self.assertTrue(output_path.exists())
            self.assertEqual(read_csv(output_path), [])
            mock_print.assert_any_call("CSV cleaning complete!")
            mock_print.assert_any_call(f"Data rows processed: 0")
            mock_print.assert_any_call(f"Duplicate rows removed: 0")
            mock_print.assert_any_call(f"Data rows written: 0")
            mock_print.assert_any_call(f"Output saved to: {output_path.resolve()}")


if __name__ == '__main__':
    unittest.main()