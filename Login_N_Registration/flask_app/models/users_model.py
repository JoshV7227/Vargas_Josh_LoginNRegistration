from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, request
from icecream import ic
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



#------------------------------ USER CLASS


class User:
    DB = 'Login_and_Registration_schema'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']









#------------------------------ CREATE USER

    @classmethod
    def save_user(cls,data):

        #QUERY TO CREATE USER, ALREADY VALIDATED AT THIS POINT
        query = """
        INSERT INTO users(first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        #HASHING THE PASSWORD WITH BCRYPT
        password_hashed = bcrypt.generate_password_hash(request.form['password'])


        #TAKING THE FORM AND PREPARING IT TO SUBMIT THE QUERY
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : password_hashed
        }


        #SUBMITTING THE QUERY TO THE DATABASE AND RETURNING AS 'RESULTS'
        results = connectToMySQL(cls.DB).query_db(query,data)


        return results
    





#------------------------------ GET USER BY EMAIL


    @classmethod
    def get_by_email(cls,data):


        #SETTING UP QUERY AND GETTING ALL FROM USERS WITH EMAIL
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """

        #SUBMITTING REQUEST TO DATABASE
        result = connectToMySQL(cls.DB).query_db(query,data)


        #IF NO IS USER FOUND
        if len(result) < 1:
            return False
        

        #WE RETURN THE CLASS INSTANCE OF THE FIRST ITEM IN THE DICTIONARY
        return cls(result[0])








    #------------------------------REGISTRATION VALIDATER
    @staticmethod
    def validate_registration(data):

        is_valid = True 

        if len(data['first_name']) < 3:
            flash("Name must be at least 3 characters. You are not 'IT'...you clown..lol")
            is_valid = False

        if len(data['last_name']) < 3:
            flash("Last Name must be at least 3 characters")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        if len(data['password']) < 8:
            flash("Passwords must be at least 8 characters")
            is_valid = False

        if (data['password']) != (data['confirm_password']):
            flash("Somethin's up with your passwords, Try again bud")
            is_valid = False

        return is_valid