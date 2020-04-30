import os


class CSVCreator:

    @staticmethod
    def create(name, dataframe):
        csv_name = f'{name}.csv'
        csv_path = os.path.dirname(os.path.abspath(__file__)) + f'/{csv_name}'
        dataframe.to_csv(csv_path, index=None)
        return csv_name, csv_path
