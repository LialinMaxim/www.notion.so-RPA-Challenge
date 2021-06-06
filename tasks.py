import os
import json
from time import sleep

import requests
import pandas as pd
import fitz


class SiteParser:
    HOME_URL = 'https://itdashboard.gov'
    BASE_API_URL = f'{HOME_URL}/api/v1/ITDB2'

    def __init__(self, output_file='itdashboard_gov', folder='output', sleep_seconds=0.7, reload_files=False,
                 agencies_list=None, pdf_columns=None, pdf_page=0,
                 index_rows=False, sort_agency_columns=None, sort_investments_columns=None):
        self.session = requests.session()
        self.output_file = output_file
        self.reload_files = reload_files
        self.index = index_rows
        self.sleep = sleep_seconds
        self.agencies_list = agencies_list or tuple()
        self.pdf_columns = pdf_columns
        self.pdf_page = pdf_page
        self.agency_columns = sort_agency_columns
        self.investments_columns = sort_investments_columns
        self.output_folder = os.path.join(folder)
        self._json_folder = os.path.join(folder, 'json')
        self._pdf_folder = os.path.join(folder, 'pdf')
        self._token = None

    def get_agencies(self) -> list:
        self.session.headers.update({'Referer': f'{self.HOME_URL}/drupal/'})
        data = self._load_json(f'{self.BASE_API_URL}/visualization/govwide/agencyTiles')
        return data.get('result', [])

    def get_agency(self, code) -> list:
        self.session.headers.update({'Referer': f'{self.HOME_URL}/drupal/summary/{code}'})
        data = self._load_json(
            f'{self.BASE_API_URL}/visualization/agency/investmentsTable/agencyCode/{code}?full=1'
        )
        return data.get('result', [])

    def get_pdf_values(self, code, uii, sep=': ') -> dict:
        columns = dict()
        if not self.pdf_columns:
            return columns
        self.session.headers.update({'Referer': f'{self.HOME_URL}/drupal/summary/{code}/{uii}'})
        file_path = self._load_pdf(url=f'{self.BASE_API_URL}/businesscase/pdf/generate/uii/{uii}')

        pdf = fitz.Document(file_path)
        pdf_page = pdf.load_page(self.pdf_page)
        for line in pdf_page.getText().split('\n'):
            if sep in line:
                d = line.split(sep)
                if len(d) == 2:
                    k, v = d
                    if k in self.pdf_columns:
                        columns[self.pdf_columns[k]] = v
        return columns

    def _set_up(self, folder=None):
        if not self._token:
            # load cookies to session
            self._token = self.get_request(f'{self.HOME_URL}/').headers
        if folder and not os.path.exists(folder):
            os.makedirs(folder)  # create folder

    def _load_json(self, url):
        file_name = '_'.join(url.split('?')[0].split('/')[-4:])
        file_path = os.path.join(self._json_folder, f'{file_name}.json')
        print(file_path)
        if self.reload_files or not os.path.isfile(file_path):
            self._set_up(self._json_folder)
            data = self.get_request(url).json()
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)
        else:
            with open(file_path, 'r') as f:
                data = json.load(f)
        return data

    def _load_pdf(self, url) -> str:
        file_name = '_'.join(url.split('?')[0].split('/')[-3:])
        file_path = os.path.join(self._pdf_folder, f'{file_name}.pdf')
        print(file_path)
        if self.reload_files or not os.path.isfile(file_path):
            self._set_up(self._pdf_folder)
            with open(file_path, 'wb') as f:
                f.write(
                    self.get_request(url).content
                )
        return file_path

    def get_request(self, url):
        sleep(self.sleep)
        r = self.session.get(url)
        print({"status_code": r.status_code, 'url': r.url})
        if r.status_code != 200:
            raise ValueError('Status code is not 200 ok')
        return r

    def __call__(self, *args, **kwargs):
        self._set_up(self.output_folder)
        file_path = os.path.join(self.output_folder, f'{self.output_file}.xlsx')
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            agencies = self.get_agencies()
            df = pd.DataFrame(agencies)
            df.to_excel(writer, sheet_name="agencies", index=self.index, columns=self.agency_columns)
            for agency in self.get_agencies():
                if (not self.agencies_list) or (agency['agencyCode'] in self.agencies_list):
                    investments = self.get_agency(agency['agencyCode'])
                    for i in investments:
                        if i.get('businessCaseId') and i.get('numberOfProjects'):
                            i.update(
                                self.get_pdf_values(code=i['agencyCode'], uii=i['UII'])
                            )
                    df = pd.DataFrame(investments)
                    print({'agencyCode': agency['agencyCode'], 'data': df.shape}, '\n')
                    df.to_excel(
                        writer,
                        sheet_name=f"{agency['agencyCode']}_{agency['agencyName']}".replace(' ', '_')[:30],
                        index=self.index,
                        columns=self.investments_columns
                    )


main = SiteParser(
    output_file='itdashboard_gov_part',
    agencies_list=['007', '012', '422'],
    pdf_columns={
        '1. Name of this Investment': 'PDF Investment',
        '2. Unique Investment Identifier (UII)': 'PDF UII'
    }
)

if __name__ == '__main__':
    main()
