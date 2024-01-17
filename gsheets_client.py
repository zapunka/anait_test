from googleapiclient import discovery
from google_auth_httplib2 import AuthorizedHttp
from google.oauth2 import service_account
import json
from typing import List


DISCOVERY_SERVICE_URL = "https://sheets.googleapis.com/$discovery/rest?version=v4"
SCOPES = (
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
)


class GSheets:
    def __init__(self, creds_json_file: str = None, creds_account_info: str = None):
        credentials = None
        if creds_account_info:
            creds_json = json.loads(creds_account_info)
            credentials = service_account.Credentials.from_service_account_info(
                creds_json, scopes=SCOPES
            )
        elif creds_json_file:
            credentials = service_account.Credentials.from_service_account_file(
                creds_json_file, scopes=SCOPES
            )
        http = AuthorizedHttp(credentials)
        self.service = discovery.build(
            "sheets", "v4", http=http, discoveryServiceUrl=DISCOVERY_SERVICE_URL
        )

    def clear_sheet(self, spreadsheet_id: str, clear_range: str):
        """
        Очистить заданный диапазон
        :param spreadsheet_id: id таблицы
        :param clear_range: диапазон для очистки вида "Лист2!H1"
        """
        self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=clear_range,
            body={}
        ).execute()

    def insert_to_sheet(self, spreadsheet_id: str, insert_range: str, data: List):
        """
        Args:
            data: данные для вставки вида
            [
                ["Azzrael Code", "YouTube Channel"], # строка
                ["check it",       "RIGHT NOW !!!"], # строка
            ]
            spreadsheet_id: id документа
            insert_range: диапазон для вставки вида "Лист2!H1"
        """

        body = {"values": data}

        self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=insert_range,
            valueInputOption="RAW",
            body=body,
        ).execute()
