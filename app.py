"""
app.py
------
This is the main file that runs the Lost and Found website.

It uses Flask, which is a lightweight Python web framework.
Each "route" below is one page or one action on the website.

To run this project:
    1. Install Flask -> pip install flask
    2. Run this file  -> python app.py
    3. Open your browser at http://127.0.0.1:5000
"""

import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from database import get_connection, init_db, init_admin_table

# ---------------------------------------------------------
# Basic app setup
# ---------------------------------------------------------
app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # needed for flash messages & admin login

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    """Checks if the uploaded file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Create the database tables (only creates them if they don't exist yet)
init_db()
init_admin_table()


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------
@app.route("/")
def home():
    """Shows the homepage with two options: report lost item / report found item,
    plus a quick look at the most recent items."""
    conn = get_connection()
    recent_items = conn.execute(
        "SELECT * FROM items ORDER BY id DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("home.html", items=recent_items)


# ---------------------------------------------------------
# Report a Lost or Found Item (same form is reused for both)
# ---------------------------------------------------------
@app.route("/report/<item_type>", methods=["GET", "POST"])
def report_item(item_type):
    """
    item_type will be either 'lost' or 'found'.
    GET  -> show the empty form
    POST -> save the submitted form data into the database
    """
    if item_type not in ("lost", "found"):
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]
        location = request.form["location"]
        reporter_name = request.form["reporter_name"]
        reporter_contact = request.form["reporter_contact"]
        today = date.today().strftime("%Y-%m-%d")

        # Handle the optional image upload
        image_filename = None
        file = request.files.get("image")
        if file and file.filename != "" and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            # Add item_type + title so filenames don't clash with each other
            image_filename = f"{item_type}_{title}_{image_filename}".replace(" ", "_")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        conn = get_connection()
        conn.execute("""
            INSERT INTO items
            (item_type, title, category, description, location,
             date_reported, reporter_name, reporter_contact, image_filename, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'unresolved')
        """, (item_type, title, category, description, location,
              today, reporter_name, reporter_contact, image_filename))
        conn.commit()
        conn.close()

        flash(f"Your {item_type} item report was submitted successfully!", "success")
        return redirect(url_for("home"))

    # GET request -> just show the form
    return render_template("report_form.html", item_type=item_type)


# ---------------------------------------------------------
# Browse / Search all items
# ---------------------------------------------------------
@app.route("/items")
def view_items():
    """
    Shows all reported items.
    Supports optional search/filter using URL query parameters:
        /items?keyword=bottle&category=Electronics&item_type=lost&status=unresolved
    """
    keyword = request.args.get("keyword", "").strip()
    category = request.args.get("category", "")
    item_type = request.args.get("item_type", "")
    status = request.args.get("status", "")

    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    if category:
        query += " AND category = ?"
        params.append(category)

    if item_type:
        query += " AND item_type = ?"
        params.append(item_type)

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    conn = get_connection()
    items = conn.execute(query, params).fetchall()
    # Used to fill the category dropdown in the search form
    categories = conn.execute("SELECT DISTINCT category FROM items").fetchall()
    conn.close()

    return render_template(
        "items.html",
        items=items,
        categories=categories,
        keyword=keyword,
        selected_category=category,
        selected_type=item_type,
        selected_status=status,
    )


# ---------------------------------------------------------
# View a single item's full details
# ---------------------------------------------------------
@app.route("/item/<int:item_id>")
def item_detail(item_id):
    conn = get_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()

    if item is None:
        flash("That item does not exist.", "error")
        return redirect(url_for("view_items"))

    return render_template("item_detail.html", item=item)


# ---------------------------------------------------------
# Mark an item as claimed
# ---------------------------------------------------------
@app.route("/item/<int:item_id>/claim", methods=["POST"])
def mark_claimed(item_id):
    conn = get_connection()
    conn.execute("UPDATE items SET status = 'claimed' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    flash("Item marked as claimed.", "success")
    return redirect(url_for("item_detail", item_id=item_id))


# ===========================================================
# ADMIN SECTION (optional module)
# ===========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        admin = conn.execute(
            "SELECT * FROM admin WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if admin:
            session["is_admin"] = True
            flash("Welcome back, admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect username or password.", "error")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


def admin_required():
    """Small helper function to check if the current user is logged in as admin."""
    return session.get("is_admin", False)


@app.route("/admin")
def admin_dashboard():
    if not admin_required():
        flash("Please log in as admin first.", "error")
        return redirect(url_for("admin_login"))

    conn = get_connection()
    items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("admin_dashboard.html", items=items)


@app.route("/admin/delete/<int:item_id>", methods=["POST"])
def admin_delete_item(item_id):
    if not admin_required():
        flash("Please log in as admin first.", "error")
        return redirect(url_for("admin_login"))

    conn = get_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    flash("Item deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ---------------------------------------------------------
# Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
