from api.extensions import db
from ...data.constant.COLUMNS import MOVIE_ID_COLUMN, COMPANY_ID_COLUMN


class MoviesCompanies(db.Model):
    __tablename__ = "Movies_Companies"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        COMPANY_ID_COLUMN, db.Integer, db.ForeignKey("Companies.company_id")
    )
    movie_id = db.Column(MOVIE_ID_COLUMN, db.String(255),
                         db.ForeignKey("Movies.tmdb_id"))

    movie = db.relationship("Movies", back_populates="companies")
    company = db.relationship("Companies", back_populates="movies")

    def __init__(self, id, company_id, movie_id, movie, company):
        self.id = id
        self.company_id = company_id
        self.movie_id = movie_id
        self.movie = movie
        self.company = company
