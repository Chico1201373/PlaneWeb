from flask import Flask, render_template
from opensky_api import OpenSkyApi
import sqlite3
from flask import jsonify
from config import ENCRYPTED_USERNAME, ENCRYPTED_PASSWORD
app = Flask(__name__)


def decrypt_credentials(encrypted_username, encrypted_password):
    username = encrypted_username
    password = encrypted_password
    return username, password

username, password = decrypt_credentials(ENCRYPTED_USERNAME, ENCRYPTED_PASSWORD)

def create_table():
    connection = sqlite3.connect("flights.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_states (
            icao24 TEXT,
            callsign TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            on_ground INTEGER,
            heading REAL,
            velocity REAL,
            vertical_rate REAL,
            sensors INTEGER,
            time_position INTEGER,
            spi INTEGER,
            squawk TEXT,
            alert INTEGER,
            true_track REAL,
            emergency INTEGER
        )
    ''')
    connection.commit()

def get_flight_state_base():
    connection = sqlite3.connect("flights.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM flight_states')
    flight_states = cursor.fetchall()
    connection.close()
    return flight_states

def get_flight_state_api_sync():
    api = OpenSkyApi(username, password)
    response = api.get_states()
    #response.status_code == 200 and 
    if response and response.states is not None:
        connection = sqlite3.connect("flights.db")
        cursor = connection.cursor()
        for state in response.states:
            cursor.execute('''
                INSERT INTO flight_states VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                state.icao24,
                state.callsign,
                state.origin_country,
                state.latitude,
                state.longitude,
                state.baro_altitude,
                state.on_ground,
                state.true_heading,
                state.velocity,
                state.vertical_rate,
                state.sensors,
                state.time_position,
                state.spi,
                state.squawk,
                state.alert,
                state.true_track,
                state.emergency
            ))
        connection.commit()
        connection.close()

def get_countrys():
    flight_states = get_flight_state_base()
    unique_countries = set(state[2] for state in flight_states)
    unique_countries_list = sorted(list(unique_countries))
    return unique_countries_list


@app.route('/')
async def index():
    create_table()
    get_flight_state_api_sync()
    flight_states = get_flight_state_base()
    unique_countries_list = get_countrys()
    return render_template('index.html', states=flight_states,countries =unique_countries_list )


@app.route('/atualizar_dados')
def atualizar_dados():
    current_flight_states = get_flight_state_base()
    get_flight_state_api_sync()
    updated_flight_states = get_flight_state_base()

    if current_flight_states != updated_flight_states:
        unique_countries_list = get_countrys()
        return jsonify(success_message="Dados atualizados com sucesso.",states=updated_flight_states,countries =unique_countries_list)
    
    return jsonify(error_message="Erro: Os dados não foram atualizados.")


@app.route('/get_flight_states')
def get_flight_states():
    flight_states = get_flight_state_base()
    unique_countries_list = get_countrys()
    return jsonify(states=flight_states,countries =unique_countries_list )

if __name__ == '__main__':
    app.run(debug=True)

