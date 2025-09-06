from sqlalchemy import Column, Integer, ForeignKey, String,BigInteger
from sqlalchemy.orm import relationship
from . import db
class UserSkills(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    skill_id = db.Column(db.String, db.ForeignKey("skills.id"), nullable=False)

    user = db.relationship("User", back_populates="skills")
    skill = db.relationship("Skill", back_populates="users")