from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyCn4fUDcfhDke5Uwe5ARfWo9ecH2Ss2ZQU",
  "authDomain": "hospikol-e2d8c.firebaseapp.com",
  "databaseURL": "https://hospikol-e2d8c-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "hospikol-e2d8c",
  "storageBucket": "hospikol-e2d8c.appspot.com",
  "messagingSenderId": "911667640468",
  "appId": "1:911667640468:web:04f32bc9b26828bb21dc81",
  "measurementId": "G-14JFFTGXDK"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    if request.form['password']==request.form['confirmPassword']:
      try:
        user = {'name': request.form['name'], 'account_type':1, 'questions': 0}
        login_session['user'] = auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        db.child('Users').child(login_session['user']['localId']).set(user)
        return render_template('index.html')
      except: 
        return render_template('signup.html')
    else:
      return render_template('signup.html')
  else:
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
      return render_template('index.html')
    except:
      return render_template('login.html')
  else:
    return render_template('login.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
  if request.method=='POST':
    # try:
    try:
      number = db.child('q_num').get().val()['number_q']
      number+=1
    except:
      number = 0
    try:
      db.child('q_num').update({'number_q': number})    
    except:
      db.child('q_num').set(num)

      # num = db.child('Users').child(login_session['user']['localId']).get().val()
      # num = num['questions']
    question = {'question':request.form['question'], 'answers':{}, 'user':login_session['user']['localId'], 'description': request.form['description']}
    db.child('Questions').child(login_session['user']['localId']).child(number).set(question)
    return redirect(url_for('show_questions'))
    # except:
    #   return redirect('/show_questions')
  else:
    return redirect('/show_questions')

@app.route('/show_questions')
def show_questions():
  # try:
    num=0
    users = db.child('Users').get().val().keys()
    print(users)
        # questions |= que_dict[user][question]
    for uid in users:
      questions = db.child('Questions').child(uid).get().val()
      print(questions)

    return render_template('about.html', questions=questions)
    # , questions=questions
  # except:
  #   return render_template('index.html')

@app.route('/add_answer/<string:key>/<string:user>', methods=['GET', 'POST'])
def add_answer(key, user):
  if request.method=='POST':
    # try:
      answer={'user': login_session['user']['localId'], 'text': request.form['answer']}
      db.child('Questions').child(user).child(key).child('answers').push(answer)
      return redirect('/show_questions')
    # except:
    #   return redirect('/show_questions')
  else:
    return redirect('/show_questions')

@app.route('/logout')
def logout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('home'))
@app.route('/doctors')
def doctors():
  return render_template('doctors.html')


@app.route('/question/<string:key>')
def show_question(key):
  question = db.child('Questions').child(key).get().val()
  return render_template('question.html', question=question)
if __name__ == '__main__':
    app.run(debug=True)