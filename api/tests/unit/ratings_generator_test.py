from ...data.util.ratings_generator import RatingsGenerator
from .data_imputer_test import prepare_sample_data
import pandas as pd


def test_people_ratings_genearator():
    sample_data = pd.read_csv("api/tests/sample_data/tmdb_sample.csv")
    sample_data = prepare_sample_data(sample_data)

    ratings_generator = RatingsGenerator()
    assert len(ratings_generator.people_ratings) == 0
    ratings_generator.generate_people_ratings(sample_data)

    assert len(ratings_generator.people_ratings) == 25


def test_companies_ratings_genearator():
    sample_data = pd.read_csv("api/tests/sample_data/tmdb_sample.csv")
    sample_data = prepare_sample_data(sample_data)
    sample_data["production_companies"] = sample_data["production_companies"].apply(
        lambda x: x.split("|"))

    ratings_generator = RatingsGenerator()
    assert len(ratings_generator.companies_ratings) == 0
    ratings_generator.generate_companies_ratings(sample_data)

    assert len(ratings_generator.companies_ratings) == 16
