from api.extensions import db
from ...data.constant.COLUMNS import COLLECTION_ID_COLUMN, PRIMARY_NAME_TMDB_COLUMN


class Collections(db.Model):
    __tablename__ = "Collections"
    collection_id = db.Column(db.String(255), primary_key=True)
    primary_name = db.Column(db.String(255))

    def __init__(self, collection_id, primary_name):
        self.collection_id = collection_id
        self.primary_name = primary_name

    def to_dict(self):
        return {
            COLLECTION_ID_COLUMN: self.collection_id,
            PRIMARY_NAME_TMDB_COLUMN: self.primary_name,
        }
