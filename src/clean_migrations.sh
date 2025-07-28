
set -e

PROJECT_DIR="/home/xenox/Desktop/Saas-application/src"

source "$PROJECT_DIR/../venv/bin/activate"

echo "Removing __pycache__ directories and *.pyc files..."
find "$PROJECT_DIR" -name "__pycache__" -type d -exec rm -rf {} +
find "$PROJECT_DIR" -name "*.pyc" -type f -exec rm -f {} +
echo "Cache files removed."

echo "Removing migration files..."
find "$PROJECT_DIR" -path "*/migrations/*" -type f ! -name "__init__.py" -exec rm -f {} +
echo "Migration files removed."


echo "Creating new migrations..."
python manage.py makemigrations
echo "Migrations created."

echo "Applying migrations..."
python manage.py migrate
echo "Migrations applied successfully."

deactivate