from typing import Union
from pydantic import BaseModel

class TranslatorResponseModel(BaseModel):
    error: int = 0
    source_language: str
    target_text: str

class DetectorResponseModel(BaseModel):
    error: int = 0
    detected_language: str


class FileTranslatorResponseModel(BaseModel):
    error: int = 0
    output_file: str

