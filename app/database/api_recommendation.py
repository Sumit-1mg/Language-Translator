import sqlite3


class APIRecommendation:

    @classmethod
    def execute_query(cls, query):
        connection = sqlite3.connect('/Users/sumit.gangwar1/Desktop/Language-Translator/database.db')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @classmethod
    def calculate_success_rate(cls):
        # Connect to the SQLite database.
        connection = sqlite3.connect('/Users/sumit.gangwar1/Desktop/Language-Translator/database.db')
        cursor = connection.cursor()

        # Define dictionaries to store the total attempts and successful attempts for each API.
        api_total_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}
        api_successful_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}

        # Fetch data from the database and update the dictionaries accordingly.
        query = "SELECT api_used, translation_success FROM translation_requests;"
        result = cls.execute_query(query)

        for row in result:
            api, success = row
            if api in api_total_attempts:
                api_total_attempts[api] += 1
                if success == 1:
                    api_successful_attempts[api] += 1

        # Calculate success rates for each API.
        success_rate_google = api_successful_attempts['google'] / api_total_attempts['google']
        success_rate_lacto = api_successful_attempts['lacto'] / api_total_attempts['lacto']
        success_rate_rapid = api_successful_attempts['rapid'] / api_total_attempts['rapid']

        # Close the database connection.
        cursor.close()
        connection.close()

        return success_rate_google, success_rate_lacto, success_rate_rapid
