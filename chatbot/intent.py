import pickle as pkl
import os

class IntentClassifier:
    def __init__(self):
        #TODO import model
        # self.preprocessor = self._load(os.path.join(os.path.dirname(__file__), "preprocessor.pkl"))
        # self.model = self._load(os.path.join(os.path.dirname(__file__), "model.pkl"))
        pass
    def _load(self, filename):
        file = open(filename, "rb")
        data = pkl.load(file)
        file.close()
        return data
    def predict(self, text):
        return self.model.predict_proba(self.preprocessor.transform([text])).tolist()[0]