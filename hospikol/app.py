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





if __name__ == '__main__':
    app.run(debug=True)