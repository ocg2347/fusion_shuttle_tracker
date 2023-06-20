import time
from fusionchecker import fusionchecker
from sendmail import send_noti_email
import json

PERIOD = 150 # seconds

while True:
    try:
        available_tickets = fusionchecker()
        if available_tickets:
            send_noti_email(f"THERE MIGHT BE AVAILABLE TICKETS: \n \
                            {json.dumps(available_tickets, indent=4)} \n \
                            https://bassliner.org/de/fahrten/fusion-festival-2023-3")
        time.sleep(PERIOD)
    except Exception as e:
        print("error!")
        time.sleep(1)
        continue