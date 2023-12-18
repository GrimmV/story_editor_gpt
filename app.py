from flask import Flask, request, make_response, jsonify
# from StandardBot import StandardBot
from InteractiveBot import InteractiveBot
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
# import warnings
# warnings.filterwarnings("ignore")

# Prepare environment variables
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(filename='logging.log', level=logging.DEBUG)

load_dotenv()

CURRENT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ['OPENAI_API_KEY'] = CURRENT_OPENAI_API_KEY
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://nextvisionopenai.openai.azure.com"
os.environ["OPENAI_DEPLOYMENT_NAME"] = "GPT35Turbo"
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# init GPT Objects
def create_app(config=None):
    app = Flask(__name__)

    standard_bot = InteractiveBot()

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,  # This will use the user's IP to track the requests
        default_limits=["6 per minute"]
    )

    @app.route("/api/test", methods=["GET", "OPTIONS"])
    # @limiter.limit("1 per minute")
    def test_api():
        
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()
        elif request.method == "GET": 
            gpt_response = standard_bot.test_call()
            response = make_response(gpt_response)
            return _corsify_actual_response(response)
        else:
            raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))
                
    @app.route('/api/recommend/outline', defaults={'temperature': None}, methods=["POST", "OPTIONS"])
    @app.route("/api/recommend/outline/<temperature>", methods=["POST", "OPTIONS"])
    def recommend_outline(temperature):
        
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()
        elif request.method == "POST": 
            request.get_json(force=True)
            request_json = request.json
            if (temperature):
                gpt_response = standard_bot.handle_outline_request(request_json["setup"], float(temperature))
            else:
                gpt_response = standard_bot.handle_outline_request(request_json["setup"])
            response = make_response(gpt_response)
            return _corsify_actual_response(response)
        else:
            raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))
        

    @app.route('/api/recommend', defaults={'temperature': None}, methods=["POST", "OPTIONS"])
    @app.route("/api/recommend/<temperature>", methods=["POST", "OPTIONS"])
    def recommend(temperature):
        
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()
        elif request.method == "POST": 
            request.get_json(force=True)
            request_json = request.json
            if (temperature):
                gpt_response = standard_bot.handle_suggestion_request(request_json["setup"], request_json["history"], request_json["character_choice"], float(temperature))
            else:
                gpt_response = standard_bot.handle_suggestion_request(request_json["setup"], request_json["history"], request_json["character_choice"])
            response = make_response(gpt_response)
            return _corsify_actual_response(response)
        else:
            raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))


    def _build_cors_preflight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    def _corsify_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # Error handler for rate limiting
    @app.errorhandler(429)
    def ratelimit_error(e):
        return jsonify(success=False, message="ratelimit exceeded", error=str(e)), 429
    
    return app

if __name__ == "__main__":
    app = create_app()
    serve(app, host='0.0.0.0', port=5000)