from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, Markup
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User,Test
import sqlite3

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/charts")
@login_required
def chart():
    votes = Test.query.filter_by(username=current_user.username, activity='voted').count()
    questions = Test.query.filter_by(username=current_user.username, activity='asks question').count()
    sharing = Test.query.filter_by(username=current_user.username, activity='sharing answer').count()
    searching = Test.query.filter_by(username=current_user.username, activity='checking similar questions').count()
    edits = Test.query.filter_by(username=current_user.username, activity='checking edits').count()
    total = votes+questions+searching+edits+sharing

    labels = ["vote", "asking questions", "sharing answers", "searching questions", "checking edits"]
    values = [votes, questions, sharing, searching, edits]
    colors = [ "#F7464A", "#46BFBD", "#FDB45C","#FEDCBA","#ABCDEF"]

    votesn = Test.query.filter(Test.username!=current_user.username, Test.activity=='voted').count()
    questionsn = Test.query.filter(Test.username!=current_user.username, Test.activity=='asks question').count()
    sharingn = Test.query.filter(Test.username!=current_user.username, Test.activity=='sharing answer').count()
    searchingn = Test.query.filter(Test.username != current_user.username, Test.activity == 'checking similar questions').count()
    editsn = Test.query.filter(Test.username != current_user.username, Test.activity == 'checking edits').count()

    valuesn = [votesn, questionsn, sharingn,searchingn,editsn]
    totaln = votesn + questionsn + searchingn + editsn + sharingn

    all_users = []
    all_votequestion_values = []
    all_votes = []
    all_searches = []
    query = db.session.query(Test.username).distinct()
    for val in query:
        all_users.append(val[0])
        query2 = Test.query.filter_by(username=val[0], activity='voted').count()
        query3 = Test.query.filter_by(username=val[0], activity='asks question').count()
        all_votequestion_values.append(query2 + query3)

        query2 = Test.query.filter_by(username=val[0], activity='voted').count()
        all_votes.append(query2)

        query2 = Test.query.filter_by(username=val[0], activity='checking similar questions').count()
        all_searches.append(query2)

    labelsbar = ["January", "February", "March", "April", "May", "June", "July", "August"]
    valuesbar = [10, 9, 8, 7, 6, 4, 7, 8]

    temp_max = max(votes, questions, sharing,edits,searching)

    variation = max(abs(float(votes) / float(total) - float(votesn) / float(totaln)),
                    abs(float(questions) / float(total) - float(questionsn) / float(totaln)),
                    abs(float(sharing) / float(total) - float(sharingn) / float(totaln)),
                    abs(float(searching) / float(total) - float(searchingn) / float(totaln)))

    if float(temp_max) > 0.65 * float(total):
        return render_template('activity_chart.html', set1=zip(all_searches, all_users, colors),
                           set2=zip(all_votequestion_values, all_users, colors), set3=zip(all_votes, all_users, colors),
                           variate=variation, equal='votes,question and share similarly', spammer='be a spammer',
                           labelsbar=labelsbar, valuesbar=valuesbar, set=zip(values, labels, colors),
                           setn=zip(valuesn, labels, colors), title="Overall User Activity",
                           title2="Overall Other Users")
    else:
        return render_template('activity_chart.html', set1=zip(all_searches, all_users, colors),
                               set2=zip(all_votequestion_values, all_users, colors),
                               set3=zip(all_votes, all_users, colors),
                               variate=variation, equal='votes,question and share similarly', spammer='not be a spammer',
                               labelsbar=labelsbar, valuesbar=valuesbar, set=zip(values, labels, colors),
                               setn=zip(valuesn, labels, colors), title="Overall User Activity",
                               title2="Overall Other Users")

    variation = max(abs(float(votes)/float(total)-float(votesn)/float(totaln)),abs(float(questions)/float(total)-float(questionsn)/float(totaln)),abs(float(sharing)/float(total)-float(sharingn)/float(totaln)))
    print abs(float(votes/total)-float(votesn/totaln)),abs(float(questions/total)-float(questionsn/totaln)),abs(float(sharing/total)-float(sharingn/totaln))
    print "variation is ",variation
    temp_max = max(votes, questions, sharing)
    if votes==questions==sharing:
        return render_template('activity_chart.html',set1=zip(all_searches, all_users, colors), set2=zip(all_vote_values, all_users, colors), set3=zip(all_sp_values, all_users, colors),variate=variation,equal='votes,question and share similarly',spammer='not be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),title="Overall User Activity", title2="Overall Other Users")
    elif votes==temp_max:
        if float(votes/total)>=0.65:
            return render_template('activity_chart.html', variate=variation, equal='vote more',
                               spammer='be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                               set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                               title="Overall User Activity", title2="Overall Other Users")
        else:
            return render_template('activity_chart.html', variate=variation, equal='vote more',
                                   spammer='not be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                                   set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                                   title="Overall User Activity", title2="Overall Other Users")
    elif questions==temp_max:
        if float(votes/total)>=0.65:
            return render_template('activity_chart.html', variate=variation, equal='question more',
                               spammer='be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                               set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                               title="Overall User Activity", title2="Overall Other Users")
        else:
            return render_template('activity_chart.html', variate=variation, equal='question more',
                                   spammer='not be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                                   set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                                   title="Overall User Activity", title2="Overall Other Users")
    else:
        if float(votes/total)>=0.65:
            return render_template('activity_chart.html', variate=variation, equal='share more',
                               spammer='be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                               set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                               title="Overall User Activity", title2="Overall Other Users")
        else:
            return render_template('activity_chart.html', variate=variation, equal='share more',
                                   spammer='not be a spammer', labelsbar=labelsbar, valuesbar=valuesbar,
                                   set=zip(values, labels, colors), setn=zip(valuesn, labels, colors),
                                   title="Overall User Activity", title2="Overall Other Users")

    return render_template('activity_chart.html',labelsbar=labelsbar,valuesbar=valuesbar, set=zip(values, labels, colors), setn=zip(valuesn, labels, colors), title="Overall User Activity",title2="Overall Other Users")
'''

@app.route('/charts', methods=['GET','POST'])
@login_required
def chart():
    print "ghi"
    votes = Test.query.filter_by(username=current_user.username, activity='voted').count()
    questions = Test.query.filter_by(username=current_user.username, activity='asks question').count()
    sharing = Test.query.filter_by(username=current_user.username, activity='sharing answer').count()
    print votes,questions,sharing
    labels = ["votes", "questions", "sharing"]
    values = [votes,questions,sharing]
    colors = ["#F7464A", "#46BFBD", "#FDB45C"]
    return render_template('chart.html', set=zip(values, labels, colors),title="Overall User Activity")
'''

@app.route('/profile', methods=['GET','POST'])
def fetching():
    if request.method == "POST":
        data = request.form
        temp = dict(data)
        dict_data = {}
        for ele in temp:
            dict_data[ele] = temp[ele][0]
        dict_data['count'] = int(dict_data['count'])
        query = Test(username=dict_data['usern'], count=dict_data['count'], activity=dict_data['activity'])
        db.session.add(query)
        db.session.commit()
        print "inserted into db"
        return render_template('index.html', title='Home')
'''
    print "starting conn"
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    print str(current_user.username)
    c.execute("SELECT time, activity FROM Test WHERE username like '" + str(current_user.username) + "' ORDER BY id DESC LIMIT 20")
    data = c.fetchall()

    print "rendering"
    return render_template('analytics.html', title='Home', data=data)
'''

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():


    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    print current_user
    user = User.query.filter_by(username=username).first_or_404()
    posts = Test.query.filter_by(username=username).first()
    #print username,posts
    #table = Test(posts)
    #table.border = True
    #print "table"
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    print str(current_user.username)
    c.execute("SELECT time, activity FROM Test WHERE username like '" + str(current_user.username) + "' ORDER BY id DESC LIMIT 20")
    data = c.fetchall()

    print "rendering"

    return render_template('user.html', user=user, data=data)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    print "yeh"
    print form
    if form.validate_on_submit():
        print "idhar"
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
