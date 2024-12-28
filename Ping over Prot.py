# Lib to Ping the server over port
import socket

# Libs to get variabels from PRTG and converting to JSON
import sys
import json

# Libs from PRTG to create the Custom Sensor 
from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from paesslerag_prtg_sensor_api.sensor.units import ValueUnit

# Request the Variables and format them 
data = json.loads(sys.argv[1])
params = data["params"].split(", ")

# Create the Translation 
locale = 'de'

translation = {
    'de': {
        'limit_error_msg': 'Der Server ist Offline',
    },
    'en': {
        'limit_error_msg': 'The server is offline',
    },
    'sp': {
        'limit_error_msg': 'El servidor está fuera de línea',
    },
    'fr': {
        'limit_error_msg': 'Le serveur est hors ligne',
    },
    'it': {
        'limit_error_msg': 'Il server è offline',
    },
    'pt': {
        'limit_error_msg': 'O servidor está offline',
    },
    'zh': {
        'limit_error_msg': '服务器离线',
    },
    'ja': {
        'limit_error_msg': 'サーバーがオフラインです',
    },
    'ru': {
        'limit_error_msg': 'Сервер не в сети',
    },
    'tr': {
        'limit_error_msg': 'Sunucu çevrimdışı',
    },
    'nl': {
        'limit_error_msg': 'De server is offline',
    }
}

# Defining the variables
server_host = params[0]
server_port = params[1]
server_name = params[2]

Value = 1

# fuction to check the Server
def check_server(host, port, timeout=5):
    try:
        with socket.create_connection((host, port), timeout):
            return True
    except (socket.timeout, socket.error):
        return False

# Checking the server and update the Value variable 
if check_server(server_host, server_port):
    Value = 1
else:
    Value = 3

# Create the Custom sensor and print them 
csr = CustomSensorResult(text='')

csr.add_primary_channel(name=server_name,
                        value=Value,
                        unit=ValueUnit.COUNT,
                        is_float=False,
                        is_limit_mode=True,
                        limit_max_error=2,
                        limit_error_msg=translation[locale]['limit_error_msg'])

print(csr.json_result)
