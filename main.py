import csv
from pathlib import Path


def main():
    input_filename = input("What is your file name/path? ")
    input_path = Path(input_filename).resolve()

    try:
        csv_rows = read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The input file '{input_filename}' could not be found.")
        return

    while True:
        has_header_input = input("Does the input file have a header (y/n)? ")

        if has_header_input.lower().strip() == "y":
            has_header = True
            break
        elif has_header_input.lower().strip() == "n":
            has_header = False
            break

    input_data_rows = len(csv_rows)

    if has_header and input_data_rows > 0:
        input_data_rows -= 1

    cleaned_rows = clean_rows(csv_rows)
    output_data_rows = len(cleaned_rows)

    if has_header and output_data_rows > 0:
        output_data_rows -= 1

    valid_filename = False
    while not valid_filename:
        output_filename = input("What would you like your output filename to be (for example: output.csv)? ")
        output_path = Path(output_filename).resolve()

        if output_path != input_path:
            if not output_path.exists():
                valid_filename = True
            else:
                while True:
                    approval = input("The file you entered already exists, are you sure you want to overwrite (y/n)? ")

                    if approval.lower().strip() == "y":
                        valid_filename = True
                        break
                    elif approval.lower().strip() == "n":
                        print("Please enter a new filename.")
                        break
                    else:
                        print("Please enter a valid answer.")
        else:
            print("Output file cannot be the same as input file.")

    write_csv(output_path, cleaned_rows)

    duplicates_removed = len(csv_rows) - len(cleaned_rows)
    print("CSV cleaning complete!")
    print(f"Data rows processed: {input_data_rows}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"Data rows written: {output_data_rows}")
    print(f"Output saved to: {output_path}")


def read_csv(input_path):
    with open(input_path, 'r', newline='', encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        return list(csv_reader)


def clean_rows(rows):
    cleaned_rows = []

    for row in rows:
        cleaned_row = []

        for value in row:
            cleaned_row.append(value.strip())

        cleaned_rows.append(cleaned_row)

    unique_rows = []

    for row in cleaned_rows:
        if row not in unique_rows:
            unique_rows.append(row)

    return unique_rows


def write_csv(output_path, rows):
    with open(output_path, 'w', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)

        csv_writer.writerows(rows)


main()