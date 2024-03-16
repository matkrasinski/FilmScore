from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin


class VideosCounterTransformer(BaseEstimator, TransformerMixin):    
    def __init__(self, separator="|", bonus=1, videos_column="videos", weight=1.0):
        self.separator = separator
        self.bonus = bonus
        self.videos_column = videos_column
        self.scaler = StandardScaler()
        self.weight = weight


    def fit(self, X, y=None):
        transformed_data = self.transform(X)
        self.scaler.fit(transformed_data)

        return self

    def transform(self, X):
        result = X[self.videos_column].apply(lambda x: len(x.split(self.separator))) + self.bonus
        result_array = result.values.reshape(-1, 1)

        scaled_result = self.scaler.fit_transform(result_array)
     
        return scaled_result * self.weight