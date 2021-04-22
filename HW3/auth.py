import os
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user
from flask import Flask, render_template, request, make_response, abort, redirect, session, url_for, flash

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.urandom(16).hex()

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(username):
    return User(username=username, password=users[username])

users= {
    "Anya": "123",
    "guest": "qwe",
    "student": "sit"
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            user = User(username=username, password=password)
            login_user(user)
            return redirect('/cabinet')
        else:
            return redirect('/invalid')
    return render_template('login.html')

@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/invalid')
def invalid():
    return render_template('invalid.html')

# Return static images and files on http://localhost:5000/static/<image_name>
@app.route('/static/<path:filename>')
def show_files_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)