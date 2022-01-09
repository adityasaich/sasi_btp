import json
from flask import Flask, render_template, make_response, request
from model import model
import os
app = Flask(__name__)
classParams = {}
port = int(os.environ.get('PORT', 5000))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/stateDistrictMap', methods=['GET'])
def getStateDistrictMap():
    result = clf.params['labels']['State_District_Map']
    return {'result': result}


@app.route('/options')
def getOptions():
    result = '<option value=\'Select\'>Select</option>'
    for option in clf.params['labels'][request.args.get('param')]:
        result += '<option value=\'{option}\'>{option}</option>'.format(
            option=option)
    return {'result': result}


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    body = json.loads(request.data)
    response = {}
    try:
        response = clf.predict(
            body['district'], body['season'], int(body['year']), body['crop'])
        return make_response({"result": response[0]}, response[1])
    except Exception as err:
        print("while predicting error has occured " + str(err))
        return make_response("error while prediction", 500)


clf = model()
clf.main()
app.run(host='0.0.0.0', port=port, debug=False)
