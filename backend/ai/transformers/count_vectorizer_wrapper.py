from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer


class CountVectorizerWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, weight=1.0):
        self.weight = weight
        self.count_vectorizer = CountVectorizer()

    def fit(self, X, y=None):
        self.count_vectorizer.fit(X)
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy = self.count_vectorizer.transform(X_copy)

        return X_copy * self.weight
