from flask_app import app 
from flask_app.controllers import users_control
from flask import render_template, session, redirect




@app.route('/')
def index():

    return render_template('index.html')


#The next step is creating the validations, we have created the register
#part. The display html could use a little work








if __name__ == '__main__':
    app.run(debug=True,port=5001)