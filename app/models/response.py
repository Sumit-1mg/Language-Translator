from typing import Union

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: int = 1
    error_message: str


class TranslatorSuccessResponse(BaseModel):
    error: int = 0
    translated_text: str


class TranslatorResponseModel(BaseModel):
    response: Union[TranslatorSuccessResponse, ErrorResponse]


class DetectorSuccessResponse(BaseModel):
    error: int = 0
    detected_language: str


class DetectorResponseModel(BaseModel):
    response: Union[DetectorSuccessResponse, ErrorResponse]


class FileTranslatorSuccessResponse(BaseModel):
    error: int = 0
    output_file: str


class FileTranslatorResponseModel(BaseModel):
    response: Union[DetectorSuccessResponse, ErrorResponse]
