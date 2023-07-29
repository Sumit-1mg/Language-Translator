from app.utils.language_code import LanguageCodeHandler


class Suggestions:
    def __init__(self):
        pass

    def suggestion_handler(self, request_data):
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
