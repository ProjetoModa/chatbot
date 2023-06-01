from models import db, Session, Logs
from .digai import DigAI
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

    def init(self, id):
        self._log({"action": '/init', "uuid": id})
        return self._getSession(id).state

    def navigate(self, id, page):
        self._log({"action": '/navigate', "uuid": id, "data": {"page": page}})
        session = self._getSession(id)
        state = json.loads(session.state)
        
        state['page'] = page
        session.state = json.dumps(state)
        self._updateSession(session)
        
        return session.state

    def chat(self, id, text):
        session = self._getSession(id)
        state = json.loads(session.state)

        actions, state = self.digai.turn(state, text)
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/chat', "uuid": id,
                  "data": {"state": state, "actions": actions}})
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
        state['page'] = '/end'
        session.state = json.dumps(state)
        self._updateSession(session)

        self._log({"action": '/finish', "uuid": id})
        return state
