from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from weather import get_current_weather
#from waitress import serve
from chat import get_response

app = Flask(__name__)
CORS(app)

#####@app.route("/", methods=["GET"])

@app.route('/')
def index():
    return render_template('index.html')


### For Weather app data ###
@app.get('/weather')
def get_weather():
    
    city = request.args.get('city')
    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
    
    return render_template(        
        "base.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        humidity=f"{weather_data['main']['humidity']:.1f}",
        pressure=f"{weather_data['main']['pressure']:.1f}"
    )

#This will handle the chatbot request

@app.post("/predict")
def predict():    
    text = request.get_json().get("message")
    #TODO: Check error
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run()


