
import requests
import time
import schedule
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

# Now try accessing the variables

my_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
recipient = os.getenv("RECIPIENT")


MY_LAT = 59.522947
MY_LONG = 15.989472

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour_now = time_now.strftime("%H")


def is_dark():
    if hour_now in range(sunrise, sunset):
        return False
    else:
        return True



def is_nearby(iss_longitude, iss_latitude, my_long, my_lat, margin = 5):
    if abs(iss_longitude - my_long) <= margin and abs(iss_latitude - my_lat) <= margin:
        return True
    else:
        return False
    

minute_now = time_now.strftime("%M")

    
def send_iss_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs=recipient, 
                msg=f"Subject: ISS Visible from your location.\n\nISS Visible from your location")
            

def iss_nearby():
    if is_dark() and is_nearby(iss_longitude, iss_latitude, MY_LONG, MY_LAT):
        send_iss_email()
        return True
    else:
        print("Not yet visible from your location")
        return False



schedule.every(1).minute.do(iss_nearby)

while True:
    schedule.run_pending()
    time.sleep(1)