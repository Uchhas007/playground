from . import db
from datetime import datetime


class Resume(db.Model):
    __tablename__ = "resume"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(25), nullable=False)
    degree = db.Column(db.String(250), nullable=False)
    institute = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1500), nullable=False)


class Certificates(db.Model):
    __tablename__ = "certificates"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    url = db.Column(db.String(5000), nullable=False)


class XP(db.Model):
    __tablename__ = "xp"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)


class Contacts(db.Model):
    __tablename__ = "contacts"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    num = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    msg = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(20), nullable=True)


class Services(db.Model):
    __tablename__ = "services"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    image_file = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(100), nullable=True)


class Skills(db.Model):
    __tablename__ = "skills"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    percentage = db.Column(db.String(500), nullable=False)


class Language(db.Model):
    __tablename__ = "language"
    sno = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(250), nullable=False)
    percentage = db.Column(db.String(20), nullable=False)


class Projects(db.Model):
    __tablename__ = "projects"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1200), nullable=False)
    task_info = db.Column(db.String(1200), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    img_file = db.Column(db.String(500), nullable=False)


class CV(db.Model):
    __tablename__ = "cv"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5250), nullable=False)
    file = db.Column(db.String(1000), nullable=False)


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    born_month = db.Column(db.String(20))
    born_day = db.Column(db.String(10))
    born_year = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    nationality = db.Column(db.String(50))

    place = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(50))
    planet = db.Column(db.String(50))   # apartment / unit

    img_path = db.Column(db.String(200))
    profession = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(20))

    facebook = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))

    no_of_projects = db.Column(db.Integer, default=0)
    awards = db.Column(db.Integer, default=0)
    customers = db.Column(db.Integer, default=0)
    coffee = db.Column(db.Integer, default=0)

    cv_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)