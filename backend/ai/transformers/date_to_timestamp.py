from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime

class DateToTimestampTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, date_column, weight=1.0):
        self.date_column = date_column
        self.timestamp_scaler = MinMaxScaler()
        self.weight = weight
    
    def fit(self, X, y=None):
        X_timestamp = X[self.date_column].apply(self._date_to_timestamp).to_frame()
        self.timestamp_scaler.fit(X_timestamp)
        
        return self
    
    def transform(self, X):
        X_transformed = X.copy()
        X_transformed[self.date_column] = X_transformed[self.date_column].apply(self._date_to_timestamp)
        X_transformed[self.date_column] = self.timestamp_scaler.transform(X_transformed[self.date_column].to_frame())
        
        return X_transformed * self.weight
    
    def _date_to_timestamp(self, date_value):
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, "%Y-%m-%d")
        return int(date_value.timestamp())