import logging

from google.cloud import bigquery
from google.api_core.exceptions import Conflict


class BigQueryClientHelper:

    def __init__(self, project_id):
        self.__cloud_client = bigquery.Client(project=project_id)
        self.__project_id = project_id

    def create_dataset(self, dataset_id, description=None):
        name = f'{self.__project_id}.{dataset_id}'
        logging.info(f'--> Creating Dataset "{name}"...')

        dataset = bigquery.Dataset(name)
        dataset.description = description if description \
            else 'Dataset containing tables with fake data'
        dataset.location = 'US'

        try:
            return self.__cloud_client.create_dataset(dataset)
        except Conflict:
            logging.info(f'Dataset {dataset_id} already exists!')

    def load_from_gcs(self, gcs_path, table_id, dataset_id):
        dataset_ref = self.__cloud_client.dataset(dataset_id)
        job_config = bigquery.LoadJobConfig()

        job_config.skip_leading_rows = 1
        # The source format defaults to CSV, so the line below is optional.
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.autodetect = True
        uri = gcs_path

        load_job = self.__cloud_client.load_table_from_uri(
            uri, dataset_ref.table(table_id), job_config=job_config
        )  # API request
        logging.info(f'Starting job {load_job.job_id}')

        load_job.result()  # Waits for table load to complete.
        logging.info('Job finished.')

        destination_table = self.__cloud_client.get_table(dataset_ref.table(table_id))
        logging.info(f'Loaded {destination_table.num_rows} rows.')
