from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin


import numpy as np

class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, fill_value="NaN", weight=1.0):
    self.ohe = OneHotEncoder(handle_unknown='ignore')
    self.fill_value = fill_value
    self.weight = weight

  def fit(self, X, y=None):
    X_str = np.asarray(X).astype(str)  # Convert to string type
    self.ohe.fit(X_str.reshape(-1, 1))
    return self

  def transform(self, X):
    X_str = np.asarray(X).astype(str)  # Convert to string type
    X_filled = np.where(X_str == '', self.fill_value, X_str)
    X_filled_reshaped = X_filled.reshape(-1, 1)
    return self.ohe.transform(X_filled_reshaped) * self.weight
  
