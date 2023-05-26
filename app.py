from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import Chatbot
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

cors = CORS()
chatbot = Chatbot()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    
    cors.init_app(app)
    
    from models import db
    db.init_app(app)
    
    @app.route('/')
    def index():
        return "ok"
    
    @app.route('/init', methods=['POST'])
    def init():
        id = request.json.get('id')
        utterance = request.json.get('utterance')
        return jsonify({"state": chatbot.chat(id, utterance)})
    
    @app.route('/chat', methods=['POST'])
    def chat():
        id = request.json.get('id')
        utterance = request.json.get('utterance')
        actions, state = chatbot.chat(id, utterance)
        return jsonify({"actions": actions, "state": state})
    
    @app.route('/entropy', methods=['POST'])
    def entropy():
        id = request.json.get('id')
        entropy = request.json.get('entropy')
        actions, state = chatbot.entropy(id, entropy)
        return jsonify({"actions": actions, "state": state})
    
    @app.route('/like', methods=['POST'])
    def like():
        id = request.json.get('id')
        product = request.json.get('product')
        return jsonify({"state": chatbot.like(id, product)})
    
    @app.route('/dislike', methods=['POST'])
    def dislike():
        id = request.json.get('id')
        product = request.json.get('product')
        return jsonify({"state": chatbot.dislike(id, product)})
    
    @app.route('/finish', methods=['POST'])
    def finish():
        id = request.json.get('id')
        return jsonify({"state": chatbot.finish(id)})
        
        
    return app