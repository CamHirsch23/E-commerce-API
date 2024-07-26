# Initialize a new Flask project
mkdir ecommerce_app
cd ecommerce_app

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Flask, Flask-SQLAlchemy, and Flask-Marshmallow
pip install Flask Flask-SQLAlchemy Flask-Marshmallow mysql-connector-python
