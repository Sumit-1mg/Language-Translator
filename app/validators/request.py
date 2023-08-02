from pydantic import BaseModel,validator
from app.utils.language_code import LanguageCodeHandler

class ValidateSupport:
    @classmethod
    def validate_support(cls,language):
        language = language.lower().strip()
        validate = LanguageCodeHandler()
        if not validate.is_valid_language(language):
            raise ValueError("API does not support {} language ".format(language))
        return language


class TranslatorModel(BaseModel):
    source_language: str
    source_text: str
    target_language: str

    @validator('source_text')
    def validate_support(source_text, values):
        from app.managers.detector import Detector
        source_language = values['source_language']
        source_language_detector = Detector()
        _detected_language = source_language_detector.api_call({'source_text':source_text})
        detected_language = _detected_language['detected_language']
        if detected_language.lower() != source_language:
            raise ValueError('Detected Language doesnot match with Source Language')

        return source_text

    @validator("source_language")
    def validate_source_language(value):
        return ValidateSupport.validate_support(value)

    @validator("target_language")
    def validate_target_language(value):
        return ValidateSupport.validate_support(value)

class FileTranslatorModel(BaseModel):
    input_file: str
    output_language: str

    @validator("output_language")
    def validate_output_language(value):
        return ValidateSupport.validate_support(value)


class DetectorModel(BaseModel):
    source_text: str
