import os

from .bq_creator import BigQueryClientHelper
from .csv_creator import CSVCreator
from .dataframe_creator import DFCreator
from .gcs_storage_client_helper import StorageClientHelper
from .uuid_helper import UUIDHelper


class BQFakeTableCreator:

    def __init__(self,
                 project_id,
                 bq_dataset_id=None,
                 bq_table_id=None,
                 num_rows=None,
                 num_cols=None,
                 obfuscate_col_names=None):
        self.__project_id = project_id
        self.__bq_dataset_id = bq_dataset_id
        self.__bq_table_id = bq_table_id
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__obfuscate_col_names = obfuscate_col_names

    def create(self):
        df_name, dataframe = DFCreator(self.__bq_table_id,
                                       self.__num_rows,
                                       self.__num_cols,
                                       self.__obfuscate_col_names).create()
        csv_name, csv_path = CSVCreator.create(df_name, dataframe)
        storage_helper = StorageClientHelper(project_id=self.__project_id)
        generated_id = UUIDHelper.generate_uuid()
        temp_bucket_name = f'bucket_{generated_id}'
        storage_helper.create_bucket(temp_bucket_name)
        gcs_path = storage_helper.upload_file(temp_bucket_name, csv_path, csv_name)

        bigquery_helper = BigQueryClientHelper(project_id=self.__project_id)
        dataset_id = self.__bq_dataset_id if self.__bq_dataset_id \
            else f'bq_dataset_{generated_id}'
        bigquery_helper.create_dataset(dataset_id)
        bigquery_helper.load_from_gcs(gcs_path, df_name, dataset_id)
        storage_helper.delete_bucket(temp_bucket_name)
        # Cleans up generated file.
        os.remove(csv_path)
