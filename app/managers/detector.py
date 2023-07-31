import requests
from pydantic import ValidationError
from sanic import json

from app.models.request import DetectorModel
from app.utils.dotenv_reader import google_api_key
from app.utils.constant import GOOGLE_URL
from app.utils.language_code import LanguageCodeHandler


class Detector:

    def __init__(self):
        pass

    def api_call(self, request_data):

        try:
            DetectorModel(**request_data)
        except ValidationError as e:
            return {"error": 1, "error_message": str(e)}

        ans = {'error': 0}
        try:
            url = GOOGLE_URL + '/detect'
            params = {
                "q": request_data.get('source_text'),
                "key": google_api_key,
            }
            response = requests.post(url, params=params)
            response = response.json()

            code_to_language = LanguageCodeHandler()
            code = response.get('data').get('detections')[0][0].get('language')
            ans['detected_language'] = code_to_language.get_language(code)


        except Exception as e:
            ans['error'] = 1
            ans['error_message'] = e
        return ans
