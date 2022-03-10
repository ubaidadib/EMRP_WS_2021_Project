import psycopg2
import pandas.io.sql as psql
import pandas as pd
import credentials as creds
# ********************************************
# to execute everything inside queries.py file
from queries import *
# ********************************************
#from logger import logger


# Define our connection string
conn_string = "host=" + creds.PGHOST + " port=" + "5432" + " dbname=" + creds.PGDATABASE + " user=" + creds.PGUSER \
    + " password=" + creds.PGPASSWORD
conn = psycopg2.connect(conn_string)
print("Connected to server!")

# Create a cursor object
cursor = conn.cursor()


def get_all(schema, table):  # Show-Up all TrashBins and Device_id

    query = "SELECT * FROM public.ta_trashbin ORDER BY bin_id ASC"
    conn_trashbin_dev = pd.read_sql(query, conn)
    return conn_trashbin_dev


def get_active(schema, table):  # Show-Up all Measurments of Active Sensor
    cursor.callproc('db_exec')
    query = "SELECT * FROM public._dynamic_pivot"
    active_meas = pd.read_sql(query, conn)
    return active_meas


def get_failure(schema, table):  # Show-Up all Measurments of In-Active Sensor

    query = "SELECT * FROM public.vi_prob_meas ORDER BY dev_eui ASC"
    failure_meas = pd.read_sql(query, conn)
    return failure_meas


def get_distance(schema, table):
    query = "SELECT * FROM public.vi_last_meas WHERE channel = 'distance' order by last_date"
    dist = pd.read_sql(query, conn)
    return(dist)


def get_temperature(schema, table):
    query = "SELECT * FROM public.vi_last_meas WHERE channel = 'temperature' order by last_date"
    temp = pd.read_sql(query, conn)
    return(temp)
