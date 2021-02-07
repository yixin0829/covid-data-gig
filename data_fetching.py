# This script will be further developed to fetch up-to-date data that is needed
# to run on all the notebooks to yield final processed data.
import requests
from requests.exceptions import HTTPError
import os
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

# create directory if not exist
Path('./COVID_NET').mkdir(parents=False, exist_ok=True)

# all the download links we need to download up-to-date datasets that were used
covid_addition_hosp_csv_url = 'https://gis.cdc.gov/9f1dfdb1-e4fc-4c84-b67b-7062dafaf348'
covid_hosp_csv_url = 'https://gis.cdc.gov/6605e289-427b-48c4-b517-986ddcd80711'
population_est = 'https://www2.census.gov/programs-surveys/popest/tables/2010-2020/state/totals/nst-est2020.xlsx'
who_covid_data = 'https://storage.googleapis.com/kaggle-data-sets/494724/1862179/compressed/covid_19_data.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20210207%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20210207T201006Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=3a01187e702df3db13061a03b10771a25868cbc24dd9e6683f09e4922480188cd5606c2023eab2872ede41e165c37a878153b76ce330056835c0b326702b3d6b0ca33a2fd70963eed01a5fcf7e46c40a4144c1f9bafea7cb8d24823a6c4955661666396d50dd717c07beab10353f8c5d0d9fee9a07709c3f2c80af522e7d3ce419dcb9d2205d0246b7f244bb4f37120b752f0cf1b253ffcfed424d4973b780a76b3f82e4257d73108cb7bf5eec560c47a1c21b7c0e5398fe7ab369bc78b4bd3bffa3fd41d00a787917bafa3e9d562a99867c27cee52045aca9e698251380f523c7ebc0db26ad8423875a18d2347944f246c4e2fc7a88ab884dea9c48be93982a'


# utility function for fetching single file from url
def fetch_data(url, path):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        with open(path, 'wb') as f:
            f.write(resp.content)
        print('Successfully download files from url.')


# fetch zipped csv files and upzip
def fetch_zip(url, path):
    resp = requests.get(url)
    zipfile = ZipFile(BytesIO(resp.content))
    # get file names in the .zip file 
    files = zipfile.namelist()
    for i, f in enumerate(files):
        with open(f'{path}{f}', 'wb') as csv:
            for line in zipfile.open(f).readlines():
                csv.write(line)

path = './COVID_NET/'
fetch_zip(who_covid_data, path)
fetch_data(population_est, './US_Census/nst-est2020.xlsx')
# fetch covid hospitalization data
fetch_data(covid_hosp_csv_url, './COVID_NET/COVID-19Surveillance_All_Data.csv')