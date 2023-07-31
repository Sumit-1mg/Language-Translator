from requests_cache import CachedSession

from app.utils.constant import GOOGLE_URL
from app.utils.dotenv_reader import google_api_key


class IsApiAvailable:

    @classmethod
    async def is_api_available(cls):
        try:
            params = {
                "q": "hello",
                "target": "hi",
                "key": google_api_key,
            }
            session = CachedSession(cache_name='cache', allowable_methods=['GET', 'POST'], expire_after=86400)
            session.post(GOOGLE_URL, params=params, timeout=5)
            return True
        except:
            return False