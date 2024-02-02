from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin


import numpy as np

class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, fill_value="NaN", weight=1.0, sparse_output=True):
    self.sparse_output = sparse_output
    self.ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=self.sparse_output)
    self.fill_value = fill_value
    self.weight = weight

  def fit(self, X, y=None):
    X_str = np.asarray(X).astype(str)
    self.ohe.fit(X_str.reshape(-1, 1))
    return self

  def transform(self, X):
    X_str = np.asarray(X).astype(str)
    X_filled = np.where(X_str == '', self.fill_value, X_str)
    X_filled_reshaped = X_filled.reshape(-1, 1)
    return self.ohe.transform(X_filled_reshaped) * self.weight
  
