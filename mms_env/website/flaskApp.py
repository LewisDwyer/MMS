from flask import Flask, render_template, request, redirect, url_for, session
from website.databaseManager import *
from website.utils import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

conn = getMySqlConnection(app)

@app.route('/', methods=['GET', 'POST'])
def hello():
    trucklist = getAllTrucks(conn)
    if request.method == 'GET':
        session['registration'] = None
        registration = request.args.get('registration')
        if request.args.get('submit_button') == 'View Route Information':
            return redirect(url_for("map", registration=registration))
        elif request.args.get('submit_button') == 'Add GPS Data':
            return redirect(url_for("addGpsData", registration=registration)) 
        else:
            return render_template("mainpage.html", trucklist=trucklist) 
    return render_template("mainpage.html", trucklist=trucklist)    


@app.route('/map',  methods=['GET', 'POST'])
def map():
    if(session.get('registration') is None):
        session['registration'] = request.args.get('registration')
    truckid = session.get('registration')
    if request.method == 'POST':
        date = request.form.get('date')
        dbpoints = getAllPoints(conn, truckid, date)
        points = dbPointsToTupList(dbpoints)
        gpspoints = []
        for point in points:
            gpspoints.append(gpsToPxl(point[0], point[1]))
        print(gpspoints)
        
        speed = "Truck had an average speed of {}km/h".format(calculateSpeedDuringRoute(dbpoints))
        print(speed)



        return render_template("map.html", truckid=truckid, mine="South Deep Mine",date=date,gpspoints=gpspoints, speed=speed)
    return render_template("map.html", truckid=truckid, mine="South Deep Mine")


@app.route('/addGpsData', methods=['GET', 'POST'])
def addGpsData():
    if(session.get('registration') is None):
        session['registration'] = request.args.get('registration')
    truckid = session.get('registration')

    if request.method == 'POST':
        gpsDataList = getGpsDataListFromPost(request.form.get('gpsData'))
        try:
            gpsObjectList = processGpsData(gpsDataList, truckid)
        except Exception as e:
            print(e)
            return render_template("addGpsData.html", truckid=truckid, formatting="Please check data format")
        for gpsObj in gpsObjectList:
            addGpsDataDB(conn, gpsObj.truckid, gpsObj.gpsdata, gpsObj.capturedatetime)

    return render_template("addGpsData.html", truckid=truckid)