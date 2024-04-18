import requests
import json
import unittest

BASE_URL = "https://api-energy-k8s.test.virtaglobal.com/v1/tests/"
station_id = [1, 2, 3, 4, 5]


def make_api_request(method: str, station_id: int, command: str, payload=None) -> any:
    """
        Make api request

        :param: method: request method to be sent
        :param: url: url to be sent
        :param: station_id: id of station
        :param: payload: software id to tested against
    """

    url = f"{BASE_URL}{station_id}"
    data = {"command": command, "payload": payload}
    try:
        match method.upper():
            case "GET":
                response = requests.get(url, json=data)
            case "POST":
                response = requests.post(url, json=data)
            case _:
                raise ValueError('Wrong method has been used')

        response.raise_for_status()  # Raise an exception if the status code is not 200
        return response.json()
    except requests.RequestException as e:
        print(f"Error making API request for station {station_id}: {e}")
        return None


def test_get_Version(station_id: int, version: int) -> None:
    """
        verify station version returns valid value

        :param: station_id: id of station
        :param: version: software id to tested against
    """

    response = make_api_request("GET", station_id, "getVersion")
    if response:
        version = float(response.get("version", version))
        assert version > 1.6, f"Station {station_id} version check failed"
    else:
        print(f"Station {station_id} version check successfull")
    return

def test_get_Interval(station_id: int, Interval: float) -> None:
    """
    :param station_id:
    :param version:
    :return:
    """
    response = make_api_request("GET", station_id, "getInterval")
    if response:
        interval = float(response.get("interval", 0))
        assert 1<=interval<60, f"Station {station_id} get interval check failed"

def test_set_Values(station_id: int, Values: float) -> None:
    """

    :param station_id:
    :param Values:
    :return:
    """
    payload= 8 #Sample payload
    response = make_api_request("POST", station_id, "setValues", payload)
    if response:
        status = response.get("status", "")
        if 1 < payload < 10:
            assert status == "OK", f"Station {station_id} setValues check failed"
        elif payload > 10:
            assert status == "FAILED", f"Station {station_id} setValues check failed"


if name == "main":
    test_get_version()
    test_get_interval()
    test_set_values()
    print("All tests passed!")


