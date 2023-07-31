import aiohttp
from pydantic import ValidationError
from sanic.response import json
import requests
from requests_cache import CachedSession

from app.database.database_management import StoreTranslationRequest
from app.models.request import TranslatorModel
from app.models.response import TranslatorResponseModel
from app.utils.dotenv_reader import google_api_key, lacto_api_key, rapid_api_key
from app.utils.constant import GOOGLE_URL, LACTO_URL, RAPID_URL
from app.utils.language_code import LanguageCodeHandler
from app.utils.input_validator import InputValidator


class Translator:
    TIMEOUT = 5  # in seconds

    @classmethod
    async def translate(cls, request_data, service):

        try:
            TranslatorModel(**request_data)
        except Exception as e:
            return {"error": 1, "error_message": str(e)}

        print(request_data)

        validate = InputValidator()
        validation_response = validate.validate(request_data)
        if validation_response['error']:
            return validation_response

        language_to_code = LanguageCodeHandler()
        ans = {'error': 0, 'source_language': request_data.get('source_language')}

        source_language = language_to_code.get_code(request_data.get('source_language'))
        target_language = language_to_code.get_code(request_data.get('target_language'))
        text = request_data.get('source_text')

        try:
            if service == "google":
                response, status = await cls.translate_with_google(src_text=text, target_lang=target_language)
                ans['target_text'] = response['data']['translations'][0]['translatedText']

            elif service == 'lacto':
                response, status = await cls.translate_with_lacto(src_text=text, src_lang=source_language,
                                                                  target_lang=target_language)
                ans['target_text'] = response.get('translations')[0].get('translated')[0]

            else:
                response, status = await cls.translate_with_rapid(src_text=text, src_lang=source_language,
                                                                  target_lang=target_language)
                ans['target_text'] = response.get('data').get('translatedText')

            if status == 200:
                StoreTranslationRequest.store_translation_request(source_language, target_language, service, True)
            else:
                StoreTranslationRequest.store_translation_request(source_language, target_language, service, False)

        except:
            ans['error'] = 1
            ans['error_message'] = 'Cannot able to translate'

        return ans

    @classmethod
    async def translate_with_google(cls, src_text, target_lang):
        params = {
            "q": src_text,
            "target": target_lang,
            "key": google_api_key,
        }
        result = await cls._make_post(url=GOOGLE_URL, params=params)
        return result

    @classmethod
    async def translate_with_lacto(cls, src_text, target_lang, src_lang):
        headers = {
            'X-API-Key': lacto_api_key,
            'Content-Type': 'json',
            'Accept': 'json'
        }
        data = {
            'texts': [src_text],
            "to": [target_lang],
            "from": src_lang
        }
        result = await cls._make_post(url=LACTO_URL, headers=headers, data=data)
        return result

    @classmethod
    async def translate_with_rapid(cls, src_text, target_lang, src_lang):
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }
        data = {
            "source_language": src_lang,
            "target_language": target_lang,
            "text": src_text
        }
        result = await cls._make_post(url=RAPID_URL, headers=headers, data=data)
        return result

    @classmethod
    async def _make_post(cls, url, data=None, params=None, headers=None):
        timeout = aiohttp.ClientTimeout(total=cls.TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url=url, headers=headers, data=data, params=params) as res:
                status = res.status
                content = await res.json()
                return content, status
