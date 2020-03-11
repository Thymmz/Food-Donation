from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import os
from db import Database


app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'lkj98t&%$3rhfSwu3D'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



# Handle the index (home) page
@app.route('/')
def index():
    return render_template('index.html')


# Handle any files that begin "/course" by loading from the course directory
@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'course', path))

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        # re_enter_password = request.form['re_enter_password']
        # if typed_password != re_enter_password:
        #     message = "Password does not match."
        if username and typed_password:
            encryptedpassword = pbkdf2_sha256.encrypt(typed_password, rounds=200000, salt_size=16)
            get_db().create_user(username, encryptedpassword)
            return redirect('/')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encryptedpassword']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('index.html', message=message)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# Handle any unhandled filename by loading its template
@app.route('/<name>')
def generic(name):
    if 'user' in session:
        return render_template(name + '.html')
    else:
        return render_template(name + '.html')

# Any additional handlers that go beyond simply loading a template
# (e.g., a handler that needs to pass data to a template) can be added here


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
