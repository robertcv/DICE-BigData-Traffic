import os

# Apache Kafka settings
KAFKA_HOST = 'host'
KAFKA_PORT = 'port'

# Bluetooth sensors
BT_SENSORS_LAST_URL = 'https://datacloud-timon.xlab.si/data_access/bt_sensors/velocities_avgs_last/'
BT_SENSORS_URL = 'https://datacloud-timon.xlab.si/data_access/bt_sensors/sensors/'
TIMON_USERNAME = 'username'
TIMON_PASSWORD = 'password'
TIMON_CRT_FILE = 'crt/datacloud.crt'
BT_SENSORS_IMG_DIR = 'image/'
BT_SENSORS_DATA_FILE = 'data/bt_sensors.json'
BT_SENSORS_DATA_AGE = 60 * 60 * 24 # 1 day
BT_SENSORS_NOT_USE = ['BTR0219', 'BTR0218', 'BTR0217', 'BTR0213']
BT_SENSORS_KAFKA_TOPIC = 'bt_json'

# Traffic counters
COUNTERS_URL = 'https://opendata.si/promet/counters/'
COUNTERS_IMG_DIR = 'image/'
COUNTERS_KAFKA_TOPIC = 'counter_json'

# Inductive loops
INDUCTIVE_LOOPS_HOST = '10.30.1.132'
INDUCTIVE_LOOPS_PORT = 9200
INDUCTIVE_LOOPS_INDEX = 'inductive_loops'
INDUCTIVE_LOOPS_IMG_DIR = 'image/'
INDUCTIVE_LOOPS_KAFKA_TOPIC = 'inductive_json'

# LPP traffic
LPP_STATION_URL = 'http://194.33.12.24/stations/getAllStations'
LPP_STATION_KAFKA_TOPIC = 'lpp_station_json'
LPP_STATION_FILE = 'data/stations.json'
LPP_STATION_DIRECTION_FILE = 'data/stations_directions.csv'

LPP_ROUTES_ON_STATION_URL = 'http://194.33.12.24/stations/getRoutesOnStation'
LPP_ROUTES_ON_STATION_FILE = 'data/routes_on_station.json'

LPP_STATIC_URL= 'http://194.33.12.24/timetables/getArrivalsOnStation'
LPP_STATIC_KAFKA_TOPIC = 'lpp_static_json'

LPP_LIVE_URL = 'http://194.33.12.24/timetables/liveBusArrival'
LPP_LIVE_KAFKA_TOPIC = 'lpp_live_json'

LPP_ROUTE_GROUPS_URL = 'http://194.33.12.24/routes/getRouteGroups'
LPP_ROUTE_URL = 'http://194.33.12.24/routes/getRoutes'
LPP_ROUTE_FILE = 'data/routes.json'

LPP_DATA_AGE = 60 * 60 * 24 # 1 day

# Air pollution
POLLUTION_URL = 'http://www.ljubljana.si/si/zivljenje-v-ljubljani/okolje-prostor-bivanje/stanje-okolja/zrak/'
POLLUTION_KAFKA_TOPIC = 'pollution_json'

# Ljubljana loaction
LJ_MIN_LNG = 14.44
LJ_MAX_LNG = 14.58
LJ_MIN_LAT = 46.0
LJ_MAX_LAT = 46.1

# Web scraper
SCRAPER_TIMEOUT = 0.5
SCRAPER_RETRIES = 10
SCRAPER_SLEEP = 2
SCRAPER_IGNORE_STATUS_CODE = False

# Environment overrides
locals().update(os.environ)

# Local overrides
try:
    from pytraffic.local_settings import *
except ImportError:
    pass