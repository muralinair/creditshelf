from creditshelf.settings import PHANTOMJS_EXE

class Constants:
    PBR = None
    S3_BUCKET_URL = "https://s3.amazonaws.com/tripdata/index.html"
    MOTOR_DATA_API = "https://data.cityofnewyork.us/resource/h9gi-nx95.csv"
    S3_Bucket_DATA_XPATH = "//a[contains(text(),'tripdata') and contains(text(),'2019') and not(contains(text(),'JC-'))]"
    PHANTOMJS_EXE = PHANTOMJS_EXE
