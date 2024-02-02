from api.extensions import db
from ...data.constant.COLUMNS import PERSON_ID_COLUMN, MOVIE_ID_COLUMN


class MoviesPeople(db.Model):
    __tablename__ = "Movies_People"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(
        PERSON_ID_COLUMN, db.String(255), db.ForeignKey("People.person_id")
    )
    movie_id = db.Column(MOVIE_ID_COLUMN, db.String(255),
                         db.ForeignKey("Movies.imdb_id"))
    category = db.Column(db.String(255))

    movie = db.relationship("Movies", back_populates="people")
    person = db.relationship("People", back_populates="movies")

    def __init__(self, movie_id, person_id, category):
        self.movie_id = movie_id
        self.person_id = person_id
        self.category = category

    def save(self):
        db.session.commit()
