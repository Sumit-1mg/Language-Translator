from pydantic import BaseModel


class TranslatorModelResponse(BaseModel):
    error: int
    source_language: str
    target_text: str


class DetectorModelResponse(BaseModel):
    error: int
    detected_language: str


class FileTranslatorModelResponse(BaseModel):
    error: int
    output_file: str
