from backend.extensions import db
from ...data.constant.COLUMNS import PERSON_ID_COLUMN, PRIMARY_NAME_TMDB_COLUMN, RATING_COLUMN


class People(db.Model):
    __tablename__ = "People"
    person_id = db.Column(db.String(255), primary_key=True)
    primary_name = db.Column(db.String(255))
    rating = db.Column(db.Float)

    movies = db.relationship("MoviesPeople", back_populates="person")

    def __init__(self, person_id, primary_name, rating):
        self.person_id = person_id
        self.primary_name = primary_name
        self.rating = rating

    def to_dict(self):
        return {
            PERSON_ID_COLUMN: self.person_id,
            PRIMARY_NAME_TMDB_COLUMN: self.primary_name,
            RATING_COLUMN: self.rating,
        }
