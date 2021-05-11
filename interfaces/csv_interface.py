import csv
import os


class CsvInterface:
    def __init__(self):
        self.writer = None

        if not os.path.exists('db/csv'):
            os.mkdir('db/csv')

    def write(self, file_name, sign_to_write):
        file = open('db/csv/' + file_name, mode='a+')
        self.writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

        file.write('#HEADER\n')
        self.writer.writerows(sign_to_write[0])
        file.write('#TRAILER\n')
        self.writer.writerows(sign_to_write[1])
