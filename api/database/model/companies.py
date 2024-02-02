from api.extensions import db
from ...data.constant.COLUMNS import COMPANY_ID_COLUMN, COMPANY_NAME_COLUMN, RATING_COLUMN


class Companies(db.Model):
    __tablename__ = "Companies"
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    rating = db.Column(db.Float)

    movies = db.relationship("MoviesCompanies", back_populates="company")

    def __init__(self, company_id, company_name, rating):
        self.company_id = company_id
        self.company_name = company_name
        self.rating = rating

    def to_dict(self):
        return {
            COMPANY_ID_COLUMN: self.company_id,
            COMPANY_NAME_COLUMN: self.company_name,
            RATING_COLUMN: self.rating,
        }

    def to_simple_dict(self):
        return {COMPANY_ID_COLUMN: self.company_id, COMPANY_NAME_COLUMN: self.company_name}
