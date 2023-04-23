import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sentence_transformers import SentenceTransformer


class CustomSentenceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = self.__load_model()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        texts = pd.Series(X)
        embeddings = self.model.encode(list(texts), show_progress_bar=False)
        return embeddings

    def __load_model(self):
        model = SentenceTransformer(self.model_name)
        return model

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["model"]
        return state

    def __setstate__(self, state):
        """Restore state from the unpickled state values."""
        self.__dict__.update(state)
        self.model = self.__load_model()
