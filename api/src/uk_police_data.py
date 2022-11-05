import pandas as pd


class DataExtraction:
    def __init__(self, path_dir):
        self.path_dir = path_dir

        # find the files from 2019 to 2022
        self._database = self.read_csv()

    def read_csv(self):
        self._database = pd.read_csv(self._source)

    def look_up_column(self, label_index):
        return (self._database.loc[:, label_index]).dropna()

    def run(self):
        self.read_csv()
        return self.look_up_column(self._request).to_numpy().tolist()
