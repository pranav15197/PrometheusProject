import json


class NDJsonReader:
    def __init__(self, filename):
        self.filename = filename
        self.bad_rows = []

    def parse_rows(self):
        data = []
        with open(self.filename) as f:
            for line in f.readlines():
                try:
                    line = line[:-1]
                    data.append(json.loads(line))
                except Exception:
                    self.bad_rows.append(line)
        return data
