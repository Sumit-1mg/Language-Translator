from pydantic import BaseModel


class TranslatorModel(BaseModel):
    source_language: str
    source_text: str
    target_language: str


class DetectorModel(BaseModel):
    source_text: str


class FileTranslatorModel(BaseModel):
    input_file: str
    output_language: str
