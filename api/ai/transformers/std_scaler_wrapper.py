from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

class StandardScalerWrapper(BaseEstimator, TransformerMixin):
  def __init__(self, weight=1.0):
    self.weight = weight
    self.scaler = StandardScaler()
  
  def fit(self, X, y=None):
    self.scaler.fit(X)
    return self
  
  def transform(self, X):
    X_copy = X.copy()
    X_copy = self.scaler.transform(X_copy)
    return X_copy * self.weight