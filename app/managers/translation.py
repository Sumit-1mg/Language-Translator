import asyncio

from aiohttp_client_cache import CachedSession, SQLiteBackend
from app.database.save_response import StoreTranslationResponse
from app.managers.detector import Detector
from app.models.request import TranslatorModel
from app.models.response import TranslatorResponseModel
from app.utils.dotenv_reader import google_api_key, lacto_api_key, rapid_api_key
from app.utils.constant import GOOGLE_URL, LACTO_URL, RAPID_URL
from app.utils.language_code import LanguageCodeHandler


class Translator:
    TIMEOUT = 5 # in seconds

    @classmethod
    async def translate(cls, request_data, service):

        try:
            TranslatorModel(**request_data)
        except ValueError as v:
            return {"error": 1, "error_message": str(v)}
        except Exception as e:
            return {"error": 1, "error_message": str(e)}

        ans = {'error': 0, 'source_language': request_data['source_language']}
        source_language = request_data.get("source_language").lower().strip()
        source_language_detector = Detector()
        _detected_language = source_language_detector.api_call(request_data)
        if _detected_language['error']:
            return _detected_language
        detected_language = _detected_language['detected_language']
        if detected_language.lower() != source_language:
            ans['error'] = 1
            ans['error_message'] = 'Detected Language doesnot match with Source Language'
            return ans

        language_to_code = LanguageCodeHandler()
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

            try:
                TranslatorResponseModel(**ans)
            except Exception as e:
                return {"error": 1, "error_message": str(e)}

            if status == 200:
                StoreTranslationResponse.store_translation_request(source_language, target_language, service, True)
            else:
                StoreTranslationResponse.store_translation_request(source_language, target_language, service, False)
        except asyncio.TimeoutError:
            ans['error']=1
            ans['error_message']= "Timeout Error"
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
        async with CachedSession(cache=SQLiteBackend('cache', allowed_methods=('GET', 'POST')),
                                 allowable_methods=['GET', 'POST']) as session:
            async with session.post(url=url, headers=headers, params=params, data=data, timeout=cls.TIMEOUT) as res:
                status = res.status
                content = await res.json()
                return content, status

