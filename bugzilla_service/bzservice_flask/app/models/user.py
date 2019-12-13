from app import db, ma
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import validates, fields, ValidationError
from uuid import uuid4

class BugzillaUser(db.Model):
    __tablename__ = 'bzuser'
    _id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(120), nullable=False)
    apikey = db.Column(db.String(256))
    #bz_user_id = db.Column(db.String(256))
    #roles = db.Array()
    #groups = db.Array()


class BugzillaUserSchema(ma.ModelSchema):
    email = fields.Email(required=True)
    full_name = fields.Str(required=True)
    password = fields.Str(required=True)
    apikey = fields.Str(required=True)

    class Meta:
        model = BugzillaUser
 
