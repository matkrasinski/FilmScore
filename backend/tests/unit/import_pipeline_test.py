from ...database.util.import_pipeline import ImportPipeline
from ...database.util.update_pipeline import UpdatePipeline
from ...data.constant.COLUMNS import *


def test_import_pipeline():
    import_pipeline = ImportPipeline()
    assert len(import_pipeline.data) == 0

    import_pipeline.merge_tmdb_imdb(
        "left", tmdb_data="backend/tests/sample_data/tmdb_sample.csv",
        title_ratings="backend/tests/sample_data/title.ratings.tsv",
        title_crew="backend/tests/sample_data/title.crew.tsv",
        principals="backend/tests/sample_data/title.principals.tsv")
    assert len(import_pipeline.data) != 0

    import_pipeline.set_train_data()
    assert len(import_pipeline.train_data) != 0

    import_pipeline.set_new_data()
    assert len(import_pipeline.new_data) != 0

    import_pipeline.set_released_data()
    assert len(import_pipeline.data) != 0

    import_pipeline.run_predictions(
        model_path="backend/tests/sample_data/model.joblib")

    predictions = import_pipeline.new_data["predicted_rating"].to_list()

    assert all(value > -1 for value in predictions)
