import csv

input_filename = input("What is your file name/path? ")

with open(input_filename, 'r', newline='', encoding="utf-8") as file:
    csvreader = csv.reader(file)

    csvrows = []

    for row in csvreader:
        csvrows.append(row)

    cleaned_rows = []

    for row in csvrows:
        cleaned_row = []

        for data in row:
            cleaned_row.append(data.strip())

        cleaned_rows.append(cleaned_row)

    unique_rows = []

    for row in cleaned_rows:
        if row not in unique_rows:
            unique_rows.append(row)


output_filename = input("What would you like your output filename to be? ")

with open(output_filename, 'w', newline='', encoding="utf-8") as file:
    csvwriter = csv.writer(file)

    csvwriter.writerows(unique_rows)