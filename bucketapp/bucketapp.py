from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from bucketapp.models.user.user import User
from bucketapp.models.bucketlist.bucketlist import Bucketlist
from bucketapp.models.activity.activity import Activity

app = Flask(__name__)
app.secret_key = 'supersecret'


app.users = {}
app.registered_emails = []
app.bucketlist = {}


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap


def get_id_for_email(email):
    for user in app.users:
        if app.users[user].email == email:
            return app.users[user].id


def add_bucket_list(name, user_id):
    new_bucketlist = Bucketlist(name, user_id)
    if user_id not in app.bucketlist:
        app.bucketlist[user_id] = {new_bucketlist.id: new_bucketlist}
    else:
        app.bucketlist[user_id][new_bucketlist.id] = new_bucketlist
    return True


def rm_bucket_list(bucket_id, user_id):
    del app.bucketlist[user_id][bucket_id]
    return True


def edit_bucket_list(name, user_id, bucket_id):
    app.bucketlist[user_id][bucket_id].name = name
    return True


def _add_activity(name, description, date, status, user_id, bucket_id):
    new_activity = Activity(name, bucket_id, description, date, status)
    if name not in app.bucketlist[user_id][bucket_id].activities:
        app.bucketlist[user_id][bucket_id].activities[new_activity.id] = new_activity


def _edit_activity(name, description, date, user_id, bucket_id, activity_id):
    activity = app.bucketlist[user_id][bucket_id].activities[activity_id]
    activity.name = name
    activity.description = description
    activity.date = date

@app.route('/')
def home():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if email not in app.registered_emails:
            error = 'You do not have an account, please register.'
        else:
            user_id = get_id_for_email(email)
            if app.users[user_id].password != password:
                error = 'Invalid password, please try again.'
            else:
                session['logged_in'] = True
                session['email'] = email
                session['id'] = user_id
                flash('You are logged in')
                return redirect(url_for('bucketlist'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['inputName'].lower()
        email = request.form['inputEmail'].lower()
        password = request.form['inputPassword'].lower()
        passwordAgain = request.form['inputPasswordAgain'].lower()

        if email not in app.registered_emails:
            if password == passwordAgain:
                new_user = User(name, email, password)
                app.users[new_user.id] = new_user
                app.registered_emails.append(email)
                session['logged_in'] = True
                session['email'] = email
                session['id'] = new_user.id
                flash('You are registered and logged in')
                return redirect(url_for('bucketlist'))
            else:
                error = 'The password you entered do not match.'
        else:
            error = 'Your email has been used.'

    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('id', None)
    flash('you are logged out.')
    return redirect(url_for('home'))


@app.route('/bucketlist')
@login_required
def bucketlist():
    bucketlists = None if session['id'] not in app.bucketlist else app.bucketlist[session['id']]
    return render_template('bucketlist.html', bucketlists=bucketlists)


@app.route('/add_bucketlist', methods=['GET', 'POST'])
@login_required
def add_bucketlist():
    if request.method == 'POST':
        bucketlist = request.form['bucketlist']
        user_id = session['id']
        add_bucket_list(bucketlist, user_id)
        flash(bucketlist + ' has been added successful.')
        return redirect(url_for('bucketlist'))
    return render_template('add_bucketlist.html')


@app.route('/rm_bucketlist/<bucket_id>')
@login_required
def rm_bucketlist(bucket_id):
    bucketlist = app.bucketlist[session['id']][bucket_id].name
    user_id = session['id']
    rm_bucket_list(bucket_id, user_id)
    flash(bucketlist + ' has been removed.')
    return redirect(url_for('bucketlist'))


@app.route('/edit_bucketlist/<bucket_id>', methods=['GET', 'POST'])
@login_required
def edit_bucketlist(bucket_id):
    bucket_name = app.bucketlist[session['id']][bucket_id].name
    if request.method == 'POST':
        new_name = request.form['bucketlist']
        edit_bucket_list(new_name, session['id'], bucket_id)
        flash('You have successfully changed ' + bucket_name + ' to ' + new_name)
        return redirect(url_for('bucketlist'))
    return render_template('edit_buckitlist.html', bucket_id=bucket_id, bucket_name=bucket_name)


@app.route('/add_activity/<bucket_id>', methods=['GET', 'POST'])
@login_required
def add_activity(bucket_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        status = False
        _add_activity(title, description, date, status, session['id'], bucket_id)
        flash(title + ' has been added.')
        return redirect(url_for('bucketlist'))
    return render_template('add_activity.html', bucket_id=bucket_id)


@app.route('/show_activity/<bucket_id>/<activity_id>')
@login_required
def show_activity(bucket_id, activity_id):
    activity = app.bucketlist[session['id']][bucket_id].activities[activity_id]
    return render_template('show_activity.html', activity=activity, bucket_id=bucket_id)


@app.route('/edit_activity/<bucket_id>/<activity_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(bucket_id, activity_id):
    activity = app.bucketlist[session['id']][bucket_id].activities[activity_id]
    old_name = activity.name
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        date = request.form['date']
        user_id = session['id']

        _edit_activity(name, description, date, user_id, bucket_id, activity_id)

        flash('Activity has been edited from ' + old_name + ' to ' + name)
        return redirect(url_for('bucketlist'))
    return render_template('edit_activity.html', activity=activity, bucket_id=bucket_id)


@app.route('/rm_activity/<bucket_id>/<activity_id>')
@login_required
def rm_activity(bucket_id, activity_id):
    activity = app.bucketlist[session['id']][bucket_id].activities[activity_id].name
    del app.bucketlist[session['id']][bucket_id].activities[activity_id]
    flash(activity + ' has been removed.')
    return redirect(url_for('bucketlist'))

if __name__ == '__main__':
    app.run(debug=True)
