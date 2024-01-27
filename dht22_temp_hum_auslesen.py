import board
import adafruit_dht
import pandas as pd


from time import sleep
from datetime import datetime


dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

data_point_intervall_seconds = 3600

temp_list = []
humidity_list = []
time_list = []

while True:
    try:
        while True:
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            temp_list.append(temperature_c)
            humidity_list.append(humidity)
            time_list.append(date_time)

            df = pd.DataFrame(
                list(zip(time_list, temp_list, humidity_list)),
                columns=["Zeit", "Temperatur", "Luftfeuchtigkeit"],
            )

            df.to_csv("temp_hum.csv", index=False)

            print(
                f"Data stored! Next measurement in {int(data_point_intervall_seconds/60)} minutes."
            )
            print("The last 100 entries:\n")
            print(df.tail(100))
            sleep(3600)

    except RuntimeError as error:
        print(error.args[0])
        sleep(2)
        print("trying again...")

    except Exception as error:
        dhtDevice.exit()
        sleep(2)
        print("trying again...")
        raise error
