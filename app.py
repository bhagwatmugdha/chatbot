from flask import Flask, request, jsonify, make_response
import requests
app = Flask(__name__)

# @app.route('/', methods =['GET'])
# def respond():
#     return jsonify({"reply":"What's Up"})

# @app.route('/', methods =['POST'])
# def verify():
#     data = request.data
#     return data

emojis = {
    "pos": ":)",
    "neutral": ":|",
    "neg": ":("
}

def fetch_results(query, lang):
    available_languages = ["english", "french", "dutch"]

    if lang.lower() not in available_languages:
        return "Sorry, " + lang + "not in the available languages."
    else:
        lang = lang.lower()
    
    url = 'http://text-processing.com/api/sentiment/'
    payload = {'text': query, 'lang': lang}
    response = requests.post(url, data = payload)

    if response.status_code == 200:
        json_response = response.json()
        label = json_response["label"]
        probability = json_response["probability"][label]
        emoji = emojis[label]

        result = query + " is " + label + " " + emoji + " : " + str(int(probability*100)) + "%"
    
    else:
        result = "request overlimit"

    return result

def results(request):
    action = request.get("queryResult")
    params = action['parameters']

    language = params['language']
    query = params['text']

    results = fetch_results(query = query, lang = language)

    response = {'fulfillmentText' : results}
    return response


@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
    res = results(request.get_json(force = True))
    print(jsonify(res))
    return make_response(jsonify(res))


if __name__ == "__main__":
    app.run(debug=True)
