from flask import Flask, render_template
from opensky_api import OpenSkyApi

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        print("Acessando a rota /")

        api = OpenSkyApi()
        print("Chamando api.get_states()")
        states = api.get_states()

        # Imprima mais informações sobre a resposta da API
        print(f"Tipo de resposta: {type(states)}, Dados da resposta: {states}")

        # Verifique se a resposta da API não é None
        if states is not None and states.states is not None:
            print("Processando dados da API")

            # Crie uma lista de dicionários com as informações relevantes
            aircraft_data = [
                {
                    'icao24': s.icao24,
                    'callsign': s.callsign,
                    'longitude': s.longitude,
                    'latitude': s.latitude,
                    'baro_altitude': s.baro_altitude,
                    'velocity': s.velocity
                } for s in states.states
            ]

            print("Dados processados com sucesso")

            return render_template('index.html', aircraft_data=aircraft_data)

        else:
            # Caso a resposta da API seja None
            print("A resposta da API é None")
            return "Não foi possível obter dados da OpenSky API."

    except Exception as e:
        # Imprima a exceção no console
        print(f"Erro na aplicação Flask: {str(e)}")
        # Retorne uma mensagem de erro genérica para o usuário
        return "Ocorreu um erro na aplicação Flask. Por favor, tente novamente mais tarde."

if __name__ == '__main__':
    app.run(debug=True)
