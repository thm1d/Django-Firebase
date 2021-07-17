from django.shortcuts import render
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

authfb = firebase.auth()

db = firebase.database()

def indexView(request):
    return render(request, 'base/index.html')

def registerView(request):
    return render(request, 'base/register.html')

def postRegisterView(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    pw = request.POST.get('pass')

    try:
        user = authfb.create_user_with_email_and_password(email, pw)
    except:
        message = "Please Enter a Valid Name & Email Address"
        return render(request, 'base/register.html', {'message': message})

    uid = user['localId']

    data = {
        'name': name,
        'email': email,
        'status': '1'
    }

    db.child('users').child(uid).child('details').set(data)
    
    return render(request, 'base/login.html')

def authView(request):
    return render(request, 'base/login.html')

def profileView(request):
    email = request.POST.get('email')
    pw = request.POST.get('pass')

    try:
        user = authfb.sign_in_with_email_and_password(email, pw)
    except:
        message = "Invalid Credentials"
        return render(request, 'base/login.html', {'message': message})

    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    local_id = user['localId']
    name = db.child('users').child(local_id).child('details').child('name').get().val()
    return render(request, 'base/profile.html', {'email': name})

def logOutView(request):
    logout(request)
    return render(request, 'base/login.html')
