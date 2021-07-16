from django.shortcuts import render, redirect
from decouple import config
from django.contrib.auth import logout
import pyrebase, time, pytz
from datetime import timezone, datetime

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

def createReportView(request):
    return render(request, 'base/create.html')

def postCreateReportView(request):
    work = request.POST.get('work-assign')
    progress = request.POST.get('progress')
    url = request.POST.get('url')

    tz = pytz.timezone('Asia/Dhaka')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    time_mil = int(time.mktime(time_now.timetuple()))

    id_token = request.session['uid']
    user_info = authfb.get_account_info(id_token)
    local_id = user_info['users'][0]['localId']

    data = {
        'work': work,
        'progress': progress,
        'url': url
    }

    db.child('users').child(local_id).child('reports').child(time_mil).set(data)
    name = db.child('users').child(local_id).child('details').child('name').get().val()
    return render(request, 'base/profile.html', {'email': name})

def checkReportView(request):
    id_token = request.session['uid']
    user_info = authfb.get_account_info(id_token)
    local_id = user_info['users'][0]['localId']
    name = db.child('users').child(local_id).child('details').child('name').get().val()

    all_timestamps = db.child('users').child(local_id).child('reports').shallow().get().val()
    print(all_timestamps)
    timestamps = []
    if all_timestamps is None:
        return render(request, 'base/check.html', {'message': 'No Reports Available', 'name': name})
    else:
        for i in all_timestamps:
            timestamps.append(i)

    timestamps.sort(reverse=True)

    works = []
    for i in timestamps:
        work = db.child('users').child(local_id).child('reports').child(i).child('work').get().val()
        works.append(work)

    print(works)

    dates = []
    for i in timestamps:
        i = float(i)
        date = datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        dates.append(date)

    print(dates)
    comb_list = zip(timestamps, dates, works)
    return render(request, 'base/check.html', {'comb_list': comb_list, 'name': name})

def postCheckReportView(request, key):
    time = key

    id_token = request.session['uid']
    user_info = authfb.get_account_info(id_token)
    local_id = user_info['users'][0]['localId']
    name = db.child('users').child(local_id).child('details').child('name').get().val()

    work = db.child('users').child(local_id).child('reports').child(time).child('work').get().val()
    progress = db.child('users').child(local_id).child('reports').child(time).child('progress').get().val()
 
    i = float(time)
    date = datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    
    context = {
        'time': time,
        'name': name,
        'work': work,
        'progress': progress,
        'date': date,
    }
    return render(request, 'base/report.html', context)