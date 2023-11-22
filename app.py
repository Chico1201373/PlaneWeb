from flask import Flask, render_template
from opensky_api import OpenSkyApi
import sqlite3

app = Flask(__name__)

# Função para criar a tabela se não existir
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
            emergency INTEGER
        )
    ''')
    connection.commit()

async def get_flight_state():
    api = OpenSkyApi("chicoreis", "123123")
    #api = OpenSkyApi("chico1", "123123")

    response = api.get_states()

    print(response)

    return response

@app.route('/')
async def index():
    # Criar a tabela se não existir
    create_table()

    # Obter os dados de voo
    response = await get_flight_state()

    # Carregar os dados da base de dados
    connection = sqlite3.connect("flights.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM flight_states')
    flight_states = cursor.fetchall()

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
            state.true_track,
            state.velocity,
            state.vertical_rate,
            state.sensors,
            state.time_position,
            state.spi,
            state.squawk,
            state.position_source,
            state.category
        ))

    connection.commit()

    return render_template('index.html', states=flight_states)

if __name__ == '__main__':
    app.run(debug=True)

