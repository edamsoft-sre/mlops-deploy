from dvc import api
import pandas as pd
from io import StringIO
import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name): (message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)
import os

print(open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
logger = logging.getLogger(__name__)
logging.info('Fetching data..')

movie_data_path = api.read('movies.csv', remote='dataset-track')
financial_data_path = api.read('dataset/finantials.csv', remote='dataset-track')
opening_data_path = api.read('dataset/opening_gross.csv', remote='dataset-track')

fin_data = pd.read_csv(StringIO(financial_data_path))
movie_data = pd.read_csv(StringIO(movie_data_path))
opening_data = pd.read_csv(StringIO(opening_data_path))

numeric_columns_mask = (movie_data.dtypes == float) | (movie_data.dtypes == int)
numeric_columns = [col for col in numeric_columns_mask.index if numeric_columns_mask[col]]
movie_data = movie_data[numeric_columns+['movie_title']]

fin_data = fin_data['movie_title', 'production_budget', 'worldwide_gross']
fin_movie_data = pd.merge(fin_data, movie_data, on='movie_title', how='left')
full_movie_data = pd.merge(opening_data, fin_movie_data, on='movie_title', how='left')

full_movie_data = full_movie_data.drop(['gross', 'movie_title'], axis=1)
full_movie_data.to_csv('dataset/full_data.csv', index=False)

logger.info('Data fetched and prepared...')
