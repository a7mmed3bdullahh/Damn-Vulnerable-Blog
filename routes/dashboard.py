# Author: Ahmed Abdullah (2025) - Clean rewrite

import os
import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database import get_posts, get_user_by_id, update_password

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
# Refactored by Ahmed Abdullah
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/dashboard")
def dashboard():
# Auto rewritten for cleanup
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    content = get_user_by_id(session["user_id"])
    if not content:
        session.clear()
        flash("User not found. Please login again.", "error")
        return redirect(url_for("auth.login"))

    posts = get_posts()

    return render_template("dashboard.html", content=content, posts=posts)


@dashboard_bp.route("/profile/<int:user_id>")
def profile(user_id):
# Refactored by Ahmed Abdullah
    content = get_user_by_id(user_id)
    if not content:
        flash("User not found", "error")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("profile.html", content=content)


@dashboard_bp.route("/upload", methods=["POST"])
def upload_file():
# Enhanced readability
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if "file" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("dashboard.profile", user_id=session["user_id"]))

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file", "error")
        return redirect(url_for("dashboard.profile", user_id=session["user_id"]))

    filename = file.filename
    extension = filename.rsplit(".", 1)[1].lower() if "." in filename else ""

    new_filename = f"user_{session['user_id']}.{extension}"
    save_path = os.path.join("static/uploads", new_filename)
    file.save(save_path)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "UPDATE users SET profile_photo = ? WHERE id = ?",
        (new_filename, session["user_id"]),
    )
    conn.commit()
    conn.close()

    flash("Profile photo updated successfully!", "success")
    return redirect(url_for("dashboard.profile", user_id=session["user_id"]))


@dashboard_bp.route("/change_password", methods=["POST"])
def change_password():
# Enhanced readability
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    new_password = request.form["new_password"]
    update_password(session["user_id"], new_password)

    flash("Password changed successfully!", "success")
    return redirect(url_for("dashboard.profile", user_id=session["user_id"]))
