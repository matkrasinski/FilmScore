from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfVectorizerWrapper(BaseEstimator, TransformerMixin):
  def __init__(self, weight=1.0):
    self.weight = weight
    self.tfidf = TfidfVectorizer(max_features=1000)

  def fit(self, X, y=None):
    self.tfidf.fit(X)
    return self
  
  def transform(self, X):
    X_copy = X.copy()
    X_copy = self.tfidf.transform(X_copy)

    return X_copy * self.weight