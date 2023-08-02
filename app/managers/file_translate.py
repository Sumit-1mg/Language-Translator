import asyncio
import aiohttp
from pydantic import ValidationError

from app.validators.request import FileTranslatorModel
from app.validators.response import FileTranslatorResponseModel
from app.utils.dotenv_reader import google_api_key
from app.utils.constant import GOOGLE_URL
from app.utils.language_code import LanguageCodeHandler


class File_translator:

    def __init__(self):
        self.api_call_limit = 40
        self.url = GOOGLE_URL

    def split_text_into_chunks(self, text, chunk_size):
        '''
        Split the given text into chunks of the specified chunk_size.
        :param
        text (str): The input text to be split into chunks.
        chunk_size (int): The maximum size of each chunk.
        :return:
        List[str]: A list of text chunks, where each chunk has a maximum size of chunk_size.
        '''

        chunks = []
        current_chunk = ""

        for word in text.split():
            if len(current_chunk) + len(word) <= chunk_size:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "

        # Add the last chunk, if any
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    async def make_request(self, session, text, target_language):
        '''
        This make async request to the google api
        '''
        params = {
            'key': google_api_key,
            'q': text,
            'target': target_language,
        }
        async with session.get(self.url, params=params) as response:
            data = await response.json()
            return data['data']['translations'][0]['translatedText']

    async def async_api_call(self, text, target_language):
        async with aiohttp.ClientSession() as session:
            translated_text = await self.make_request(session, text, target_language)
            return translated_text

    async def translate_file(self, request_data):

        try:
            FileTranslatorModel(**request_data)
        except ValidationError as e:
            return {"error": 1, "error_message": str(e)}

        input_file = request_data['input_file']
        output_language = request_data['output_language']
        output_file = input_file.split('.')[0] + '_' + output_language + '.' + input_file.split('.')[1]

        ans = {'error': 0}
        try:
            with open(input_file, 'r') as file:
                input_text = file.read()
        except:
            ans['error'] = 1
            ans['error_message'] = 'File doesnot exist'
            return ans
        chunks = self.split_text_into_chunks(input_text, 5000)

        translated_chunks = []
        tasks = []
        language_to_code = LanguageCodeHandler()
        target_language = language_to_code.get_code(output_language)
        for chunk in chunks:
            task = self.async_api_call(chunk, target_language)
            tasks.append(task)
        translated_chunks = await asyncio.gather(*tasks, return_exceptions=True)
        translated_text = " ".join(translated_chunks)
        with open(output_file, 'w') as file:
            file.write(translated_text)
        ans['output_file'] = output_file

        try:
            FileTranslatorResponseModel(**ans)
        except Exception as e:
            return {"error": 1, "error_message": str(e)}

        return ans
