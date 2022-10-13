from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'user_crud_mod'

mysql = MySQL(app)

@app.route ('/users')
def users():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    cur.execute(sql)
    result = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("users.html", result=result)

@app.route ('/users/new', methods=["GET", "POST"])
def users_new():
    if request.form:
        cur = mysql.connection.cursor()
        sql = "INSERT INTO users (first_name, last_name, email) VALUES ('" + request.form.get('firstname') + "', '"+ request.form.get('lastname') + "', '"+request.form.get('email') +"')"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('users'))
        
    return render_template("users_new.html")

@app.route('/users/<id>')
def users_show(id):
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM users WHERE id=" + id
    cur.execute(sql)
    result = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return render_template("users_show.html", result=result)

@app.route('/users/<id>/delete')
def users_delete(id):
    cur = mysql.connection.cursor()
    sql = "DELETE FROM users WHERE id=" + id
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users'))

@app.route('/users/<id>/edit', methods=["GET", "POST"])
def users_edit(id):
    if request.form:
        cur = mysql.connection.cursor()
        sql = "UPDATE users SET first_name = '" + request.form.get('firstname') + "', last_name = '" + request.form.get('lastname') + "', email = '" + request.form.get('email') + "' WHERE id=" + id
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()

    cur = mysql.connection.cursor()
    sql = "SELECT *  FROM users WHERE id=" + id
    cur.execute(sql)
    result = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return render_template("users_edit.html", result=result)

app.run(debug=True)