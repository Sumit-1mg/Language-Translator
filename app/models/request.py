from pydantic import BaseModel,validator

from app.utils.language_code import LanguageCodeHandler


class TranslatorModel(BaseModel):
    source_language: str
    source_text: str
    target_language: str

    @validator("source_language")
    def validate_source_language(value):
        _source_language = value.lower().strip()
        validate = LanguageCodeHandler()
        if not validate.is_valid_language(_source_language):
            raise ValueError("API does not support {} language as target language".format(_source_language))
        return value

    @validator("target_language")
    def validate_target_language(value):
        _target_language = value.lower().strip()
        validate = LanguageCodeHandler()
        if not validate.is_valid_language(_target_language):
            raise ValueError("API does not support {} language as target language".format(_target_language))
        return value

class FileTranslatorModel(BaseModel):
    input_file: str
    output_language: str

    @validator("output_language")
    def validate_output_language(value):
        validate = LanguageCodeHandler()
        _target_language = value.lower().strip()
        if not validate.is_valid_language(_target_language):
            raise ValueError("API does not support {} language as target language".format(_target_language))
        return value


class DetectorModel(BaseModel):
    source_text: str
