import asyncio
from aiohttp_client_cache import CachedSession, SQLiteBackend
from app.validators.request import TranslatorModel
from app.validators.response import TranslatorResponseModel
from app.utils.dotenv_reader import google_api_key, lacto_api_key, rapid_api_key
from app.utils.constant import GOOGLE_URL, LACTO_URL, RAPID_URL
from app.utils.language_code import LanguageCodeHandler
from app.models.save_response import SaveResponse


class Translator:
    TIMEOUT = 5  # in seconds

    @classmethod
    async def translate(cls, request_data, service):
        try:
            TranslatorModel(**request_data)
        except ValueError as msg:
            return {"error": 1, "error_message": str(msg)}
        except Exception as e:
            return {"error": 1, "error_message": str(e)}

        ans = {'error': 0, 'source_language': request_data['source_language']}
        language_to_code = LanguageCodeHandler()
        source_language = language_to_code.get_code(request_data.get('source_language'))
        target_language = language_to_code.get_code(request_data.get('target_language'))
        text = request_data.get('source_text')

        try:
            translation_function = f"translate_with_{service}"
            response, status = await getattr(cls, translation_function)(src_text=text, src_lang=source_language, target_lang=target_language)
            ans['target_text'] = response

            try:
                TranslatorResponseModel(**ans)
            except Exception as e:
                return {"error": 1, "error_message": str(e)}

            #SaveResponse.save(source_language, target_language, service, int(True)) if status == 200 else SaveResponse.save(source_language, target_language, service, int(False))
            await SaveResponse.save_translation_request(source_language, target_language, service, int(True)) if status ==200 else await SaveResponse.save_translation_request(source_language, target_language, service, int(False))

        except asyncio.TimeoutError:
            ans['error'] = 1
            ans['error_message'] = "Timeout Error"
        except Exception as e:
            ans['error'] = 1
            ans['error_message'] = str(e)

        return ans

    @classmethod
    async def translate_with_google(cls, src_text,src_lang, target_lang):
        params = {
            "q": src_text,
            "target": target_lang,
            "key": google_api_key,
        }
        result,status_code = await cls._make_post(url=GOOGLE_URL, params=params)
        return result['data']['translations'][0]['translatedText'],status_code

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
        result ,status_code = await cls._make_post(url=LACTO_URL, headers=headers, data=data)
        return result.get('translations')[0].get('translated')[0],status_code

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
        result, status_code = await cls._make_post(url=RAPID_URL, headers=headers, data=data)
        return result.get('data').get('translatedText'),status_code

    @classmethod
    async def _make_post(cls, url, data=None, params=None, headers=None):
        async with CachedSession(cache=SQLiteBackend('cache', allowed_methods=('GET', 'POST')),
                                 allowable_methods=['GET', 'POST']) as session:
            async with session.post(url=url, headers=headers, params=params, data=data, timeout=cls.TIMEOUT) as res:
                status = res.status
                content = await res.json()
                return content, status
