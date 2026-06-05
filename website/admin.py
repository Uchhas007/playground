from flask import (
    Blueprint, render_template, request, session,
    redirect, flash, url_for, abort,
)
from . import db
from .models import (
    Resume, Certificates, XP, Contacts,
    Services, Skills, Language, Projects, CV, UserProfile,
)
from datetime import datetime
import os
from functools import wraps

admin = Blueprint("admin", __name__)

# ── Credentials from env ──────────────────────────────────────────────────────
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme")

# ── Model registry ────────────────────────────────────────────────────────────
MODEL_MAP = {
    "resume": Resume,
    "certificates": Certificates,
    "xp": XP,
    "contacts": Contacts,
    "services": Services,
    "skills": Skills,
    "language": Language,
    "projects": Projects,
    "cv": CV,
}

# Human-readable labels for each model's columns
COLUMN_LABELS = {
    "resume": ["Date", "Degree / Title", "Institute / Organisation", "Description"],
    "certificates": ["Date", "Certificate Name", "Platform", "Description", "URL"],
    "xp": ["Date", "Role / Position", "Platform / Organisation", "Description"],
    "contacts": ["Name", "Phone", "Email", "Subject", "Message", "Date"],
    "services": ["Service Name", "Image Path", "Date"],
    "skills": ["Skill Name", "Percentage (0-100)"],
    "language": ["Language", "Percentage (0-100)"],
    "projects": ["Name", "Category", "Description", "Task Info", "GitHub URL", "Image Path"],
    "cv": ["Title", "File Path"],
}


# ── Auth decorator ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("admin_logged_in") != True:
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


def _ctx():
    """Common context passed to every admin template."""
    return {
        "user": UserProfile.query.first(),
        "contacts": Contacts.query.order_by(Contacts.date.desc()).limit(5).all(),
        "total_contacts": Contacts.query.count(),
        "projects": Projects.query.all(),
        "model_map": MODEL_MAP,
    }


# ── Login / Logout ────────────────────────────────────────────────────────────

@admin.route("/admin/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        entered_email = request.form.get("username", "").strip()
        entered_pass = request.form.get("password", "")

        if entered_email == ADMIN_EMAIL and entered_pass == ADMIN_PASS:
            session["admin_logged_in"] = True
            session["admin_email"] = entered_email
            flash("Welcome back!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")


@admin.route("/admin/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_email", None)
    flash("You have been logged out successfully.", "info")
    return redirect("/")


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin.route("/admin")
@login_required
def dashboard():
    ctx = _ctx()
    stats = {
        "projects": Projects.query.count(),
        "skills": Skills.query.count(),
        "contacts": Contacts.query.count(),
        "services": Services.query.count(),
        "xp": XP.query.count(),
        "certificates": Certificates.query.count(),
        "resume": Resume.query.count(),
    }
    recent_contacts = Contacts.query.order_by(Contacts.date.desc()).limit(5).all()
    return render_template(
        "admin_dashboard.html",
        stats=stats,
        recent_contacts=recent_contacts,
        **ctx,
    )


# ── Profile / Account Settings ────────────────────────────────────────────────

@admin.route("/admin/profile", methods=["GET", "POST"])
@login_required
def profile():
    ctx = _ctx()
    user = UserProfile.query.first()

    if request.method == "POST":
        user.fname = request.form.get("fname", user.fname)
        user.lname = request.form.get("lname", user.lname)
        user.profession = request.form.get("profession", user.profession)
        user.phone = request.form.get("phone", user.phone)
        user.email = request.form.get("email", user.email)
        user.born_day = request.form.get("born_day", user.born_day)
        user.born_month = request.form.get("born_month", user.born_month)
        user.born_year = request.form.get("born_year", user.born_year)
        user.sex = request.form.get("sex", user.sex)
        user.nationality = request.form.get("nationality", user.nationality)
        user.place = request.form.get("place", user.place)
        user.city = request.form.get("city", user.city)
        user.state = request.form.get("state", user.state)
        user.postal_code = request.form.get("postal_code", user.postal_code)
        user.country = request.form.get("country", user.country)
        user.planet = request.form.get("planet", user.planet)
        user.facebook = request.form.get("facebook", user.facebook)
        user.twitter = request.form.get("twitter", user.twitter)
        user.instagram = request.form.get("instagram", user.instagram)
        user.linkedin = request.form.get("linkedin", user.linkedin)
        user.github = request.form.get("github", user.github)
        user.no_of_projects = int(request.form.get("no_of_projects", user.no_of_projects or 0))
        user.awards = int(request.form.get("awards", user.awards or 0))
        user.customers = int(request.form.get("customers", user.customers or 0))
        user.coffee = int(request.form.get("coffee", user.coffee or 0))
        user.img_path = request.form.get("img_path", user.img_path)
        user.cv_path = request.form.get("cv_path", user.cv_path)

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("admin.profile"))

    return render_template("admin_profile.html", profile=user, **ctx)


# ── Generic List / View ───────────────────────────────────────────────────────

@admin.route("/admin/manage/<string:table_name>")
@login_required
def manage(table_name):
    model = MODEL_MAP.get(table_name.lower())
    if not model:
        abort(404)
    items = model.query.all()
    labels = COLUMN_LABELS.get(table_name.lower(), [])
    ctx = _ctx()
    return render_template(
        "admin_table.html",
        items=items,
        table_name=table_name,
        labels=labels,
        **ctx,
    )


# ── Add Item ──────────────────────────────────────────────────────────────────

@admin.route("/admin/add/<string:table_name>", methods=["GET", "POST"])
@login_required
def add_item(table_name):
    model = MODEL_MAP.get(table_name.lower())
    if not model:
        abort(404)

    ctx = _ctx()
    columns = [c for c in model.__table__.columns if c.name != "sno"]

    if request.method == "POST":
        new_data = {}
        for col in columns:
            if col.name.lower() == "date" and not request.form.get(col.name):
                new_data[col.name] = datetime.now().strftime("%Y-%m-%d")
            else:
                new_data[col.name] = request.form.get(col.name, "")
        new_item = model(**new_data)
        db.session.add(new_item)
        db.session.commit()
        flash(f"New entry added to {table_name}.", "success")
        return redirect(url_for("admin.manage", table_name=table_name))

    return render_template(
        "admin_form.html",
        table_name=table_name,
        columns=columns,
        item=None,
        action="Add",
        **ctx,
    )


# ── Edit Item ─────────────────────────────────────────────────────────────────

@admin.route("/admin/edit/<string:table_name>/<int:sno>", methods=["GET", "POST"])
@login_required
def edit_item(table_name, sno):
    model = MODEL_MAP.get(table_name.lower())
    if not model:
        abort(404)

    item = model.query.filter_by(sno=sno).first_or_404()
    ctx = _ctx()
    columns = [c for c in model.__table__.columns if c.name != "sno"]

    if request.method == "POST":
        for col in columns:
            val = request.form.get(col.name)
            if val is not None:
                setattr(item, col.name, val)
        db.session.commit()
        flash(f"Entry #{sno} updated in {table_name}.", "success")
        return redirect(url_for("admin.manage", table_name=table_name))

    return render_template(
        "admin_form.html",
        table_name=table_name,
        columns=columns,
        item=item,
        action="Edit",
        **ctx,
    )


# ── Delete Item ───────────────────────────────────────────────────────────────

@admin.route("/admin/delete/<string:table_name>/<int:sno>", methods=["POST"])
@login_required
def delete_item(table_name, sno):
    model = MODEL_MAP.get(table_name.lower())
    if not model:
        abort(404)
    item = model.query.filter_by(sno=sno).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash(f"Entry #{sno} deleted from {table_name}.", "warning")
    return redirect(url_for("admin.manage", table_name=table_name))


# ── Contacts detail view ──────────────────────────────────────────────────────

@admin.route("/admin/contact/<int:sno>")
@login_required
def view_contact(sno):
    ctx = _ctx()
    contact = Contacts.query.filter_by(sno=sno).first_or_404()
    return render_template("admin_contact_detail.html", contact=contact, **ctx)


@admin.route("/admin/contact/delete/<int:sno>", methods=["POST"])
@login_required
def delete_contact(sno):
    contact = Contacts.query.filter_by(sno=sno).first_or_404()
    db.session.delete(contact)
    db.session.commit()
    flash("Contact message deleted.", "warning")
    return redirect(url_for("admin.manage", table_name="contacts"))