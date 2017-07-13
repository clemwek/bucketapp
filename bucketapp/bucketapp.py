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
            return  app.users[user].id


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
            error = 'Invalid credentials, please try again.'
        else:
            user_id = get_id_for_email(email)
            if app.users[user_id].password != password:
                error = 'Invalid credentials, please try again.'
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

        if password == passwordAgain:
            new_user = User(name, email, password)
            app.users[new_user.id] = new_user
            app.registered_emails.append(email)
            session['logged_in'] = True
            session['email'] = email
            session['id'] = new_user.id
            flash('You are registered and logged in')
            return redirect(url_for('bucketlist'))
        error = 'password do not march'

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
        new_bucketlist = Bucketlist(bucketlist, user_id)
        if user_id not in app.bucketlist:
            app.bucketlist[user_id] = {new_bucketlist.id: new_bucketlist}
        else:
            app.bucketlist[user_id][new_bucketlist.id] = new_bucketlist
        flash(bucketlist + ' has been added successful.')
        return redirect(url_for('bucketlist'))
    return render_template('add_bucketlist.html')


@app.route('/rm_bucketlist/<bucket_id>')
@login_required
def rm_bucketlist(bucket_id):
    del app.bucketlist[session['id']][bucket_id]
    flash('Bucket has been removed.')
    return redirect(url_for('bucketlist'))


@app.route('/edit_bucketlist/<bucket_id>', methods=['GET', 'POST'])
@login_required
def edit_bucketlist(bucket_id):
    bucket_name = app.bucketlist[session['id']][bucket_id].name
    if request.method == 'POST':
        new_name = request.form['bucketlist']
        app.bucketlist[session['id']][bucket_id].name = new_name
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
        new_activity = Activity(title, bucket_id, description, date, status)
        if title not in app.bucketlist[session['id']][bucket_id].activities:
            app.bucketlist[session['id']][bucket_id].activities[new_activity.id] = new_activity
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
    if request.method == 'POST':
        activity.name = request.form['title']
        activity.description = request.form['description']
        activity.date = request.form['date']

        flash('Activity has been edited.')
        return redirect(url_for('bucketlist'))
    return render_template('edit_activity.html', activity=activity, bucket_id=bucket_id)


@app.route('/rm_activity/<bucket_id>/<activity_id>')
@login_required
def rm_activity(bucket_id, activity_id):
    del app.bucketlist[session['id']][bucket_id].activities[activity_id]
    flash('Activity has been removed.')
    return redirect(url_for('bucketlist'))

if __name__ == '__main__':
    app.run(debug=True)
