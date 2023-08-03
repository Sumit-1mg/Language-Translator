from datetime import datetime, timedelta
from app.models.model import TranslationRequest


class Recommendation:

    @classmethod
    async def find_recent_requests(cls):

        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        requests = await TranslationRequest.filter(
            timestamp__gte=one_hour_ago
        ).values('api_used', 'translation_success')

        return requests

    @classmethod
    async def highest_success_api(cls):
        result = await cls.find_recent_requests()
        api_total_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}
        api_successful_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}

        for row in result:
            api = row['api_used']
            success = row['translation_success']
            if api in api_total_attempts:
                api_total_attempts[api] += 1
                if success == 1:
                    api_successful_attempts[api] += 1

        api_success_rates = {
            'google': api_successful_attempts['google'] / api_total_attempts['google'] if api_total_attempts[
                                                                                              'google'] != 0 else 0,
            'lacto': api_successful_attempts['lacto'] / api_total_attempts['lacto'] if api_total_attempts[
                                                                                           'lacto'] != 0 else 0,
            'rapid': api_successful_attempts['rapid'] / api_total_attempts['rapid'] if api_total_attempts[
                                                                                           'rapid'] != 0 else 0
        }

        highest_success_rate_api = "google"
        max_success = api_success_rates['google']

        for key, value in api_success_rates.items():
            if value > max_success:
                max_success = value
                highest_success_rate_api = key

        response = {'api': "{}".format(highest_success_rate_api.title())}
        return response


