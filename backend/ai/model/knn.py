from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from backend.ai.transformers import OneHotEncoderTransformer, MultiLabelBinarizerTransformer, CountVectorizerWrapper, DateToTimestampTransformer, VideosCounterTransformer, MinMaxScalerWrapper, StandardScalerWrapper


def prepare_model(k=20):
    weights = {
        "directors_rating": 20/100,
        "actors_rating": 23/100,
        "companies_rating": 23/100,
        "collection": 6/100,
        "release_date": 6/100,
        "spoken_languages": 6/100,
        "genres": 4.8/100,
        "production_companies": 3/100,
        "keywords": 1.5/100,
        "actors": 1.5/100,
        "directors": 1.5/100,
        "runtime": 1.5/100,
        "videos": 1.5/100,
        "og_lang": 0.7/100
    }

    transformers = [
        ("collection", OneHotEncoderTransformer(
            weight=weights["collection"]), "belongs_to_collection"),
        ("original_language", OneHotEncoderTransformer(
            weight=weights["og_lang"]), "original_language"),
        ("spoken_langugaes", MultiLabelBinarizerTransformer(
            weight=weights["spoken_languages"]), "spoken_languages"),
        ('genres', MultiLabelBinarizerTransformer(
            weight=weights["genres"]), "genres"),
        ("production_companies", MultiLabelBinarizerTransformer(
            weight=weights["production_companies"]), "production_companies"),
        ('actors', MultiLabelBinarizerTransformer(
            weight=weights["actors"]), "actors"),
        ('directors', MultiLabelBinarizerTransformer(
            weight=weights["directors"]), "directors"),
        ("keywords", CountVectorizerWrapper(
            weight=weights["keywords"]), "keywords"),
        ("release_date", DateToTimestampTransformer(
            date_column="release_date", weight=weights["release_date"]), ["release_date"]),
        ("runtime", StandardScalerWrapper(
            weight=weights["runtime"]), ["runtime"]),
        ("videos", VideosCounterTransformer(
            weight=weights["videos"]), ["videos"]),
        ("companies_rating", MinMaxScalerWrapper(
            weight=weights["companies_rating"]), ["companies_rating"]),
        ("actors_rating", MinMaxScalerWrapper(
            weight=weights["actors_rating"]), ["actors_rating"]),
        ("directors_rating", MinMaxScalerWrapper(
            weight=weights["directors_rating"]), ["directors_rating"])
    ]

    preprocessor = ColumnTransformer(
        transformers=transformers, remainder="drop")

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('knn', KNeighborsRegressor(n_neighbors=k))
    ])
    return model
