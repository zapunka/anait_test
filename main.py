import requests
import os
from dotenv import dotenv_values

from gsheets_client import GSheets


config = {
    **dotenv_values(".env"),
    **os.environ,
}

# url для доступа к API
API_URL = "https://feedbacks-api.wb.ru/api/v1"
# количество отзывов, которое необходимо выгрузить
FEEDBACK_COUNT = 1000
# ID таблицы в Google Sheets
SPREADSHEET_ID = "1GHkqFfasuHkGA01rlqzLikqMcPv6YP2R4onLonkiO_s"
# имя листа для выгрузки данных
LIST_NAME = "feedbacks"


def get_archived_feedback():
    """
    Выгрузка архивных отзывов с WB
    :return: список выгруженных отзывов
    """
    headers = {
        'Authorization': config.get('API_KEY')
    }
    params = {
        'take': FEEDBACK_COUNT,
        'skip': 0
    }

    url = f'{API_URL}/feedbacks/archive'
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    j_resp = resp.json()
    resp_data = j_resp.get('data')
    resp_feedbacks = resp_data.get('feedbacks') if resp_data else []

    return resp_feedbacks


if __name__ == "__main__":
    feedbacks = get_archived_feedback()

    # в таблицу выводим только следующие данные: название продукта, оценка, артикул, артикул ВБ, дата написания
    result = [['название продукта', 'оценка', 'артикул', 'артикул ВБ', 'дата написания']]
    for feedback in feedbacks:
        product_details = feedback['productDetails']
        data = [product_details['productName'],
                feedback['productValuation'],
                product_details['imtId'],
                product_details['nmId'],
                feedback['createdDate']]

        result.append(data)

    sheet_client = GSheets(creds_json_file=config.get('SHEETS_CREDS_FILE'))
    list_range = f'{LIST_NAME}!A1:E'
    # предварительно очищаем лист
    sheet_client.clear_sheet(SPREADSHEET_ID, list_range)
    # сохраняем данные в google sheet
    sheet_client.insert_to_sheet(SPREADSHEET_ID, list_range, result)
