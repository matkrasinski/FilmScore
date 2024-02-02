from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class MultiLabelBinarizerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, weight=1.0, sparse_output=True):
        self.sparse_output = sparse_output
        self.mlb = MultiLabelBinarizer(sparse_output=self.sparse_output)
        self.weight= weight

    def fit(self, X, y=None):
        self.mlb.fit(X)
        return self

    def transform(self, X):
        return self.mlb.transform(X) * self.weight
