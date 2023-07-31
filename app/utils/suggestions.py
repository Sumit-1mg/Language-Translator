from app.utils.language_code import LanguageCodeHandler


class Suggestions:
    def __init__(self):
        pass

    def suggestion_handler(self, request_data):
        '''
         Generate language suggestions based on the provided target_string.
        :param request_data -> dict : A dictionary containing the 'text' field, representing the target_string for which language suggestions are to be generated.
        :return: dict: A dictionary containing the 'suggestion' field, which is a list of language suggestions.
        '''
        suggestions = []

        target_string = request_data.get('text')
        n = len(target_string)

        language_code = LanguageCodeHandler()

        if not n:
            return suggestions
        for word in language_code.get_all_language().keys():
            if target_string.lower() == word[:n].lower():
                suggestions.append(word)
        if len(suggestions) > 10:
            suggestions = suggestions[:10]
        suggestion_response = {'suggestion': suggestions}
        return suggestion_response
