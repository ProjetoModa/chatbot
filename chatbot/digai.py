from .intent import IntentClassifier
from .entity import EntityExtractor
from .policy import DialogPolicy


class DigAI:
    def __init__(self):
        self.intent = IntentClassifier()
        self.entity = EntityExtractor()
        self.policy = DialogPolicy()

    def turn(self, state, text):
        intent = self.intent.predict(text)
        entities = self.entity.extract(text)
        return self.policy.answer(state, text, intent, entities)

    def entropy(self, state):
        return self.policy.entropy(state)
