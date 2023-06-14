import numpy as np
import time
import random
import requests
import os
from .intent import Intent


class DialogPolicy:
    def __init__(self):
        self.intent_to_slot = {
            Intent.ASK_GET: ["size", "type", "fabric", "pattern", "color"],
            Intent.INFORM_DISAMBIGUATE: [],
            Intent.INFORM_GET: ["size", "type", "fabric", "pattern", "color"],
            Intent.INFORM_REFINE: ["size", "type", "fabric", "pattern", "color"],
            Intent.REQUEST_ADD_TO_CART: ["item"],
            Intent.REQUEST_COMPARE: ["item", "with_item"],
            Intent.REQUEST_GET: ["size", "type", "fabric", "pattern", "color"]
        }
        self.intent_to_answer = {
            Intent.ASK_GET: [
                "I apologize, but I'm not programmed to provide information about the clothes yet.",
                "Unfortunately, I'm unable to assist with questions specifically about the clothes on display.",
                "I'm sorry, but I don't have the capability to answer questions about the clothes in the display.",
                "Regrettably, I'm unable to provide information about the clothes in display.",
                "Unfortunately, I don't have access to information about the clothes showcased.",
                "I regret to inform you that I'm not programmed to answer specific questions about the clothes on display.",
            ],
            Intent.INFORM_DISAMBIGUATE: [
                "I apologize for the inconvenience, but I cannot identify or provide information about specific clothes at this time.",
                "Unfortunately, I am unable to assist with questions specifically related to the clothes on display as I lack the necessary knowledge.",
                "I'm sorry, but I don't have the capability to answer questions about the clothes in the display since I cannot identify them.",
                "Regrettably, I am unable to provide information about the clothes in display as I don't have the means to identify them.",
                "Unfortunately, I don't have access to information about the clothes showcased, making it impossible for me to provide details about them.",
                "I regret to inform you that I'm not programmed to answer specific questions about the clothes on display since I cannot identify them.",
            ],
            Intent.INFORM_GET: [],
            Intent.INFORM_REFINE: [],
            Intent.REQUEST_ADD_TO_CART: [
                "I'm sorry, but I don't have a shopping cart feature yet.",
                "Unfortunately, I'm unable to assist with request to add to cart as I lack a shopping cart functionality.",
                "I apologize, but I don't have the capability to add items to the cart as I don't possess a shopping cart feature.",
                "Regrettably, I'm unable to add clothes to cart since I don't have a shopping cart feature.",
            ],
            Intent.REQUEST_COMPARE: [
                "I apologize for any confusion, but I'm unable to compare the items on display as I don't have the capability to track them individually.",
                "I'm sorry, but I can't provide a comparison of the items on display because I don't have the ability to track them.",
                "Unfortunately, I don't have the capability to compare the items on display as I can't track them individually.",
                "Regrettably, I'm unable to perform comparisons of the items on display since I can't track them individually.",
                "I'm sorry, but I don't have access to the necessary information to compare the items on display as I can't track them individually.",
                "I regret to inform you that I'm unable to compare the items on display because I don't have the ability to track them individually.",
            ],
            Intent.REQUEST_GET: []
        }
        self.ask_can_assist = "I can assist you in filtering the catalog based on your preferences. Please provide me with the specific fabric, pattern, size, color, or type you are looking for, and I will help narrow down the options to match your requirements. Feel free to let me know your preferences, and I'll do my best to find the perfect match for you."
        self.recommend_text = [
            "Perhaps you'd like these?", "What do you think about these?"]
        self.entropy_text = ["What is your preference about {}?",
                             "What do you think about the skirt {}?",
                             "Do you have any preference about {}?",
                             "What {} do you like?"]
        self.instead = [
            "Instead...",
            "Alternatively...",
            "As an alternative",
        ]

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

        if intent in [Intent.ASK_GET, Intent.INFORM_DISAMBIGUATE, Intent.REQUEST_COMPARE]:
            actions.append(
                {"action": "answer", "text": random.choice(self.intent_to_answer[intent])})
            if elapsed >= 30:
                shouldRecommend = True
                actions.append(
                    {"action": "answer", "text": random.choice(self.instead)})
            else:
                actions.append(
                    {"action": "answer", "text": self.ask_can_assist})
        elif intent in [Intent.REQUEST_GET, Intent.INFORM_GET, Intent.INFORM_REFINE]:
            shouldRecommend = True

        if shouldRecommend:
            actions.append({"action": "recommend"})
            actions.append(
                {"action": "answer", "text": random.choice(self.recommend_text)})
            entropyResponse = requests.post(
                os.getenv('RECOMM_API')+"/entropy", json={"state": state})
            if entropyResponse.ok:
                actions.extend(self.entropy(
                    state, entropyResponse.json()['entropy']))
        return actions

    def answer(self, state, text, intent, entities):
        intent_index = Intent(np.argmax(intent))
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
