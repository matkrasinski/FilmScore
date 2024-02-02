import os
import pandas as pd
from ..data.constant.FILES_NAMES import KNN_MODEL_LOCAL_PATH
from ..database.util.import_pipeline import ImportPipeline
from ..data.status.status_checker import check_file_status
from ..data.status.file_status import FileStatus
from ..ai.model_loader import ModelLoader
from ..data.util.data_imputer import apply_ratings, fillna, fillna_ratings
from ..data.util.ratings_generator import RatingsGenerator
from ..data.constant.COLUMNS import *


def get_prediction(data, model_path=KNN_MODEL_LOCAL_PATH):
    status = check_file_status(model_path)
    data_pipeline = ImportPipeline()
    if status[STATUS_COLUMN] != FileStatus.OK:
        data_pipeline.run_pipeline()

    ratings_helper = RatingsGenerator()

    data[ACTORS_RATING_COLUMN] = ratings_helper.get_people_avg_ratings(
        people=data[ACTORS_COLUMN])
    data[DIRECTORS_RATING_COLUMN] = ratings_helper.get_people_avg_ratings(
        people=data[DIRECTORS_COLUMN])

    data[COMPANIES_RATING_COLUMN] = ratings_helper.get_companies_avg_ratings(
        companies=data[PRODUCTION_COMPANIES_COLUMN])

    if type(data) != pd.DataFrame:
        data = pd.DataFrame([data])

    data = fillna_ratings(data)

    data[RUNTIME_COLUMN] = data[RUNTIME_COLUMN].apply(
        lambda x: x if isinstance(x, int) else 0)
    data[RELEASE_DATE_COLUMN] = data[RELEASE_DATE_COLUMN] if data[RELEASE_DATE_COLUMN].str == '' else '9999-12-31'

    return ModelLoader(model_path=model_path).predict_rating(data)
