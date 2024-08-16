import csv


def read_line_from_txt_file(file_location):
    with open(file_location, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                yield line


def read_from_csv(file_location):
    try:
        with open(file_location, mode='r', newline='', encoding='utf-8') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, dialect=dialect)
            for row in reader:
                yield row
    except Exception as e:
        return e


def write_to_csv(data: list[dict], file_location: str):
    fieldnames = ['id', 'title', 'amount', 'currency', 'kind', 'category', 'date']
    try:
        with open(file_location, mode='r', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()

            for item in data:
                writer.writerow({
                    'id': item['id'],
                    'title': item['title'],
                    'amount': item['amount'],
                    'currency': item['currency'],
                    'kind': item['kind'],
                    'category': item['category'],
                    'date': item['date']
                })
    except Exception as e:
        return e
