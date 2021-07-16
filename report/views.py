from django.shortcuts import render
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


def logOutView(request):
    logout(request)
    return render(request, 'base/login.html')

def createReportView(request):
    return render(request, 'report/create.html')

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
        'file-url': url
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
        return render(request, 'report/check.html', {'message': 'No Reports Available', 'name': name})
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
    return render(request, 'report/check.html', {'comb_list': comb_list, 'name': name})

def postCheckReportView(request, key):
    time = key

    id_token = request.session['uid']
    user_info = authfb.get_account_info(id_token)
    local_id = user_info['users'][0]['localId']
    name = db.child('users').child(local_id).child('details').child('name').get().val()

    work = db.child('users').child(local_id).child('reports').child(time).child('work').get().val()
    progress = db.child('users').child(local_id).child('reports').child(time).child('progress').get().val()
    file_url = db.child('users').child(local_id).child('reports').child(time).child('file-url').get().val()
 
    i = float(time)
    date = datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    
    context = {
        'time': time,
        'name': name,
        'work': work,
        'progress': progress,
        'date': date,
        'url': file_url,
    }
    return render(request, 'report/report.html', context)