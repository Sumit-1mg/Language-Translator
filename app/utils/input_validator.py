from app.managers.detector import Detector
from app.utils.language_code import LanguageCodeHandler


class InputValidator:
    def __init__(self):
        pass

    def validate(self, request_data):
        ans = {'error': 0}

        source_language = request_data.get("source_language").lower().strip()

        source_language_detector = Detector()
        detector_response = source_language_detector.api_call(request_data)
        if detector_response['error']:
            return detector_response
        detected_language = detector_response['detected_language']

        # Checking if source language is given
        validate=LanguageCodeHandler()
        if len(source_language.strip()) > 0:
            # Checking for valid language
            if not validate.is_valid_language(source_language):
                ans['error'] = 1
                ans["error_message"] = "API does not support {} language as source language".format(source_language)
                return ans
            elif detected_language.lower() != source_language.lower():
                ans['error'] = 1
                ans['error_message'] = 'Detected Language doesnot match with Source Language'
                return ans
        ans['source_language'] = detected_language
        request_data['source_language'] = detected_language
        target_language = request_data.get('target_language').lower().strip()
        ans['target_language'] = target_language
        # checking if target language is valid or not
        if not validate.is_valid_language(target_language):
            ans['error'] = 1
            ans["error_message"] = "API does not support {} language as target language".format(target_language)
            return ans
        return ans
