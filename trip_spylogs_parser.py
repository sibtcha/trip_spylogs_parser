import re
import simplekml
import argparse
import os
import datetime

class Trip:
    def __init__(self) -> None:
        pass

    def __str__(self):
        return f"{self.trip_number}, {self.start_date}, {self.start_mileage}, {self.start_latitude}, {self.start_longitude}, {self.start_altitude}, {self.start_address}, {self.finish_date}, {self.finish_mileage}, {self.finish_latitude}, {self.finish_longitude}, {self.finish_altitude}, {self.finish_address}"


def get_value_from_line(str, line):
    if str in line:
        str_split = line.split(': ')
        if len(str_split) > 1:
            str_return = str_split[1].strip('\n')
            return str_return
        else:
            return ''

def read_trip_log(file):
    #with open(file) as f:
    trips = []
    for line in file:
        if "Trip number : " in line:

            trip_number = re.findall(r'\d+', line)
            trip_number = trip_number[0]
            trip = Trip()
            trip.trip_number = trip_number
            trips.append(trip)


        if "Trip Data" in line:
            if "Start" in line:
                if get_value_from_line('DateTime', line) is not None   : trip.start_date         = get_value_from_line('DateTime', line)   
                if get_value_from_line('Mileage', line) is not None    : trip.start_mileage      = get_value_from_line('Mileage', line)    
                if get_value_from_line('Latitude', line) is not None   : trip.start_latitude     = get_value_from_line('Latitude', line)   
                if get_value_from_line('Longitude', line) is not None  : trip.start_longitude    = get_value_from_line('Longitude', line)  
                if get_value_from_line('Altitude', line) is not None   : trip.start_altitude     = get_value_from_line('Altitude', line)   
                if get_value_from_line('Address', line) is not None    : trip.start_address      = get_value_from_line('Address', line)    

            if "Finish" in line:
                if get_value_from_line('DateTime', line) is not None   : trip.finish_date        = get_value_from_line('DateTime', line) 
                if get_value_from_line('Mileage', line) is not None    : trip.finish_mileage     = get_value_from_line('Mileage', line) 
                if get_value_from_line('Latitude', line) is not None   : trip.finish_latitude    = get_value_from_line('Latitude', line) 
                if get_value_from_line('Longitude', line) is not None  : trip.finish_longitude   = get_value_from_line('Longitude', line) 
                if get_value_from_line('Altitude', line) is not None   : trip.finish_altitude    = get_value_from_line('Altitude', line) 
                if get_value_from_line('Address', line) is not None    : trip.finish_address     = get_value_from_line('Address', line) 

    return trips 

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', dest="file", required=True, help='Input file', metavar="FILE", type=argparse.FileType('r'))
	
    args = parser.parse_args()

    trips = read_trip_log(args.file)

    kml = simplekml.Kml(name=f"{args.file.name}")
    for t in trips:
        day = datetime.datetime.strptime(t.start_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y.%m.%d %H:%M:%S")
        fol = kml.newfolder(name=f"{t.trip_number} - {day}")
        fol.timestamp.when = t.start_date
        pnt_start   = fol.newpoint(name=f"{t.trip_number} - {t.start_date} - Start",   description=f"Start : {t.start_date}",      coords=[(t.start_longitude,t.start_latitude)])
        pnt_finish  = fol.newpoint(name=f"{t.trip_number} - {t.finish_date} - End",    description=f"Finish : {t.finish_date}",    coords=[(t.finish_longitude,t.finish_latitude)])

        pnt_start.style.iconstyle.color = simplekml.Color.lightgreen
        pnt_finish.style.iconstyle.color = simplekml.Color.red
    
    kml.save(f"{args.file.name}.kml")
    
           