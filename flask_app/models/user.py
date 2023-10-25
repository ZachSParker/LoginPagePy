from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self,db_data) -> None:
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('user').query_db(query,data)
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL('user').query_db(query,data)
        return cls(result[0])
    @classmethod
    def check_credentials(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('user').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name'])< 2 :
            flash('First Name is too short, needs to be at least 2 characters')
            is_valid = False
        if len(user['last_name'])< 2:
                flash('First Name is too short, needs to be at least 2 characters')
                is_valid = False
        if not str.isalpha(user['first_name']):
            is_valid = False
        if not str.isalpha(user['last_name']):
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash('Invalid password, needs to be at least 8 characters')
        return is_valid