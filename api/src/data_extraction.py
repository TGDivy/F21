import pandas as pd


class DataExtraction:
    def __init__(self, source, request):
        self._database = None
        self._request = request
        self._source = source

    def read_csv(self):
        self._database = pd.read_csv(self._source)

    def look_up_column(self, label_index):
        return (self._database.loc[:, label_index]).dropna()

    def run(self):
        self.read_csv()
        return self.look_up_column(self._request).to_numpy().tolist()


def main():
    lookup = DataExtraction(
        "./data/2022-09-city-of-london-outcomes.csv", ["Longitude", "Latitude"]
    )
    print(lookup.run())


if __name__ == "__main__":
    main()
