import os
import json


class JsonInterface:
    def __init__(self):
        self.writer = None
        self.json_folder = 'db/json/'

        if not os.path.exists(self.json_folder):
            os.mkdir(self.json_folder)

    def write(self, file_name, sign_to_write):
        file = open(self.json_folder + file_name, mode='a+')
        json.dump(sign_to_write, file)

    def read(self, file_name):
        with open(self.json_folder + file_name, mode='r+') as file:
            current_json = json.load(file)

            content = {
                "beautified": current_json,
                "to_backend": (current_json["header_signature"], current_json["trailer_signature"])
            }

            return content

