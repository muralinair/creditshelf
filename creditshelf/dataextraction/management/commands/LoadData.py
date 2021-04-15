import requests, pandas, numpy, zipfile, asyncio, traceback, aiohttp
from io import StringIO, BytesIO
from aiohttp import ClientSession, ClientTimeout
from dataextraction.models import Place, Crash, Harmed, Vehicle, Station, Trip, Bike
from tqdm import tqdm
from django.db import transaction
from dataextraction.management.commands.constants import Constants
from dataextraction.management.commands.Webdriverloader import WebdriverLoader
from .LoadDataException import LoadDataExeception


class Zip:

    def get_zip_content(self, file_name, bytes_obj):
        try:
            z = zipfile.ZipFile(BytesIO(bytes_obj))
            file_list = file_name.split(".")
            file_list.remove("zip")
            filename = ".".join(file_list)
            return z.read(filename), filename
        except zipfile.BadZipfile as e:
            raise LoadDataExeception("BAD_ZIP_FILE",e)
        except zipfile.LargeZipFile as e:
            raise LoadDataExeception("LARGE_ZIP_FILE",e)
        except Exception as e:
            raise e


class Csv:
    def generate_dataframe(self, csvObj, nanSubstitute=None):
        try:
            df = pandas.read_csv(csvObj)
            if nanSubstitute is not None:
                df.fillna(nanSubstitute, inplace=True)
            return df
        except pandas.errors.EmptyDataError as e:
            raise LoadDataExeception("EMPTY_CSV", e)
        except pandas.errors.ParserError as e:
            raise LoadDataExeception("INVALID_CSV", e)
        except Exception as e:
            raise e

    def convert_df_to_numerics(self, dataframe):
        try:
            return dataframe.apply(pandas.to_numeric, errors='ignore')
        except Exception as e:
            raise e

    def change_column_type(self, dataframe, columnname, type):
        try:
            dataframe[columnname] = dataframe[columnname].astype(type)
            return True
        except pandas.errors.ParserError as e:
            raise LoadDataExeception("INVALID_CSV", e)
        except Exception as e:
            raise e

    def retrieve_data_from_dataframe(self, df, start_ind, column_name, default_value, compare):
        try:
            return (df.iloc[start_ind, df.columns.get_loc(column_name)] if isinstance(
                df.iloc[start_ind, df.columns.get_loc(column_name)],
                compare) else default_value)
        except pandas.errors.EmptyDataError as e:
            raise LoadDataExeception("EMPTY_CSV", e)
        except pandas.errors.ParserError as e:
            raise LoadDataExeception("INVALID_CSV", e)
        except Exception as e:
            raise e


class Data(Zip, Csv, Constants):
    PBR = Constants.PBR

    def load_data(self):
        pass

    def get_data(self, url):
        pass


class Get_Sync(Data):
    def get_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise LoadDataExeception("INVALID_STATUS_CODE")
            return self.generate_dataframe((StringIO(response.text)), nanSubstitute=0)
        except (requests.exceptions.Timeout, \
                requests.exceptions.InvalidURL, \
                requests.exceptions.ReadTimeout, \
                requests.exceptions.ConnectionError, \
                requests.exceptions.RequestException, \
                ) as e:
            raise LoadDataExeception("UNABLE_TO_CONNECT_TO_ENDPOINT", e)
        except Exception as e:
            raise e

    @transaction.atomic
    def load_data(self):
        try:
            print("Syncing DB with API")
            with tqdm(total=2003) as pbar:
                self.PBR = pbar
                df = self.get_data(Constants.MOTOR_DATA_API)
                self.PBR.update()
                self.change_column_type(df, "zip_code", numpy.integer)
                self.PBR.update()
                df = self.convert_df_to_numerics(df)
                self.PBR.update()
                for index in range(df.shape[0]):
                    collision_id = self.retrieve_data_from_dataframe(df, index, "collision_id", 0, numpy.integer)
                    Crash.objects.get_or_create(
                        collision_id=collision_id,
                        defaults={
                            "date_of_crash":
                                self.retrieve_data_from_dataframe(df, index, "crash_date", "0000-00-00T00:00:00.000",
                                                                  str).split("T")[0],
                            "time_of_crash": self.retrieve_data_from_dataframe(df, index, "crash_time", "None", str)
                        }
                    )
                    self.PBR.update()
                for index in range(df.shape[0]):
                    c_id = self.retrieve_data_from_dataframe(df, index, "collision_id", 0, numpy.integer)
                    c = Crash.objects.get(collision_id=c_id)
                    Place.objects.get_or_create(
                        collision_id=c,
                        defaults={
                            "borough": self.retrieve_data_from_dataframe(df, index, "borough", "None", str),
                            "zip": self.retrieve_data_from_dataframe(df, index, "zip_code", 0000, numpy.integer),
                            "location_lat": self.retrieve_data_from_dataframe(df, index, "latitude", 0000,
                                                                              numpy.float64),
                            "location_log": self.retrieve_data_from_dataframe(df, index, "longitude", 0000,
                                                                              numpy.float64),
                            "on_street": self.retrieve_data_from_dataframe(df, index, "on_street_name", "None", str),
                            "off_street": self.retrieve_data_from_dataframe(df, index, "off_street_name", "None", str),
                            "cross_street": self.retrieve_data_from_dataframe(df, index, "off_street_name", "None",
                                                                              str),
                        }
                    )
                    Vehicle.objects.get_or_create(
                        collision_id=c,
                        defaults={
                            "veh_type_1": self.retrieve_data_from_dataframe(df, index, "vehicle_type_code1", "None",
                                                                            str),
                            "veh_type_2": self.retrieve_data_from_dataframe(df, index, "vehicle_type_code2", "None",
                                                                            str),
                            "veh_type_3": self.retrieve_data_from_dataframe(df, index, "vehicle_type_code_3", "None",
                                                                            str),
                            "veh_type_4": self.retrieve_data_from_dataframe(df, index, "vehicle_type_code_4", "None",
                                                                            str),
                            "veh_type_5": self.retrieve_data_from_dataframe(df, index, "vehicle_type_code_5", "None",
                                                                            str),
                        }
                    )
                    Harmed.objects.get_or_create(
                        collision_id=c,
                        defaults={
                            "ped_injured": self.retrieve_data_from_dataframe(df, index, "number_of_pedestrians_injured",
                                                                             0,
                                                                             numpy.integer),
                            "ped_killed": self.retrieve_data_from_dataframe(df, index, "number_of_pedestrians_killed",
                                                                            0,
                                                                            numpy.integer),
                            "cycl_injured": self.retrieve_data_from_dataframe(df, index, "number_of_cyclist_injured", 0,
                                                                              numpy.integer),
                            "cycl_killed": self.retrieve_data_from_dataframe(df, index, "number_of_cyclist_killed", 0,
                                                                             numpy.integer),
                            "motor_injured": self.retrieve_data_from_dataframe(df, index, "number_of_motorist_injured",
                                                                               0,
                                                                               numpy.integer),
                            "motor_killed": self.retrieve_data_from_dataframe(df, index, "number_of_motorist_killed", 0,
                                                                              numpy.integer),
                        }
                    )
                    self.PBR.update()
            return True
        except LoadDataExeception as l:
            print(l.mesg)
            print(traceback.format_exc())
            return False
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return False


class Get_Async(Data):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    frame_data = {}
    data_station = {}

    async def get_async_zip_content(self, file_name, r):
        data, filename = super().get_zip_content(file_name, r)
        self.frame_data[filename] = self.generate_dataframe(csvObj=StringIO(data.decode("utf-8")), nanSubstitute=0)

    async def gather_data_async(self, file_name, file_url):
        try:
            client_timeout = ClientTimeout(total=600)
            async with ClientSession(timeout=client_timeout) as session:
                r = await session.get(file_url)
                self.PBR.update()
                r.raise_for_status()
                r = await r.read()
                self.PBR.update()
                await self.get_async_zip_content(file_name, r)
        except aiohttp.ClientResponseError as e:
            raise LoadDataExeception("CLIENT_RESPONSE_ERROR", e)
        except aiohttp.ClientConnectorError as e:
            raise LoadDataExeception("CLIENT_CONNECTION_ERROR",e)
        except Exception as e:
            raise e

    async def main(self, url_text_map):
        task = [self.gather_data_async(url, url_text_map[url]) for url in url_text_map]
        await asyncio.gather(*task)

    def get_data(self, url):
        with WebdriverLoader(10) as web_driver:
            web_driver.start_phantom(url)
            elements = web_driver.get_elements(Constants.S3_Bucket_DATA_XPATH)
            url_text_map = web_driver.get_url_text_map(elements)
        asyncio.run(self.main(url_text_map))

    @transaction.atomic
    def load_data(self):
        try:
            print("Syncing DB with CSV")
            with tqdm(total=10779) as pbar:
                self.PBR = pbar
                self.get_data(Constants.S3_BUCKET_URL)
                self.PBR.update()
                for key in self.frame_data.keys():
                    start_station_ids = self.frame_data[key]['start station id'].unique()
                    stop_station_ids = self.frame_data[key]['end station id'].unique()
                    unique_station_ids = set(start_station_ids).union(stop_station_ids)
                    for station in unique_station_ids:
                        if station not in self.data_station:
                            frame = self.frame_data[key]
                            station_name = list(frame[self.frame_data[key]['start station id'] == station][
                                                    'start station name'].unique()) or list(
                                frame[self.frame_data[key]['end station id'] == station][
                                    'end station name'].unique())
                            station_location_log = list(frame[self.frame_data[key]['start station id'] == station][
                                                            'start station longitude'].unique()) or list(
                                frame[self.frame_data[key]['end station id'] == station][
                                    'end station longitude'].unique())
                            station_location_lat = list(frame[self.frame_data[key]['start station id'] == station][
                                                            'start station latitude'].unique()) or list(
                                frame[self.frame_data[key]['end station id'] == station][
                                    'end station latitude'].unique())
                            self.data_station[station] = {
                                "station_name": station_name[0],
                                "station_location_lat": station_location_lat[0],
                                "station_location_log": station_location_log[0]
                            }
                        self.PBR.update()

                for data in self.data_station:
                    Station.objects.get_or_create(
                        station_id=data,
                        defaults={
                            "station_name": self.data_station[data]["station_name"],
                            "location_lat": self.data_station[data]["station_location_lat"],
                            "location_log": self.data_station[data]["station_location_log"],
                        }
                    )
                    self.PBR.update()

                for key in self.frame_data.keys():
                    #self.frame_data[key].fillna(0, inplace=True)
                    for bikeid in self.frame_data[key]['bikeid'].unique():
                        Bike.objects.get_or_create(
                            id=bikeid
                        )
                    self.PBR.update()

                for key in self.frame_data.keys():
                    df = self.frame_data[key]
                    for index in range(1000):
                        start_id = self.retrieve_data_from_dataframe(df, index, "start station id", 0, numpy.integer)
                        stop_id = self.retrieve_data_from_dataframe(df, index, "end station id", 0, numpy.integer)
                        b_id = self.retrieve_data_from_dataframe(df, index, "bikeid", 0, numpy.integer)
                        s_start = Station.objects.get(station_id=start_id)
                        s_stop = Station.objects.get(station_id=stop_id)
                        bike_id = Bike.objects.get(id=b_id)
                        Trip.objects.get_or_create(
                            start_station_id=s_start,
                            stop_station_id=s_stop,
                            bike_id=bike_id,
                            defaults={
                                "start_time": self.retrieve_data_from_dataframe(df, index, "starttime",
                                                                                "0000-00-00 00:00:00.0000", str),
                                "stop_time": self.retrieve_data_from_dataframe(df, index, "stoptime",
                                                                               "0000-00-00 00:00:00.0000", str),
                                "usertype": self.retrieve_data_from_dataframe(df, index, "usertype", "None", str),
                                "yod": self.retrieve_data_from_dataframe(df, index, "birth year", 0000, numpy.integer),
                                "gender": self.retrieve_data_from_dataframe(df, index, "gender", 0, numpy.integer),
                            }
                        )
                    self.PBR.update()
                return True
        except LoadDataExeception as l:
            print(l)
            print(traceback.format_exc())
            return False
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return False
