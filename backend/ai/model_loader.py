import pandas as pd

from joblib import dump, load
from .model.knn import prepare_model
from ..data.status.status_checker import check_file_status
from ..data.status.file_status import FileStatus
from ..data.constant.COLUMNS import X_TRAIN_COLUMNS, Y_TRAIN_COLUMN
from ..data.constant.FILES_NAMES import KNN_MODEL_LOCAL_PATH
from ..data.constant.COLUMNS import *


class ModelLoader:

    def __init__(self, train_data=pd.DataFrame(), model_path=KNN_MODEL_LOCAL_PATH):
        self.train_data = train_data
        self.model = None
        self.model_path = model_path

    def load_model(self, generate=False):
        model_status = check_file_status(self.model_path)
        if generate or model_status[STATUS_COLUMN] != FileStatus.OK:
            self.model = self.generate_model()
        else:
            self.model = load(self.model_path)

    def generate_model(self, save=True):
        model = prepare_model()

        model.fit(self.train_data[X_TRAIN_COLUMNS],
                  self.train_data[Y_TRAIN_COLUMN])

        if save:
            dump(model, KNN_MODEL_LOCAL_PATH)

        return model

    def predict_rating(self, data):
        if self.model is None:
            self.load_model()
        return self.model.predict(data)
