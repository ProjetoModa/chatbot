import numpy as np
import time
import random


class DialogPolicy:
    def __init__(self):
        self.intent_to_slot = [
            # ASK:GET
            ["size", "type", "fabric", "pattern"],
            # INFORM:DISAMBIGUATE
            ["size", "type", "fabric", "pattern"],
            # INFORM:GET
            ["size", "type", "fabric", "pattern"],
            # INFORM:REFINE
            ["size", "type", "fabric", "pattern"],
            # REQUEST:ADD_TO_CART
            ["item"],
            # REQUEST:COMPARE
            ["item", "with_item"],
            # REQUEST:GET
            ["size", "type", "fabric", "pattern"]
        ]
        self.recommend_text = [
            "Perhaps you'd like one of these?", "What do you think about one of these?"]
        self.entropy_text = ["What is your preference about {}?",
                             "What do you think about the skirt {}?",
                             "Do you have any preference about {}?",
                             "What {} do you like?"]

    def fill_slots(self, state, intent, entities):
        for slot in self.intent_to_slot[intent]:
            if slot not in state['slots']:
                state['slots'][slot] = []

        for ent, label in entities:
            if label in state['slots'] and ent not in state['slots'][label]:
                state['slots'][label].append(ent)

    def decide(self, state, intent, elapsed):
        actions = []
        shouldRecommend = False

        if intent in []:
            # TODO Não impelmentado
            actions.append(
                {"action": "answer", "text": random.choice(self.answers[i])})
        else:
            shouldRecommend = True

        if elapsed >= 30 or shouldRecommend:
            actions.append({"action": "recommend"})
            actions.append(
                {"action": "answer", "text": random.choice(self.recommend_text)})
            actions.append({"action": "entropy"})
        return actions

    def answer(self, state, text, intent, entities):
        intent_index = np.argmax(intent)
        now = time.time()
        elapsed = now - \
            state['turns'][-1]['time'] if len(state['turns']) else 0
        state['turns'].append({"self": True, "time": now, "data": [
                              {"action": "ask", "text": text, "intent": intent, "entities": entities}]})

        self.fill_slots(state, intent_index, entities)

        actions = self.decide(state, intent, elapsed)

        state['turns'].append(
            {"self": False, "time": time.time(), "data": actions})
        return actions, state
    
    def entropy(self, state):
        actions = []
        entities = [s for s in state['slots'] if not state['slots'][s]]
        if len(entities):
            max_entropy = 0
            entity = None
            for e in entities:
                if not e in ["item", "with_item"] and state['entropy'][e] > max_entropy:
                    max_entropy = state['entropy'][e]
                    entity = e
            if entity:
                text = random.choice([
                    "What is your preference about {}?", 
                    "What do you think about the skirt {}?",
                    "Do you have any preference about {}?",
                    "What {} do you like?"
                    ])
                actions.append({"action": "answer", "text": text.format(entity)})
        return actions, state
