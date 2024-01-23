from flask_app import app 
from flask_app.controllers import users_control
from flask import render_template, session, redirect




@app.route('/')
def index():

    return render_template('index.html')







if __name__ == '__main__':
    app.run(debug=True,port=5001)