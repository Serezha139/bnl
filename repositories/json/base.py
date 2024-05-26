import json


class BaseJsonDAO:
    file_path = None
    def __init__(self):
        self.raw_data = json.load(open(self.file_path))
        self.data_dict = self.make_dict_from_raw_data(self.raw_data)

    def make_dict_from_raw_data(self, raw_data):
        result = []
        for row in raw_data:
            record = row['fields']
            record['id'] = row['pk']
            result.append(record)
        return result

    def get_data(self):
        return self.data_dict