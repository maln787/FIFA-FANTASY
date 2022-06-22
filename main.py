from crypt import methods
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbutils import Query, DB_CONN
from contextlib import closing
import messages as m
import re
import os
import pymysql

load_dotenv()

app = Flask(__name__, template_folder='./templates')

app.config['SECRET_KEY'] = 'SECRET_KEY'

#Staring Window
@app.route('/')
def start():
    return render_template('start.html')

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(Query.USER_LOGIN, (username, password))
                account = cur.fetchone()
                print(account)
                if account:
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    session['firstname'] = account[3]
                    return redirect(url_for('home'))
                else:
                    msg = m.USER_INCORRECT_CREDS

    return render_template('index.html', msg=msg)

#logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(Query.USER_CHECK_ACC, (username,))
                account = cur.fetchone()

                if account:
                    msg = m.USER_ACC_EXISTS
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = m.USER_INVALID_EMAIL
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = m.USER_INVALID_FORMAT
                elif not username or not password or not email:
                    msg = m.USER_FORM_INCOMPLETE
                else:
                    cur.execute(Query.USER_REGISTER, ( username, password, firstname, lastname, email))
                    conn.commit()
                    msg = m.USER_REGISTER_SUCCESS

    elif request.method == 'POST':
        msg = m.USER_FORM_INCOMPLETE

    return render_template('register.html', msg=msg)

#Home Page
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], firstname = session['firstname'])
    return redirect(url_for('login'))


# Team Creation
@app.route('/createTeam', methods=['GET', 'POST'])
def createTeam():
    if 'loggedin' in session:
        msg = ''
        flag = False
        list_ = list()
        if request.method == 'POST' and 'search' in request.form and 'version' in request.form:
            player_dic = dict()
            search = request.form['search']
            version = request.form['version']
            with closing(pymysql.connect(**DB_CONN)) as conn:
                with closing(conn.cursor()) as cur:
                    cur.execute(Query.PLAYER_SEARCH, (search, version))
                    player_info = cur.fetchone()
                    flag = True
                    if player_info:
                        player_dic['Name'] = player_info[0]
                        player_dic['Overall'] = player_info[1]
                        player_dic['Value'] = player_info[2]
                        player_dic['Wage'] = player_info[3]
                        player_dic['Age'] = player_info[4]
                        player_dic['Height'] = player_info[5]
                        player_dic['Weight'] = player_info[6]
                        player_dic['Nation'] = player_info[8] 
                        player_dic['Pace'] = player_info[9]
                        player_dic['Shoot'] = player_info[10]
                        player_dic['Pass'] = player_info[11]
                        player_dic['Drib'] = player_info[12]
                        player_dic['Def'] = player_info[13]
                        player_dic['player_id'] = player_info[14]
                        
                        cur.execute(Query.POSITION, (player_dic['player_id']))
                        position_fetch = cur.fetchall()

                        cur.execute(Query.CLUB, (player_dic['player_id']))
                        club_fetch = cur.fetchall()

                        cur.execute(Query.FETCHSQNAME, (session['id'],))
                        squad_name = cur.fetchone()
                        if position_fetch and club_fetch:
                            for i in position_fetch:
                                for j in i:
                                    list_.append(j)
                            
                            player_dic['clubname'] = club_fetch[0][2]
                            player_dic['leaguename'] = club_fetch[0][3]
                            return render_template('createTeam.html', squad_name = squad_name[1] , player_position = list_, player_ = player_dic, username=session['username'], firstname = session['firstname'], flag = flag)
                    else:
                        flag = False
                        msg = m.USER_PLAYER_INCORRECT

        if request.method == 'POST' and 'add_player' in request.form:
            play = request.form['add_player']
            # print(play, session['id'])

            with closing(pymysql.connect(**DB_CONN)) as conn:
                with closing(conn.cursor()) as cur:
                    cur.execute(Query.INSERTPLAYER, (session['id'], play))
                    conn.commit()
                    msg = 'Successfully Added the Player'

            return render_template('createTeam.html', msg = msg, username=session['username'], firstname = session['firstname'])
        return render_template("createTeam.html", username=session['username'], firstname = session['firstname'], msg = msg, flag = flag)
    return redirect(url_for('login'))

# Show Team
@app.route('/myteam', methods=['GET', 'POST'])
def myteam():
    heading = []
    if 'loggedin' in session:
        msg = ''
        list_player = list()
        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(Query.FETCHTEAM, (session['id']))
                fetch_team = cur.fetchall()

                cur.execute(Query.FETCHSQNAME, (session['id'],))
                squad_name = cur.fetchone()
                final = list()

                for i in fetch_team:
                    list_player.append(i[0])

                for j in list_player:
                    cur.execute(Query.TEAMSHOW , (j,))
                    final.append(cur.fetchall())

                final_list = []
                for j in final:
                    temp = []
                    for k in j:
                        for g in k:
                            temp.append(str(g))
                        final_list.append(list(temp))

        return render_template("myteam.html", squad_name = squad_name[1], headings = ("Id","Player","Club","League","Nationality", "Overall rating","Version", "Check"), data = final_list, username=session['username'], firstname = session['firstname'])
    return redirect(url_for('login'))

#Sekect Squad Name
@app.route('/squad', methods = ['GET', 'POST'])
def squad():
    if 'loggedin' in session and request.method == 'POST':
        squad_name_user = request.form['squad']
        msg = ''
        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(Query.FETCHSQNAME, (session['id'],))
                squad_name = cur.fetchone()
                if squad_name:
                    msg = m.SQUAD_NAME_DUP
                    print(msg)
                    return redirect(url_for('createTeam', squad_name = squad_name[1], msg = msg))
                else:
                    cur.execute(Query.SQUADNAME, ( session['id'], squad_name_user))
                    conn.commit()
    return redirect(url_for('createTeam'))

# Update Squad Name
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if 'loggedin' in session and request.method == 'POST':
        update_sq = request.form['squad']
        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(Query.UPDATESQUAD, (update_sq,session['id']))
                conn.commit()
    return redirect(url_for('myteam'))

#delete player
@app.route('/delete', methods=['GET', 'POST'])
def delete():   
    if 'loggedin' in session and request.method == 'POST':
        with closing(pymysql.connect(**DB_CONN)) as conn:
            with closing(conn.cursor()) as cur:
                for getid in request.form.getlist('mycheckbox'):
                    cur.execute('DELETE FROM `user_team` WHERE player_id = {0}'.format(getid))
                    conn.commit()
        flash('Successfully Deleted!')
    return redirect(url_for('myteam'))




if __name__ == '__main__':
    app.run(debug=True)
    app.run(port=int(os.getenv('APP_PORT')))
