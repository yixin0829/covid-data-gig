# This script will be further developed to fetch up-to-date data that is needed
# to run on all the notebooks to yield final processed data.
import requests
import os
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

# create directory if not exist
Path('./COVID_NET').mkdir(parents=False, exist_ok=True)


# all the download links we need to download up-to-date datasets that were used
covid_addition_hos_csv_url = 'https://gis.cdc.gov/5a427768-588f-4c77-bb37-cf5256840301/COVID19Phase5Data.zip'
covid_hos_csv_url = 'https://gis.cdc.gov/6605e289-427b-48c4-b517-986ddcd80711'


# fetch zipped csv file and upzip
resp = urlopen(covid_addition_hos_csv_url)
zipfile = ZipFile(ByteIO(resp.read()))
for line in zipfile.open(file).readlines():
    print(line.decode('utf-8'))