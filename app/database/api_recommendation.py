import os
import sqlite3


class APIRecommendation:
    #path_to_database = os.path.dirname(os.path.dirname(os.getcwd())) + '/database.db'
    path_to_database = os.getcwd() + '/database.db'

    @classmethod
    def execute_query(cls, query):
        connection = sqlite3.connect(cls.path_to_database)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @classmethod
    def calculate_success_rate(cls):
        try:
            # Connect to the SQLite database.
            connection = sqlite3.connect(cls.path_to_database)
            cursor = connection.cursor()

            # Define dictionaries to store the total attempts and successful attempts for each API.
            api_total_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}
            api_successful_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}

            # Fetch data from the database and update the dictionaries accordingly.
            query = "SELECT api_used, translation_success FROM translation_requests WHERE timestamp >= DATETIME('now', '-1 hour');"
            result = cls.execute_query(query)
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

            # Close the database connection.
            cursor.close()
            connection.close()

            highest_success_rate_api = max(api_success_rates, key=api_success_rates.get)
            response = {'api': "{}".format(highest_success_rate_api.title())}
            return response
        except Exception as e:
            print(str(e))

