from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="static",
        template_folder="templates",
    )

    # ── Secret key ────────────────────────────────────────────────────────────
    app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

    # ── Database (Neon PostgreSQL) ────────────────────────────────────────────
    DATABASE_URL = os.environ.get("DATABASE_URL", "")

    # Neon / older Heroku-style postgres:// → postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Strip inline sslmode param — handled via connect_args
    DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "").replace(
        "&sslmode=require", ""
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"},
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ── Mail ──────────────────────────────────────────────────────────────────
    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    )

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    Mail(app)
    app.jinja_env.globals.update(getattr=getattr)

    # ── Blueprints ────────────────────────────────────────────────────────────
    from .views import views
    from .admin import admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")

    # ── Create tables & seed ──────────────────────────────────────────────────
    from .models import (
        Resume, Certificates, XP, Contacts,
        Services, Skills, Language, Projects, CV, UserProfile,
    )

    with app.app_context():
        db.create_all()
        _seed(db)

    return app


# ── Seed helper ───────────────────────────────────────────────────────────────
def _seed(db):
    """Insert initial data only when tables are empty."""
    from .models import (
        Resume, Certificates, XP, Contacts,
        Services, Skills, Language, Projects, CV, UserProfile,
    )

    if not Projects.query.first():
        db.session.add_all([
            Projects(name="TextUtils", category="Web development in Django",
                     description="A website that converts text in various ways.",
                     task_info="Include binary conversion of texts.",
                     url="https://github.com/Uchhas007/Text-Utils.git",
                     img_file="images/project1.png"),
            Projects(name="Snake Game", category="Game Development in Pygame",
                     description="An interactive, fun and classic snake game.",
                     task_info="Resolve the errors",
                     url="https://github.com/Uchhas007/Snake-Game.git",
                     img_file="images/project2.png"),
            Projects(name="Drizzler", category="Web Development in Django",
                     description="A weather forecasting app",
                     task_info="Have to make it more robust and change the API key",
                     url="https://github.com/Uchhas007/Drizzler.git",
                     img_file="images/project3.jpg"),
            Projects(name="Ami Bolsi", category="Web Development in Flask",
                     description="A personal Blogging site",
                     task_info="Change the layout and make it more secured and interactive.",
                     url="https://github.com/Uchhas007/ami-bolsi.git",
                     img_file="images/project-4.jpg"),
            Projects(name="Aurete Adhyay", category="Web Development in Flask",
                     description="An inventory website of a bookstore",
                     task_info="Use Blueprint",
                     url="https://github.com/Uchhas007/Aureate-Adhyay.git",
                     img_file="images/project-5.jpg"),
        ])
        db.session.commit()

    if not Services.query.first():
        db.session.add_all([
            Services(name="Back-End Web Development in Django and/or Flask",
                     image_file="images/backend.jpg", date="2025-05-28"),
            Services(name="Machine Learning",
                     image_file="images/ml.jpg", date="2025-05-28"),
            Services(name="Front-End Web Development",
                     image_file="images/frontend.jpg", date="2025-05-28"),
        ])
        db.session.commit()

    if not XP.query.first():
        db.session.add_all([
            XP(date="07/2019 - 04/2021", name="Joint Secretary (Day Shift)",
               platform="Remians Art Club - Dhaka Residential Model College",
               description="As the Joint Secretary of the Remians Art Club, I coordinated events, mentored junior members, and organized art exhibitions to foster creativity."),
            XP(date="06/2023 - 02/2024", name="Apprentice",
               platform="Robotics Club of BRAC University",
               description="As an apprentice in the Finance and Marketing department, I supported event budgeting and promoted club activities through digital platforms."),
            XP(date="02/2024 - 08/2024", name="Junior Executive",
               platform="Robotics Club of BRAC University",
               description="As a Junior Executive in Finance and Marketing at the Robotics Club, I led sponsorship outreach and managed budgeting for tech events."),
            XP(date="05/2024 - 06/2024", name="Campus Ambassador",
               platform="G17 Global",
               description="As a Campus Ambassador for the G17 - Bangladesh, I promoted the organization's mission, engaged students in SDG initiatives, and facilitated campus events."),
            XP(date="06/2024 - 04/2025", name="Campus Director",
               platform="G17 Global",
               description="As the Campus Director for G17 – Bangladesh at BRAC University, I led SDG-related campaigns, coordinated student involvement, and strengthened partnerships."),
            XP(date="04/2025 - 05/2025", name="Machine Learning Intern",
               platform="CodSoft",
               description="I developed customized algorithms to enable critical business insights and collaborated on predictive analytics solutions using Python and ML frameworks."),
            XP(date="04/2025 - 06/2025", name="Machine Learning Intern",
               platform="CodeAlpha",
               description="I designed and implemented customized machine learning models to solve classification problems and improved model accuracy through iterative testing."),
        ])
        db.session.commit()

    if not Language.query.first():
        db.session.add_all([
            Language(lang="Bengali", percentage="97"),
            Language(lang="English", percentage="95"),
        ])
        db.session.commit()

    if not Skills.query.first():
        db.session.add_all([
            Skills(name="Python", percentage="90"),
            Skills(name="Java", percentage="65"),
            Skills(name="HTML, CSS and JS", percentage="70"),
            Skills(name="Bootstrap", percentage="95"),
            Skills(name="Database management using MySQL", percentage="90"),
            Skills(name="Back End Web Development using Flask", percentage="90"),
            Skills(name="Back End Web Development using Django", percentage="90"),
            Skills(name="Machine Learning", percentage="75"),
        ])
        db.session.commit()

    if not CV.query.first():
        db.session.add(CV(
            title="Uchhas Saha - Resume",
            file="files/myresume (null).pdf",
        ))
        db.session.commit()

    if not Certificates.query.first():
        db.session.add_all([
            Certificates(date="09/2024 - Present", name="Python (Basic) Certificate",
                         platform="HackerRank",
                         description="Certified in Python fundamentals including Scalar types, Conditionals, Loops, Functions, and Built-in Methods.",
                         url="https://www.hackerrank.com/certificates/iframe/679"),
            Certificates(date="09/2024 - Present", name="Java (Basic) Certificate",
                         platform="HackerRank",
                         description="Covered core Java topics such as classes, data structures, and OOP fundamentals.",
                         url="https://www.hackerrank.com/certificates/iframe/d36"),
            Certificates(date="09/2024 - Present", name="Problem Solving (Basic)",
                         platform="HackerRank",
                         description="Achieved certification covering fundamental Data Structures and Algorithms.",
                         url="https://www.hackerrank.com/certificates/iframe/2d2"),
            Certificates(date="09/2024 - Present", name="Problem Solving (Intermediate)",
                         platform="HackerRank",
                         description="Achieved certification covering Data Structures (e.g., Stacks, Queues) and Algorithm design patterns.",
                         url="https://www.hackerrank.com/certificates/iframe/696"),
            Certificates(date="05/2025 - Present", name="SQL (Basic) Certificate",
                         platform="HackerRank",
                         description="Achieved certification covering basic SQL Commands and query operations.",
                         url="https://www.hackerrank.com/certificates/iframe/e2c"),
            Certificates(date="05/2025 - Present", name="Software Engineer",
                         platform="HackerRank",
                         description="Achieved certification covering advanced topics like system design, coding assessments, and OOP.",
                         url="https://www.hackerrank.com/certificates/iframe/84b"),
        ])
        db.session.commit()

    if not Resume.query.first():
        db.session.add_all([
            Resume(date="2021 - Present",
                   degree="BSc in Computer Science",
                   institute="BRAC University, Dhaka",
                   description="Studying Computer Science and Engineering with focus on software development, data structures, algorithms, and machine learning."),
            Resume(date="2019 - 2021",
                   degree="Higher Secondary Certificate (HSC)",
                   institute="Dhaka Residential Model College",
                   description="Completed HSC in Science with strong academic performance in Mathematics, Physics, and Chemistry."),
        ])
        db.session.commit()

    if not UserProfile.query.first():
        import os
        user = UserProfile(
            fname=os.environ.get("FNAME", "Uchhas"),
            lname=os.environ.get("LNAME", "Saha"),
            born_month=os.environ.get("BORN_MONTH", "April"),
            born_day=os.environ.get("BORN_DAY", "9th"),
            born_year=int(os.environ.get("BORN_YEAR", 2004)),
            sex=os.environ.get("SEX", "Male"),
            nationality=os.environ.get("NATIONALITY", "Bangladeshi"),
            place=os.environ.get("ADDR_STREET", "Tajmahal Rd."),
            city=os.environ.get("ADDR_CITY", "Dhaka"),
            state=os.environ.get("ADDR_AREA", "Mohammadpur"),
            postal_code=os.environ.get("ADDR_ZIP", "1207"),
            country=os.environ.get("ADDR_COUNTRY", "Bangladesh"),
            planet=os.environ.get("ADDR_UNIT", "C-137"),
            img_path=os.environ.get("IMG_PATH", "images/bg_1.png"),
            profession=os.environ.get("PROF", "Undergrad CS student"),
            email=os.environ.get("ADMIN_EMAIL", "admin@example.com"),
            username=os.environ.get("USERNAME", "admin"),
            password=os.environ.get("ADMIN_PASS", "changeme"),
            phone=os.environ.get("PHONE", "+880 1715 123456"),
            facebook=os.environ.get("FACEBOOK", "#"),
            twitter=os.environ.get("TWITTER", "#"),
            instagram=os.environ.get("INSTAGRAM", "#"),
            linkedin=os.environ.get("LINKEDIN", "#"),
            github=os.environ.get("GITHUB", "#"),
            no_of_projects=int(os.environ.get("NO_OF_PROJECTS", 5)),
            awards=int(os.environ.get("AWARDS", 7)),
            customers=int(os.environ.get("CUSTOMERS", 0)),
            coffee=int(os.environ.get("COFFEE", 0)),
            cv_path=os.environ.get("CV", "files/myresume (null).pdf"),
        )
        db.session.add(user)
        db.session.commit()