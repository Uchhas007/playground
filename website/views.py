from flask import Blueprint, render_template, request, session, redirect, flash
from . import db
from .models import (
    Resume, Certificates, XP, Contacts,
    Services, Skills, Language, Projects, CV, UserProfile,
)
from datetime import datetime
import uuid

views = Blueprint("views", __name__)


# ── Track unique sessions (lightweight) ───────────────────────────────────────
@views.before_request
def track_visitors():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())


# ── Public routes ─────────────────────────────────────────────────────────────

@views.route("/")
def home():
    user = UserProfile.query.first_or_404()
    return render_template("home.html", user=user)


@views.route("/resume")
def resume():
    r = Resume.query.all()
    cert = Certificates.query.all()
    user = UserProfile.query.first_or_404()
    cv = CV.query.order_by(CV.sno.desc()).first()
    return render_template("resume.html", user=user, r=r, c=cert, cv=cv)

@views.route("/services")
def services():
    service = Services.query.all()
    xp = XP.query.all()
    user = UserProfile.query.first_or_404()
    return render_template("services.html", user=user, s=service, e=xp)


@views.route("/skills")
def skills():
    skill = Skills.query.all()
    lang = Language.query.all()
    user = UserProfile.query.first_or_404()
    return render_template("skills.html", user=user, skills=skill, lang=lang)


@views.route("/projects")
def projects():
    project = Projects.query.all()
    user = UserProfile.query.first_or_404()
    return render_template("projects.html", user=user, p=project)


@views.route("/blog")
def myblog():
    user = UserProfile.query.first_or_404()
    return render_template("blog.html", user=user)


@views.route("/about")
def about():
    cv = CV.query.order_by(CV.sno.desc()).first()
    user = UserProfile.query.first_or_404()
    return render_template("about.html", user=user, cv=cv)


@views.route("/contact", methods=["GET", "POST"])
def contact():
    user = UserProfile.query.first_or_404()
    if request.method == "POST":
        entry = Contacts(
            name=request.form.get("name"),
            num=request.form.get("num"),
            email=request.form.get("email"),
            subject=request.form.get("subject"),
            msg=request.form.get("msg"),
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for contacting me! I'll get back to you soon.", "success")
        return redirect("/contact")
    return render_template("contact.html", user=user)


# ── 404 handler ───────────────────────────────────────────────────────────────
@views.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404