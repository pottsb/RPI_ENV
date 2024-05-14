from influxdb_client import InfluxDBClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class InfluxDBManager:
    def __init__(self, url, token, org):
        self.url = url
        self.token = token
        self.org = org
        self.client = None

    def initialize_client(self):
        """
        Initialize and return an InfluxDB client instance.
        
        Parameters:
            url (str): URL of the InfluxDB server.
            token (str): Authentication token for InfluxDB.
            org (str): Organization name for InfluxDB.
        
        Returns:
            InfluxDBClient: An initialized InfluxDB client object if successful, None otherwise.
        """
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
            logging.info("InfluxDB client initialized successfully.")
            return self.client
        except Exception as e:
            logging.error("Failed to initialize InfluxDB client: %s", e)
            return None

    def write_data(self, target_bucket, points):
        """
        Write data points to an InfluxDB bucket using the provided client.
        
        Parameters:
            client (InfluxDBClient): The InfluxDB client to use for writing data.
            bucket (str): The name of the bucket to write the data into.
            points (list[Point]): A list of InfluxDB Point objects to write.
            
        Returns:
            None: Function only logs success or failure of the write operation.
        """
        if self.client is None:
            logging.error("No valid InfluxDB client available. Data not written.")
            return False
        try:
            with self.client.write_api() as write_api:
                write_api.write(bucket=target_bucket, record=points)
                logging.info("Successfully wrote data to InfluxDB.")
            return True
        except Exception as e:
            logging.error("Failed to write data to InfluxDB: %s", e)
            return False
    
    def close(self):
        if self.client:
            self.client.close()
