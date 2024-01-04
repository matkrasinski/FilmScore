from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin


class MinMaxScalerWrapper(BaseEstimator, TransformerMixin):
  def __init__(self, weight=1.0):
    self.weight = weight
    self.scaler = MinMaxScaler()
  
  def fit(self, X, y=None):
    self.scaler.fit(X)
    return self
  
  def transform(self, X):
    X_copy = X.copy()
    X_copy = self.scaler.transform(X_copy)
    return X_copy * self.weight