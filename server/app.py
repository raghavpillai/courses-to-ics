from src.request import Requests
from src.parse import Parser
from src.ics_generator import IcsGenerator
import json
# Make a flask app
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def index():
    return "Default"

@app.route("/api/v1/", methods=['GET'])
def get():
    return "API v1\n/api/v1/get_classes - Get classes"

@app.route('/api/v1/get_classes', methods=['GET'])
def get_classes() -> str:
    #cookie = request.args.get('cookie')
    html = Requests.get_response_text()
    classes = Parser.get_classes(html)
    gened = IcsGenerator.get_ics_str(classes)
    # Return request
    return json.dumps({
        "errors": gened[0],
        "ics": gened[1]
    })

if __name__ == "__main__":
    html = Requests.get_response_text()
    classes = Parser.get_classes(html)
    print(classes)
    gened = IcsGenerator.get_ics_str(classes)
    with open("test.ics", "w") as f:
        f.write(gened[1])
    app.run(debug=True)