from flask import render_template, url_for, request, flash, session, redirect, jsonify
from ltwallet import app, mysql

from ltwallet.forms import RegisterForm

quotes = ["news","GBP-USD", "GBP-EUR","GBP-CAD","GBP-AUD","GBP-CHF","BTC-GBP", "EUR-USD","EUR-JPY","EUR-CHF","EUR-AUD", "BTC-EUR","USD-CAD","USD-CHF", "USD-AUD","USD-JPY", "BTC-USD", ".INX:INDEXSP", ".DJI:INDEXDJX"]
database = []
for quote in quotes:
            if "-" in quote:
                quote = quote.replace("-", "")
            elif "." in quote:
                quote = quote.strip(".").replace(":", "")
            else:
                quote = quote
            database.append(quote)
@app.route('/')
def home():
    db = "news"
    latest = False
    try:
        db = request.args['db']
        latest = request.args['latest']
    except :
        pass
    cursor = mysql.connection.cursor()
    smt = f"SELECT * FROM {db}"
    cursor.execute(smt)
    data = cursor.fetchall()
    return render_template("/home.html", data=data, database = database, db = db, latest = latest)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    # Fetch one record and return result
    account = cursor.fetchone()
    if account:
        # Create session data, we can access this data in other routes
        if account[2] == password:
            session['loggedin'] = True
            session['id'] = password
            session['username'] = username
            # Redirect to home page
            flash("Login Successful")
            return redirect(url_for("home"))
        else:
            message = "Incorect Password!!!"
            flash(message)
        return render_template("/signin.html", error = message)
    else:
        message = "Incorect Username and Password"
        return render_template("/signin.html", error = message)
    

@app.route('/signin')
def signin():
    curs = mysql.connection.cursor()
    curs.execute('''SELECT * FROM users ''')
    data = curs.fetchall()
    return render_template('signin.html', data=data)
 
@app.route('/signup')
def signup():
    return render_template("/signup.html")

@app.route('/signout')
def signout():
    session['loggedin'] = ""
    session['id'] = ""
    session['username'] = ""
    return redirect(url_for("home"))

@app.route('/current_data')
def background_process():
    
    try:
        cursor = mysql.connection.cursor()
        quote = request.args.get('market', 0, type=str)
        if quote == "news":
            error = "None"
        else:
            error = ""
        smt = f"SELECT * FROM current WHERE quote = '{quote}'"
        cursor.execute(smt)
        data = cursor.fetchall()
        if data:
            market = quote 
            time_data = []
            values_data = []
            for i in data:
                time_data.append(i[3])
                values_data.append(i[2].replace(",",""))
            return jsonify(time_data=time_data, values_data=values_data, market=market, error=error)
        else:
            return jsonify(error="None")
    except Exception as e:
        return str(e)

@app.route("/barchart")
def barchart():
    try:
        cursor = mysql.connection.cursor()
        smt = f"SELECT * FROM newcurrent WHERE quote = 'EURUSD'"
        cursor.execute(smt)
        data = cursor.fetchall()
        if data:
            market = "EURUSD" 
            time_data = []
            bids = []
            asks= []
            highs = []
            lows = []
            variables = []
            for i in data[0:5]:
                new = []
                new.append(i[6])
                new.append(i[2])
                new.append(i[3])
                new.append(i[4])
                new.append(i[5])
                variables.append(new)
            return jsonify(market=market, variables=variables)
        else:
            return jsonify(error="None")
    except Exception as e:
        return str(e)

@app.route("/charts")
def charts():
    return render_template("charts.html")