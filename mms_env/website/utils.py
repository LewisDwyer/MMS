from math import radians, cos, sin, asin, sqrt

# Some ORM yay
class gpsData:
  def __init__(self, gpsdata, truckid, capturedatetime):
    self.truckid = truckid
    self.gpsdata = gpsdata
    self.capturedatetime = capturedatetime


def gpsToPxl(lat, long):

    delta_x = 1182 # pixel x val of map
    delta_y = 787  # pixel y val of map
    map_lat = -26.430071
    map_log = 27.650212

    delta_lat = -26.396586 - map_lat # latitude
    delta_long = 27.706551 - map_log # longitude
    #TODO make the map values generic so that the map can be easily updated

    hor_scale = delta_x/delta_long # x axis ratio
    vertical_scale = delta_y/delta_lat # y axis ratio


    y = delta_y - ((lat - map_lat) * vertical_scale)
    x = (long - map_log) * hor_scale

    return [x, y]


def dbPointsToTupList(points):
    result = []
    for point in points:
        split = point[1].split(",")
        result.append((float(split[0].strip()), float(split[1].strip())))
    return result


def getGpsDataListFromPost(gpsData):
    gpsdatalist = [str.strip() for str in gpsData.splitlines()]
    return gpsdatalist

def createValidGpsDataValues(gpsDataLong, gpsDataLat, datetime, truckid):
    try:
        float(gpsDataLong)
        float(gpsDataLat)
        #TODO validate Date format
    except:
        raise Exception("Data format incorrect")

    logLatVal = gpsDataLong + ", " + gpsDataLat

    return gpsData(logLatVal, truckid, datetime)
    
        

def processGpsData(gpsDataList, truckid):
    gps = []
    for gpsDataItem in gpsDataList:
        gpsDataElem = gpsDataItem.split(',')
        if len(gpsDataElem) == 3:
            longVal = gpsDataElem[0].strip()
            latVal = gpsDataElem[1].strip()
            dateTime = gpsDataElem[2].strip()
            try:
                gpsDat = createValidGpsDataValues(longVal, latVal, dateTime, truckid)
                gps.append(gpsDat)
            except:
                # Best effort
                continue
        else: 
            continue
    return gps #now a list of gps objects semi validated

# haversine formula (stolen)
def calcTwoPointDistanceKm(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 

    print(lon2)
    print(lon1)

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r


def calculateTotalDistance(points):
    distance = 0
    for x in range(1, len(points)):
        currlat = points[x-1][0]
        currlong = points[x-1][1]
        nextlat = points[x][0]
        nextlong = points[x][1]
        distance = distance + calcTwoPointDistanceKm(currlat, currlong, nextlat, nextlong)
    print(distance)
    return distance

def calculateTotalTime(points):
    result = points[-1] - points[0]
    return result


def calculateSpeedDuringRoute(points):
    pointstup = dbPointsToTupList(points)
    totalDis = calculateTotalDistance(pointstup)
    times = []
    for point in points:
        times.append(point[2]) #timestamp in seconds
    TotalTime =  calculateTotalTime(times)
    time = TotalTime/3600
    result = totalDis/time
    return str(round(result, 2))
