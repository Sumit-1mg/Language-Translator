import os
from requests_cache import CachedSession
from sanic import Sanic
from sanic import response
from sanic.response import json

from app.managers.detector import Detector
from app.managers.translation import Translator
from app.managers.file_translate import File_translator

from app.utils.constant import GOOGLE_URL
from app.utils.dotenv_reader import google_api_key
from app.utils.suggestions import Suggestions
from app.database.api_recommendation import APIRecommendation

app = Sanic("Translator")


async def is_google_translation_api_available():
    try:
        params = {
            "q": "hello",
            "target": "hi",
            "key": google_api_key,
        }
        session = CachedSession(cache_name='cache', allowable_methods=['GET', 'POST'], expire_after=86400)
        session.post(GOOGLE_URL, params=params, timeout=5)
        return True
    except:
        return False


# Before server start listener
@app.listener("before_server_start")
async def check_api_availability(app, loop):
    print("Checking Translator API availability...")
    api_available = await is_google_translation_api_available()
    if not api_available:
        raise Exception("Translator API is not available. Server cannot start.")
    print("Translator API is available. Starting the server.")


@app.route('/')
async def index(request):
    with open(os.path.join(os.getcwd(), 'app/html/translator.html')) as f:
        a = f.read()
    return response.html(a)


@app.route('/detect')
async def detect(request):
    with open(os.path.join(os.getcwd(), 'app/html/detector.html')) as f:
        a = f.read()
    return response.html(a)


@app.post('/detector')
async def detector(request):
    _detector = Detector()
    request_data = request.json
    translated_txt = _detector.api_call(request_data)
    return json(translated_txt)


@app.post('/google_api')
async def google(request):
    _translator = Translator()
    request_data = request.json
    response_ = await _translator.translate(request_data, 'google')  # enum
    return json(response_)


@app.post('/lacto_ai_api')
async def lacto(request):
    _translator = Translator()
    request_data = request.json
    response_ = await _translator.translate(request_data, 'lacto')
    return json(response_)


@app.post('/rapid_api')
async def rapid(request):
    _translator = Translator()
    request_data = request.json
    response_ = await _translator.translate(request_data, 'rapid')
    return json(response_)


@app.post('/file_google_api')
async def file_translate(request):
    translator = File_translator()
    request_data = request.json
    ans = await translator.translate_file(request_data)
    return json(ans)


@app.post('/suggestion')
async def suggest(request):
    request_data = request.json
    obj = Suggestions()
    suggestion_list = obj.suggestion_handler(request_data)
    return json(suggestion_list)


@app.get('/recommendations')
async def recommend_api(request):
    try:
        _response = APIRecommendation.calculate_success_rate()
        return json(_response)
    except Exception as e:
        print(str(e))
