import os
from sanic import Sanic
from sanic import response
from sanic.response import json
from sqlalchemy.ext.asyncio import create_async_engine
from app.managers.detector import Detector
from app.managers.translation import Translator
from app.managers.file_translate import File_translator
from app.models.recomendation_model import Recommendation
from app.utils.is_api_available import IsApiAvailable
from app.utils.suggestions import Suggestions

app = Sanic("Translator")

# Before server start listener
@app.listener("before_server_start")
async def check_api_availability(app, loop):
    print("Checking Translator API availability...")
    api_available = await IsApiAvailable.is_api_available()
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
        _response = Recommendation.highest_success_api()
        return json(_response)
    except Exception as e:
        print(str(e))

