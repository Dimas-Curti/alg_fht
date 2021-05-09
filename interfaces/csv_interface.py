import csv
import os

class CsvInterface:
    def __init__(self):
        self.writer = None

        if not os.path.exists('db/csv'):
            os.mkdir('db/csv')

    def write(self, file_name):
        file = open('db/csv/' + file_name, mode='a+')
        self.writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
