import requests


class GetBoroughDetails:
    server_host = None
    server_port = None
    url_server = "http://{server_host}:{server_port}"
    url_list_of_places = "{url_server}/viewset/place/"
    url_harmed_at_borough = "{url_server}/viewset/place/?borough={borough}"
    url_harmed = "{url_server}/viewset/harmed/{collision_id}"

    def raise_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Server responded {response.status_code}")
            return response

        except (requests.exceptions.Timeout, \
                requests.exceptions.InvalidURL, \
                requests.exceptions.ReadTimeout, \
                requests.exceptions.ConnectionError, \
                requests.exceptions.RequestException, \
                ) as e:
            raise Exception(f"Unable to connect to server/Server not running.: {str(e)}")
        except:
            raise

    def get_cycles_harmed_details(self, borough):
        details = {"killed": 0, "injured": 0}
        response_borough = self.raise_request(
            self.url_harmed_at_borough.format(url_server=self.url_server, borough=borough))
        data_borough = response_borough.json()
        list_collision_id = [d["collision_id"] for d in data_borough]
        for collision_id in list_collision_id:
            response_harmed = self.raise_request(
                self.url_harmed.format(url_server=self.url_server, collision_id=collision_id))
            data_harmed = response_harmed.json()
            details["killed"] += data_harmed["cycl_killed"]
            details["injured"] += data_harmed["cycl_injured"]
        return details

    def get_borough_list(self):
        response = requests.get(self.url_list_of_places.format(url_server=self.url_server))
        data = response.json()
        borough_list = []
        for name in data:
            if name["borough"] not in borough_list:
                borough_list.append(name["borough"])
        return borough_list

    def __init__(self):
        server_host = input("Enter host(default:127.0.0.1): ") or "127.0.0.1"
        server_port = input("Enter host port(default:8000): ") or "8000"
        self.url_server = self.url_server.format(server_host=server_host, server_port=server_port)
        self.raise_request(self.url_server)

    def main(self):
        try:
            borough_list = self.get_borough_list()
            borough_list = {index: name for index, name in enumerate(borough_list)}
            borough = int(input(f"{borough_list}\nSelect borough: "))
            borough_num = borough_list.get(borough)
            if borough_num is None:
                raise Exception("Select valid borough")
            details = self.get_cycles_harmed_details(borough_num)
            print(f"Number of Cycles killed: {details['killed']}")
            print(f"Number of Cycles injured: {details['injured']}")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    data = GetBoroughDetails()
    data.main()
