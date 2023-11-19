from flask import Flask, render_template
from python_opensky import OpenSky, OpenSkyStates

app = Flask(__name__)

def get_flight_states():
    with OpenSky(username="chicoreis", password="amendoim123") as opensky:
        states_response: OpenSkyStates = opensky.get_states()
        return states_response.states

@app.route('/')
def index():
    states = get_flight_states()
    return render_template('index.html', states=states)

if __name__ == '__main__':
    app.run(debug=True)

