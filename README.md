# connect_data_lookup
A data lookup and visualisation tool using Ofcom's Connected Nations 2016 reports


Coding Challenge for LifeWorks
By Jim Doepp


Instructions:

1. Clone git repository or download and extract zip.
2. Create a new Python virtual environment with virtualenv.
    virtualenv --python=python3.7 /path/to/virtualenv
3. Source to virtualenv:
    source /path/to/virtualenv/bin/activate
3. Change directory to connect_data_lookup, and install requirements:
    cd connect_data_lookup
    pip install -r requirements.txt
4. Set up Django database migrations:
    ./manage.py makemigrations
    ./manage.py migrate
5. Run django:
    ./manage.py runserver
6. Access site at http://localhost:8000
7. Import data using http://localhost:8000/get_data/postcodes
    - This process takes about 5 minutes
    - The response is in JSON format

NOTES:
    - I have concentrated more on functionality and coding style rather than rendering.
    - This could be modified to be used as an API which could be accessed by another app, 
        (eg. a speed check app)
    - NaN values have been added to the database as -1

TO DO:
    - Add other related datasets (eg. Fixed local authority).
    - Currently if /get_data/postcodes is called, the database is cleared. Add a check on the size
        of the current database, and if the size is equal only allow import if forced (eg. ?force=true.
    - Some more exception calling for ingesting data.
    - Async functionality (using celery?) for loading postcodes.
    - Make it prettier.

