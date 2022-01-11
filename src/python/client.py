import atomic_store
import requests
from requests.auth import HTTPBasicAuth
import time

def send(): 
    #dt = None
    with atomic_store.open("src/resources/digital_twin.json", default=dict()) as store:
        dt = store.value
        thindId = dt["thingId"]
        response = requests.put("http://137.204.107.148:3128/api/ditto/" + thindId,
                                data=dt,
                                auth=HTTPBasicAuth("ditto", "ditto"))
        if response.status_code == 400:
            print("Error! Request malformed!")
        elif response.status_code == 404:
            print("Error! Thing not found!")
    
if __name__ == '__main__':
    while True:
        send()
        time.sleep(1)