import numpy as np
import time
import random
import requests
import os


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
        self.intent_to_answer = [
            # ASK:GET
            [
                "I apologize, but I'm not programmed to provide information about the clothes yet.",
                "Unfortunately, I'm unable to assist with questions specifically about the clothes on display.",
                "I'm sorry, but I don't have the capability to answer questions about the clothes in the display.",
                "Regrettably, I'm unable to provide information about the clothes in display.",
                "Unfortunately, I don't have access to information about the clothes showcased.",
                "I regret to inform you that I'm not programmed to answer specific questions about the clothes on display.",
            ],
            # INFORM:DISAMBIGUATE
            # INFORM:GET
            # INFORM:REFINE
            # REQUEST:ADD_TO_CART
            # REQUEST:COMPARE
            # REQUEST:GET
        ]
        self.ask_can_assist = "I can assist you in filtering the catalog based on your preferences. Please provide me with the specific fabric, pattern, size, color, or type you are looking for, and I will help narrow down the options to match your requirements. Feel free to let me know your preferences, and I'll do my best to find the perfect match for you."
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

        if intent in [0]:
            actions.append(
                {"action": "answer", "text": random.choice(self.intent_to_answer[intent])})
            actions.append(
                {"action": "answer", "text": self.ask_can_assist})
        elif elapsed >= 30:
            shouldRecommend = True

        if shouldRecommend:
            actions.append({"action": "recommend"})
            actions.append(
                {"action": "answer", "text": random.choice(self.recommend_text)})
            entropyResponse = requests.post(os.getenv('RECOMM_API')+"/entropy", json={"state": state})
            if entropyResponse.ok:
                actions.extend(self.entropy(state, entropyResponse.json()['entropy']))
        return actions

    def answer(self, state, text, intent, entities):
        intent_index = np.argmax(intent)
        now = time.time()
        elapsed = now - \
            state['turns'][-1]['time'] if len(state['turns']) else 0
        state['turns'].append({"self": True, "time": now, "data": [
                              {"action": "ask", "text": text, "intent": intent, "entities": entities}]})

        self.fill_slots(state, intent_index, entities)

        actions = self.decide(state, intent_index, elapsed)

        state['turns'].append(
            {"self": False, "time": time.time(), "data": actions})
        return actions, state

    def entropy(self, state, entropy):
        actions = []
        entities = [s for s in state['slots'] if not state['slots'][s]]
        if len(entities):
            max_entropy = 0
            entity = None
            for e in entities:
                if e in entropy and entropy[e] > max_entropy:
                    max_entropy = entropy[e]
                    entity = e
            if max_entropy > 0 and entity:
                text = random.choice(self.entropy_text)
                actions.append(
                    {"action": "answer", "text": text.format(entity)})
        return actions
