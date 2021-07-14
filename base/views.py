from django.shortcuts import render
import pyrebase

config = {
    'apiKey': "AIzaSyDyR0VY3oPezm2v5_5tDK1Sdwkirmac6CI",
    'authDomain': "djangofirebase-c9c2d.firebaseapp.com",
    'projectId': "djangofirebase-c9c2d",
    'databaseURL': "https://djangofirebase-c9c2d-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "djangofirebase-c9c2d.appspot.com",
    'messagingSenderId': "932252377053",
    'appId': "1:932252377053:web:0a6cdb65d22966d888a034",
    'measurementId': "G-Z8QMQ8ET20",
}
# Initialize Firebase
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def indexView(request):
    return render(request, 'base/index.html')

def authView(request):
    return render(request, 'base/login.html')

def profileView(request):
    email = request.POST.get('email')
    pw = request.POST.get('pass')

    user = auth.sign_in_with_email_and_password(email, pw)

    # db = firebase.database()

    # data = {}

    # results = db.child("users").push(data, user['idToken'])

    return render(request, 'base/profile.html', {'email': email})
