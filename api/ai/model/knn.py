from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from api.ai.transformers import OneHotEncoderTransformer, MultiLabelBinarizerTransformer, TfidfVectorizerWrapper, DateToTimestampTransformer, VideosCounterTransformer, MinMaxScalerWrapper, StandardScalerWrapper

def prepare_model():
    weights = {
            "directors_rating": 6/22 * 1,
            "actors_rating": 7/22 * 1,
            "companies_rating": 7/22 * 1,

            "collection": 1/11 * 1,
            "release_date": 1/11 * 1,
            "spoken_languages": 1/11 * 1, 

            "genres": 1/22 * 1,
            "production_companies": 1/22 * 1,

            "keywords": 1/44 * 1,
            "actors": 1/44 * 1,
            "directors": 1/44 * 1,
            "runtime": 1/44 * 1,
            "videos": 1/44 * 1,

            "og_lang": 1/100 * 1
        }

    sum = 0.0
    for val in weights.values():
        sum += val
    print(sum)


    transformers=[
            ("collection", OneHotEncoderTransformer(weight=weights["collection"]), "belongs_to_collection"),
            ("original_language", OneHotEncoderTransformer(weight=weights["og_lang"]), "original_language"),
            ("spoken_langugaes", MultiLabelBinarizerTransformer(weight=weights["spoken_languages"]), "spoken_languages"),
            ('genres', MultiLabelBinarizerTransformer(weight=weights["genres"]), "genres"),
            ("production_companies", MultiLabelBinarizerTransformer(weight=weights["production_companies"]), "production_companies"),
            ('actors', MultiLabelBinarizerTransformer(weight=weights["actors"]), "actors"),
            ('directors', MultiLabelBinarizerTransformer(weight=weights["directors"]), "directors"),
            ("keywords", TfidfVectorizerWrapper(weight=weights["keywords"] ), "keywords"),
            ("release_date", DateToTimestampTransformer(date_column="release_date", weight=weights["release_date"]), ["release_date"]),
            ("runtime", StandardScalerWrapper(weight=weights["runtime"]), ["runtime"]),
            ("videos", VideosCounterTransformer(weight=weights["videos"]), ["videos"]),

            ("companies_rating", MinMaxScalerWrapper(weight=weights["companies_rating"]), ["companies_rating"]),
            ("actors_rating", MinMaxScalerWrapper(weight=weights["actors_rating"]), ["actors_rating"]),
            ("directors_rating", MinMaxScalerWrapper(weight=weights["directors_rating"]), ["directors_rating"])
        ]


    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('knn', KNeighborsRegressor(n_neighbors=25))
    ])
    return model
