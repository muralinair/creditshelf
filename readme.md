# Creditshelf Coding Challenge

This is a demo repo for Credishelf recruting

Note: This project assues that  
    1. You are running on Windows  
    2. You already have installed Python version. Following code has been written on ver: 3.9  
    3. Have an active internet

  
    1.  Create virtual env by running the following  
            python -m venv <virtual environment name>  
    2.  Activate your virtual environment.
            run <virtual environment name>/Scripts/activate.bat
    3. This should add (<virtual env name>) to your prompt.

    4.  Run git pull to download the repository after forking.
        Note: Code is in master branch.
    5.  Run pip install -r requirements.txt
    6.  Goto Django prject folder where manage.py is situated.
    7.  Run the following commands 
                python manage.py makemigrations
                python manage.py migrate
                (optional): If you wish to see models in admin page
                        python manage.py createsuperuser
                            and endter details required on console.
                python manage.py syncdb
                    This will get details from web(both web and csv) and save it to models/DB.
                    This operation might take time. ~8mins depending on your internet speed.
    8.  Goto Settings.py in creditshelf/creditshelf folder and copy API key into API_KEY variable.
        Note: If you don't have API key you can follow below given instructions to get one.
            This project uses Google Maps API and Google Directions API to render few features. This 
            only works with a valid API Key as free support for maps and directions API has been depricated.
            With that said, a key needs to be created from Google Cloud Platform. I cannot put my key on public
            repos due to security reasons. 
            Note: Even though Google Cloud Platform asks for billable details, you dont have to worry for being
                    charged as this project usage resides well below free quota. 
                *  After creating Google Cloud Platform(GCP) Accout using G-Mail ID
                *  Goto Console on top right corner
                *  Click on 'Home->Dashboard' and select 'New Project'.
                *  Enter project name and hit create. This will create a new project under GCP. This might take some time.
                *  Click on 'API service->Library' and select 'Maps Javascript API' and click 'Enable'
                *  Repeat same for 'Directions API'. If you dont see Directions API on the list click on 'View all'
                *  You will be taken to API services Dashboard after enabling API.
                *  On the dashboard click on 'Credentials'
                *  After page loads click on 'Credentials in APIs & Services'
                *  click on 'CREATE CREDENTIALS' on the top and select 'API Key'.
                *  This will generate new API key. Copy this key and add to settings.py. We need to add billing account to 
                   use Maps and Directions API.
                   Note: This may be enough to see Maps but markers and directions will not work.
                   If you try to use this credentials you will get error on browser console 'You must enable billing on GCP'
                *  Click on Billing under Navigation menu(three horizontal lines) on top left.
                *  Click on 'Manage Billing' and then 'Create Accout'.
                *  Enter deails in the presented page. Select 'Google Maps Platform' for 'Business the billing account will pay for'
                *  Enter details in the next page and submit. 
                *  Now you Key should be up for Directions and Maps.
             
    
    9. After you see 'SyncDB Successful' on the prompt. Run the following command:
            python manage.py runserver
                This will start local dev server
    10. goto link mentioned in the console after server has started.
    
This is how page would look like on startup:
![alt text](https://github.com/muralinair/creditshelf/blob/120458d79d66d97b2811e7737076354a34c5c92f/creditshelf/static/images/before_borough.png?raw=true)
This is how page would look like after you have selected Borough:
![alt text](https://github.com/muralinair/creditshelf/blob/120458d79d66d97b2811e7737076354a34c5c92f/creditshelf/static/images/after_borough.png?raw=true)
    
    
