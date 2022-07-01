from flaskext.mysql import MySQL

def getMySqlConnection(app):
    try:
        mysql = MySQL()
    
        app.config['MYSQL_DATABASE_USER'] = 'root'   
        app.config['MYSQL_DATABASE_PASSWORD'] = 'frogfrog'
        app.config['MYSQL_DATABASE_DB'] = 'flasklocationapp'  
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)

        return mysql.connect()
    except:
        print("An error occurred when connecting to the Database")

def getAllTrucks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT idtruck,registration FROM truck')
        trucklist = list(cursor.fetchall())
        cursor.close()
        return trucklist
    except:
        print("An error occurred retrieving trucks from the DB")

def getAllPoints(conn, truckid, date):
    try:
        cursor = conn.cursor()
        sql = "SELECT idlocation,gpsdata,UNIX_TIMESTAMP(capturedatetime) FROM location INNER JOIN truck on location.truckid = truck.idtruck WHERE DATE(capturedatetime) = %(date)s AND registration = %(truckid)s ORDER BY capturedatetime"
        params =  {"date": date, "truckid": truckid}
        print(sql)
        print(params)
        cursor.execute(sql, params)
        points = list(cursor.fetchall())
        cursor.close()
        return points
    except:
        print("An error occurred retrieving gps data from the DB")


def addGpsDataDB(conn, truckreg, gpsdata, capturedatetime):
    try:
        cursor = conn.cursor()

        cursor.execute('SELECT idtruck,registration FROM truck where registration = %(truckreg)s', {"truckreg": truckreg})
        truckid = int(cursor.fetchone()[0])
        
        sql = "INSERT INTO location(gpsdata, capturedatetime, truckid) VALUES(%(gpsdata)s,%(capturedatetime)s, %(truckid)s)"
        params =  {"gpsdata": gpsdata, "capturedatetime":capturedatetime, "truckid": truckid}
        print(sql)
        print(params)
        cursor.execute(sql, params)
        conn.commit()
    except Exception as e:
        print(e)
        print("An error occurred Inserting gps data into the DB")


#NOTES: Some ORM would have been nice to add rather than this dirty sql