# Lost and Found System (Flask + SQLite)

A simple web application where students and staff can report lost items,
report found items, and search through all reported items.

## Features
- Report a lost item (with optional photo)
- Report a found item (with optional photo)
- Browse and search all items (by keyword, category, type, status)
- View full details of a single item
- Mark an item as claimed
- Admin panel to view and delete item records
- Works on mobile and desktop browsers

## Tech Stack
- Python 3
- Flask (web framework)
- SQLite (database)
- Jinja2 (templates)
- HTML, CSS

## Project Structure
```
lost_found_flask_project/
│
├── app.py                 -> main Flask app (all routes/pages)
├── database.py            -> database connection & table setup
├── requirements.txt       -> Python packages needed
├── .gitignore             -> files Git should ignore
├── README.md              -> this file
│
├── templates/             -> HTML pages
│   ├── base.html
│   ├── home.html
│   ├── report_form.html
│   ├── items.html
│   ├── item_detail.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
└── static/
    ├── css/style.css      -> styling for the whole site
    └── uploads/           -> uploaded item photos (created automatically)
```

`lostfound.db` (the SQLite database) is created automatically the first
time the app runs.

## Run Locally
```
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Admin Login
- URL: `/admin/login`
- Username: `admin`
- Password: `LostFound@2026`

## Deployment
The app is hosted on PythonAnywhere (free tier). It uses absolute file
paths so the database and uploads work from any working directory.
