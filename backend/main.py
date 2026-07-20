from flask import Flask, jsonify, request, make_response, render_template, flash, redirect, send_from_directory, url_for
from config import app, db
from models import Product
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os, base64


def get_admin_emails():
    return [email.strip() for email in os.environ.get('ADMIN_EMAILS', '').split(',') if email.strip()]


def get_admin_password():
    return os.environ.get('ADMIN_PASSWORD', '')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    # Helper to reliably extract Basic Auth credentials and validate them
    def is_authenticated():
        # Accept either an active session or Basic Auth header
        from flask import session
        if session.get('is_admin'):
            return True

        auth = request.authorization
        if not auth:
            header = request.headers.get('Authorization')
            if header and header.lower().startswith('basic '):
                try:
                    b64 = header.split(' ', 1)[1]
                    decoded = base64.b64decode(b64).decode()
                    username, password = decoded.split(':', 1)
                    class _A: pass
                    auth = _A()
                    auth.username = username
                    auth.password = password
                except Exception:
                    return False
        admin_emails = get_admin_emails()
        admin_password = get_admin_password()
        return bool(auth and auth.username in admin_emails and auth.password == admin_password)

    if request.method == 'GET':
        # If already authenticated render form
        if is_authenticated():
            return render_template('products.html')
        # Not authenticated: respond with 401 + WWW-Authenticate to trigger Basic Auth prompt
        resp = make_response('Could not verify!', 401)
        resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
        return resp

    if request.method == 'POST':
        # Require authentication for POST as well; return 401 to trigger Basic Auth if needed
        if not is_authenticated():
            resp = make_response('Could not verify!', 401)
            resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
            return resp

        name = request.form.get('productName')
        descript = request.form.get('productDesc')
        img_file = request.files.get('productImg')
        price = request.form.get('productPrice')

        if not (name and descript and img_file and price):
            flash('Missing data. Please fill all product fields.', 'error')
            return redirect(url_for('add_item'))

        # Validate price
        try:
            price_val = float(price)
        except ValueError:
            flash('Invalid price value.', 'error')
            return redirect(url_for('add_item'))

        # Save image safely
        img_filename = secure_filename(img_file.filename)
        img_path = os.path.join(app.static_folder, 'gqs_images', img_filename)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        img_file.save(img_path)

        # Add to database with error handling for unique constraint
        new_product = Product(name=name, descript=descript, img=f'gqs_images/{img_filename}', price=price_val)
        db.session.add(new_product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('A product with that name already exists. Choose a different name.', 'error')
            return redirect(url_for('add_item'))
        except Exception:
            db.session.rollback()
            flash('An unexpected error occurred while saving the product.', 'error')
            return redirect(url_for('add_item'))

        flash('Product added successfully!', 'success')
        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Simple session-based login fallback for browsers
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    admin_emails = get_admin_emails()
    admin_password = get_admin_password()
    if username in admin_emails and password == admin_password:
        from flask import session
        session['is_admin'] = True
        flash('Logged in successfully.', 'success')
        return redirect(url_for('add_item'))

    flash('Invalid credentials.', 'error')
    return redirect(url_for('login'))


@app.route('/debug-auth')
def debug_auth():
    # Debug endpoint (debug-only) that reports whether an Authorization header is present
    if not app.debug:
        return jsonify({'error': 'Not available'}), 404

    header = request.headers.get('Authorization')
    info = {'has_authorization_header': bool(header)}

    auth = request.authorization
    if auth:
        info['parsed_username'] = auth.username
        info['password_present'] = bool(auth.password)
    elif header and header.lower().startswith('basic '):
        try:
            b64 = header.split(' ', 1)[1]
            decoded = base64.b64decode(b64).decode()
            username, password = decoded.split(':', 1)
            info['decoded_username'] = username
            info['password_present'] = bool(password)
        except Exception as e:
            info['decode_error'] = str(e)

    return jsonify(info)


@app.route('/api/products')
def get_products():
    products = Product.query.all()
    return jsonify([{'name': p.name, 'img': p.img, 'descript': p.descript, 'price': p.price} for p in products])

#This main.py file uses a GET and POST route in the same function. The GET function retrieves the data of the webpage meanwhile the 
#POST function adds data to the database after verifying the user credentials.
@app.route('/proddets.html')
@app.route('/proddets')
def product_details():
    return render_template('proddets.html')

# Contact page routes (support both /contact and /contact.html)
@app.route('/Contact')
@app.route('/Contact.html')
def contact_page():
    return render_template('Contact.html')
@app.route('/about')
@app.route('/about.html')
def about_page():
    return render_template('about.html') 
@app.route('/index.html')
@app.route('/index')
def index_page():
    return render_template('index.html')