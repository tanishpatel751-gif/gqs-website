# ECommerce Website

A simple Flask-based e-commerce style website with a product catalog, about/contact pages, and an admin add-product flow.

## Features

- Home page and product listing views
- Product detail page
- About and contact pages
- Admin-only product creation form
- SQLite database for local development

## Project Structure

- backend/ - Flask backend and database models
- frontend/ - HTML templates and static assets
- .env.example - example environment variables
- .gitignore - ignores local secrets and database files

## Requirements

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-CORS

## Setup

1. Create and activate a virtual environment
2. Install the required packages
3. Copy .env.example to .env and update the values
4. Run the Flask app

Example:

```bash
python -m venv venv
venv\Scripts\activate
pip install flask flask-sqlalchemy flask-cors
copy .env.example .env
python backend\config.py
```

## Environment Variables

Create a local .env file with the following values:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///site.db
ADMIN_EMAILS=admin@example.com
ADMIN_PASSWORD=your-strong-password
```

Do not commit your real .env file.

## Notes

- The project uses SQLite for local development.
- The admin credentials are read from environment variables for security.
- Keep your .env file local and never upload it to GitHub.
