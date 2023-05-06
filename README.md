# Get started
## 1. Clone this repository
```git clone https://github.com/mendrika261/S4-SI-entreprise.git```
## 2. Create a virtual environment
```python -m venv venv```
## 3. Activate the virtual environment
```source venv/bin/activate```
## 4. Install requirements
```pip install -r requirements.txt```
## 5. Configure the database
Create a file named `.env` and add the following variables:
```
# Database configuration
ERP_DB_NAME=postgres
ERP_DB_USER=postgres
ERP_DB_PASSWORD=
ERP_DB_HOST=localhost
ERP_DB_PORT=5432
```
## 6. Make migrations
```python manage.py makemigrations```
## 7. Migrate
```python manage.py migrate```
## 8. Insert data
Insert data into the database with sql script in `sql/` folder
## 9. Create a superuser for login
```python manage.py createsuperuser <username>```
## 10. Run the server
```python manage.py runserver```
