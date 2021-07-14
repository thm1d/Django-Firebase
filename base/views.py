from django.shortcuts import render, redirect
from decouple import config
from django.contrib.auth import logout
import pyrebase

firebase_config = {
    'apiKey': config('API_KEY'),
    'authDomain': config('PROJECT_ID')+".firebaseapp.com",
    'projectId': config('PROJECT_ID'),
    'databaseURL': "https://"+config('PROJECT_ID')+"-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': config('PROJECT_ID')+".appspot.com",
    'messagingSenderId': config('MESSEGING_SENDER_ID'),
    'appId': config('APP_ID'),
    'measurementId': config('MEASUREMENT_ID'),
}
# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

def indexView(request):
    return render(request, 'base/index.html')

def authView(request):
    return render(request, 'base/login.html')

def profileView(request):
    email = request.POST.get('email')
    pw = request.POST.get('pass')

    try:
        user = auth.sign_in_with_email_and_password(email, pw)
    except:
        message = "Invalid Credentials"
        return render(request, 'base/login.html', {'message': message})

    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, 'base/profile.html', {'email': email})

def logOutView(request):
    logout(request)
    return render(request, 'base/login.html')
