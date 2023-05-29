import pickle as pkl
import os

class IntentClassifier:
    def __init__(self):
        self.label_encoder = self._load(os.path.join(os.path.dirname(__file__), "label.pkl"))
        self.tfidf_encoder = self._load(os.path.join(os.path.dirname(__file__), "tfidf.pkl"))
        self.model = self._load(os.path.join(os.path.dirname(__file__), "model.pkl"))
        self.label_dict = dict(zip(self.label_encoder.classes_, self.label_encoder.transform(self.label_encoder.classes_)))
    
    def getLabel(self, label):
        return self.label_dict(label)
        
    def _load(self, filename):
        file = open(filename, "rb")
        data = pkl.load(file)
        file.close()
        return data
    def predict(self, text):
        return self.model.predict_proba(self.tfidf_encoder.transform([text])).tolist()[0]