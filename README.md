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

## Tech Stack
- Python 3
- Flask (web framework)
- SQLite (database)
- HTML, CSS (no JavaScript frameworks — kept simple on purpose)

## Project Structure
```
lost_found_flask_project/
│
├── app.py                 -> main Flask app (all routes/pages)
├── database.py             -> database connection & table setup
├── requirements.txt        -> Python packages needed
├── lostfound.db             -> SQLite database (created automatically on first run)
│
├── templates/               -> HTML pages
│   ├── base.html
│   ├── home.html
│   ├── report_form.html
│   ├── items.html
│   ├── item_detail.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
└── static/
    ├── css/style.css        -> styling for the whole site
    └── uploads/              -> uploaded item photos are saved here
```

The database file (`lostfound.db`) and its tables are created automatically
the first time you run the app — you don't need to set anything up manually.

## Admin Login
- URL: `/admin/login`
- Username: `admin`
- Password: `admin123`

## Notes
- Uploaded photos are stored in `static/uploads/`.
- This project intentionally keeps the code simple and readable
  (plain SQL queries, no ORM, no JS framework) since it is a BCA
  minor project meant to be explained during evaluation.
