import os
import sqlite3


class APIRecommendation:
    path_to_database = os.getcwd() + '/database.db'

    @classmethod
    def calculate_success_rate(cls):
        try:
            api_total_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}
            api_successful_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}

            with sqlite3.connect(cls.path_to_database) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT api_used, translation_success FROM translation_requests WHERE timestamp >= DATETIME('now', '-1 hour')
                    '''
                )
                result=cursor.fetchall()
                conn.commit()

            for row in result:
                api, success = row
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
            max_success=api_success_rates['google']

            for key, value in api_success_rates.items():
                if value > max_success:
                    max_success = value
                    highest_success_rate_api = key

            response = {'api': "{}".format(highest_success_rate_api.title())}
            return response
        except Exception as e:
            print(str(e))

