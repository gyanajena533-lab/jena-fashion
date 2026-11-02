JENA FASHION - UPDATED FLASK SHOP
=================================

FEATURES
- Existing Jena Fashion burgundy/cream storefront design retained.
- Product catalogue, search and category filter.
- Product details, stock display, cart add/update/remove.
- Customer registration, login/logout and order history.
- Checkout with Cash on Delivery (COD).
- Admin product create/edit/delete and order status management.
- Customer ratings and reviews (one review per customer per product).
- SQLite database; starter products are added automatically to an empty database.

REQUIREMENTS
Python 3.10+ recommended. Open PowerShell in this folder.

WINDOWS SETUP
1. Open this extracted folder in Visual Studio Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   py -m venv .venv
4. Activate it:
   .venv\Scripts\Activate.ps1
   If PowerShell blocks activation, run this once in that terminal:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   Then activate again.
5. Install packages:
   python -m pip install -r requirements.txt
6. Set an admin login BEFORE starting the app (PowerShell):
   $env:JENA_ADMIN_EMAIL="your-email@example.com"
   $env:JENA_ADMIN_PASSWORD="choose-a-strong-password"
   $env:SECRET_KEY="replace-with-a-long-random-secret"
7. Start:
   python app.py
8. Open http://127.0.0.1:5000
9. Log in using the admin email and password from step 6. Open Admin in the top menu.

IMPORTANT
- The admin account is created only on first startup when JENA_ADMIN_EMAIL and
  JENA_ADMIN_PASSWORD are set and that email does not already exist.
- Existing SQLite data is kept. Back up instance/jena_fashion.db before replacing
  project files or changing database models.
- Online payment is NOT active. Checkout currently supports Cash on Delivery.
  Razorpay needs a merchant account, API keys, server-side order creation and
  payment signature verification before real payments should be accepted.
- Change SECRET_KEY before deployment. Never publish your secret, admin password,
  database, or customer data in a public repository or ZIP.
- For production, use HTTPS, secure cookie settings, database backups, CSRF
  protection on all forms, rate limiting, validated image uploads and a managed
  production database. This starter is not yet a fully audited production store.
- Starter product images are external Unsplash URLs; replace them with product
  photos you own or have permission to use.

RENDER / DEPLOYMENT
Set these environment variables in your host:
SECRET_KEY = a long random secret
JENA_ADMIN_EMAIL = your admin email
JENA_ADMIN_PASSWORD = a strong unique password
DATABASE_URL = your persistent PostgreSQL database URL (if provided by host)
Start command: gunicorn app:app
SQLite on temporary hosting may be erased during redeploy; use persistent PostgreSQL.
