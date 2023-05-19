echo "BUILD START"
pip install -r requirements.txt

echo "Make Migration..."
# python manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

python manage.py collectstatic --noinput --clear
echo "BUILD END"
