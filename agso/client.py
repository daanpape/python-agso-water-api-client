import requests
import typing

from .model import AgsoAddress
from .model import AgsoMeter
from .model import AgsoSubscriber
from .model import AgsoValue

class AgsoClient:
    BASE_URL = "https://api.agsoknokke-heist.be/api/v1/"

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.customer_number = -1
        self.subscriber_number = -1
        self.meter_number = -1
        self.token = None

    def authenticate(self) -> bool:
        """Authenticate to the AGSO API and store the token, returns True on success."""
        req = requests.post(
            AgsoClient.BASE_URL + "authenticate",
            json={"email": self.username, "password": self.password},
            timeout=5000,
        )

        if req.status_code != 200:
            return False

        resp = req.json()

        if "token" not in resp:
            return False

        self.token = resp["token"]
        return True

    def __authenticated_get(self, url: str) -> typing.Any:
        """Perform an authenticated GET request, returns the response as an object."""
        resp = None

        if self.token == None:
            if not self.authenticate():
                return None

        for _ in range(2):
            resp = requests.get(
                AgsoClient.BASE_URL + url,
                headers={"Authorization": "Bearer " + self.token},
                timeout=5000,
            )

            if resp.status_code == 200:
                break

            if resp.status_code == 401:
                if not self.authenticate():
                    return []
        
        return resp.json()
        

    def get_subscribers(self) -> list[AgsoSubscriber]:
        "Get all subscribers assigned to the API user, returns a list of AgsoSubscribers or None on error."
        resp = self.__authenticated_get("water/subscribers")
        if resp == None:
            return None

        subscribers = []
        for rs in resp:
            meters = []

            if rs["waterMeter1"] != None:
                meters.append(
                    AgsoMeter(
                        rs["waterMeter1"]["maxUnit"], rs["waterMeter1"]["waterMeterNr"]
                    )
                )

            if rs["waterMeter2"] != None:
                meters.append(
                    AgsoMeter(
                        rs["waterMeter2"]["maxUnit"], rs["waterMeter2"]["waterMeterNr"]
                    )
                )

            subscribers.append(
                AgsoSubscriber(
                    rs["payCustomer"]["customerNr"],
                    rs["subscriberNr"],
                    rs["payCustomer"]["firstName"],
                    rs["payCustomer"]["lastName"],
                    AgsoAddress(
                        rs["aboutLocation"]["streetName"],
                        rs["aboutLocation"]["addressNr"],
                        rs["aboutLocation"]["communityName"],
                        rs["aboutLocation"]["communityPostalCode"],
                        rs["aboutLocation"]["countryName"],
                        rs["aboutLocation"]["buildingName"],
                        rs["aboutLocation"]["description"],
                    ),
                    AgsoAddress(
                        rs["billingLocation"]["streetName"],
                        rs["billingLocation"]["addressNr"],
                        rs["billingLocation"]["communityName"],
                        rs["billingLocation"]["communityPostalCode"],
                        rs["billingLocation"]["countryName"],
                        rs["billingLocation"]["buildingName"],
                        rs["billingLocation"]["description"],
                    ),
                    rs["payCustomer"]["contactInfo"]["email"],
                    rs["payCustomer"]["contactInfo"]["fax"],
                    rs["payCustomer"]["contactInfo"]["mobileNumber"],
                    rs["payCustomer"]["contactInfo"]["phoneNumber"],
                    meters,
                )
            )

        if len(subscribers) > 0:
            self.customer_number = subscribers[0].customer_number
            self.subscriber_number = subscribers[0].subscriber_number

            if len(subscribers[0].meters) > 0:
                self.meter_number = subscribers[0].meters[0].meter_number

        return subscribers

    def __getValues(self) -> list[AgsoValue]:
        return []


    def get_accumulated_usage(self) -> list[AgsoValue]:
        if self.customer_number < 0:
            if len(self.get_subscribers()) == 0:
                return []

        req = requests.get(
            AgsoClient.BASE_URL
            + "water/"
            + str(self.customer_number)
            + "/"
            + str(self.subscriber_number)
            + "/data?timeType=DAY&dataType=AccumulatedValue",
            headers={"Authorization": "Bearer " + self.token},
            timeout=5000,
        )

        if req.status_code != 200:
            return []

        resp = req.json()

        values = []
        for rv in resp:
            if rv["waterMeterNr"] != self.meter_number:
                continue

            values.append(
                AgsoValue(rv["timeStamp"], rv["value"] * 1000, rv["estimation"])
            )

        return values

    def get_current_meter_reading(self) -> AgsoValue:
        values = self.get_accumulated_usage()
        value_count = len(values)

        if value_count == 0:
            return None

        return values[value_count - 1]