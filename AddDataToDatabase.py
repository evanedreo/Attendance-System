import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendance-d5748-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    "03010":
        {
            "name":"Evan Edreo",
            "major":"Computer Science",
            "starting_year":2022,
            "total_attendance":6,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2024-01-09 20:56:11"
        },
    "11273":
        {
            "name": "Patrick Deng",
            "major": "Computer Science",
            "starting_year": 2021,
            "total_attendance": 6,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-01-09 20:56:11"
        },
    "12912":
        {
            "name": "Iman Gadzhi",
            "major": "Business",
            "starting_year": 2020,
            "total_attendance": 10,
            "standing": "B",
            "year": 4,
            "last_attendance_time": "2024-01-09 20:56:11"
        }

}

for key, value in data.items():
    ref.child(key).set(value)