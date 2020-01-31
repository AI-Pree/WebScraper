#! python
# Data parser for json file

import json

class ParseJson():
    def __init__(self, filename):
        self.filename = filename

    @property
    def dataFile(self):
        return self.filename

    @dataFile.setter
    def dataFile(self, value):
        self.filename = value
    
    def get_data(self):
        with open(self.filename, 'rb') as output:
            return json.load(output)
    