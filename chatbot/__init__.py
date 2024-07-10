from models import db, Session, Logs, Answers
from .digai import DigAI
from googletrans import Translator
import json


class Chatbot:
    def __init__(self):
        self.digai = DigAI()
        self.defaultSession = {
            "turns": [],
            "slots": {},
            "liked": [],
            "page": "/",
        }
        self.t = Translator()

    def _log(self, data):
        log = Logs(description=json.dumps(data))
        db.session.add(log)
        db.session.commit()
        return log

    def _insertSession(self, uuid, state):
        session = Session(uuid=uuid, state=json.dumps(state))
        db.session.add(session)
        db.session.commit()
        return session

    def _updateSession(self, session):
        db.session.add(session)
        db.session.commit()
        return session

    def _getSession(self, id):
        session = Session.query.filter_by(uuid=id).first()
        if not session:
            session = self._insertSession(id, self.defaultSession)
        return session

    def init(self, id, prolific):
        self._log({"action": '/init', "uuid": id, "prolific": prolific})
        return self._getSession(id).state

    def log(self, id, data):
        self._log({"action": '/log', "uuid": id, "data": data})

    def navigate(self, id, page):
        self._log({"action": '/navigate', "uuid": id, "data": {"page": page}})
        session = self._getSession(id)
        state = json.loads(session.state)

        state['page'] = page
        session.state = json.dumps(state)
        self._updateSession(session)

        return session.state

    def chat(self, id, text, lang):
        session = self._getSession(id)
        state = json.loads(session.state)

        if lang != "en":
            translated = self.t.translate(text, dest='en')
            self._log({"action": "/translate", "uuid": id, "data": {"from": text, "to": translated.text}})
            text = translated.text

        actions, state = self.digai.turn(state, text)
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/chat', "uuid": id,
                  "data": {"state": state, "actions": actions}})
        
        if lang != "en":
            for i in range(len(actions)):
                if actions[i]['action'] == "answer":
                    translated = self.t.translate(actions[i]['text'], dest=lang)
                    self._log({"action": "/translateAnswer", "uuid": id, "data": {"from": actions[i]['text'], "to": translated.text}})
                    actions[i]['text'] = translated.text
                    
        
        return actions, state

    def like(self, id, product):
        session = self._getSession(id)
        state = json.loads(session.state)
        if product not in state['liked']:
            state['liked'].append(product)
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/like', "uuid": id,
                  "data": {"state": state, "product": product}})
        return state

    def dislike(self, id, product):
        session = self._getSession(id)

        state = json.loads(session.state)
        if product in state['liked']:
            state['liked'].remove(product)
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/dislike', "uuid": id,
                  "data": {"state": state, "product": product}})
        return state

    def finish(self, id):
        session = self._getSession(id)

        state = json.loads(session.state)
        if state['page'] == "/part-a":
            state['page'] = '/inter-ab'
        elif state['page'] == "/part-b":
            state['page'] = '/questions'
        elif state['page'] == "/part-c":
            state['page'] = '/end'
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/finish', "uuid": id})
        return state

    def questionnaire(self, id, data, complete):
        answers = Answers.query.filter_by(uuid=id).first()
        if not answers:
            answers = Answers(uuid=id)
        answers.data = json.dumps(data)
        answers.complete = complete
        db.session.add(answers)
        db.session.commit()

        self._log({"action": '/questionnaire', "uuid": id,
                  "data": {"data": data, "complete": complete}})
