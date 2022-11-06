import pandas as pd


class UKPoliceData:
    def __init__(self, path_dir):
        self.path_dir = path_dir

        # find the files from 2019 to 2022
        database = self._read_csv()
        self._database = self.clean_data(database)

    def _read_csv(self, year_range=(2022, 2023)):
        database = pd.DataFrame()
        for year in range(*year_range):
            for month in range(1, 13):
                if month < 10:
                    month = "0" + str(month)
                else:
                    month = str(month)
                for police_department in ["city-of-london", "metropolitan"]:
                    try:
                        database = pd.concat(
                            [
                                database,
                                pd.read_csv(
                                    f"{self.path_dir}/{year}-{month}/{year}-{month}-{police_department}-outcomes.csv"
                                ),
                            ]
                        )

                    except FileNotFoundError as e:
                        print(e)

        return database

    def clean_data(self, df):

        # drop missing values
        df = df.dropna()

        # drop rows when Outcome type is not "Investigation complete; no suspect identified"
        df = df[df["Outcome type"] != "Investigation complete; no suspect identified"]

        return df

    def get_data(self):
        return self._database

    def get_crime_types(self):
        return self._database["Outcome type"].unique()


class UKPoliceGetData:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.file_name = "uk_police_data.csv"

    def get_data(self):
        return pd.read_csv(f"{self.path_dir}/{self.file_name}")

    def get_crime_types(self):
        return pd.read_csv(f"{self.path_dir}/{self.file_name}")["Outcome type"].unique()


if __name__ == "__main__":
    uk_police_data = UKPoliceData("data/uk_police_data")
    df = uk_police_data.get_data()

    df.to_csv("data/uk_police_data/uk_police_data.csv")

    print(df.head())
    # print(uk_police_data.get_crime_types())
