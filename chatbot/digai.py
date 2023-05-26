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
        actions = self.policy.answer(state, text, intent, entities)
        return actions

    def entropy(self, state):
        return self.policy.entropy(state)
