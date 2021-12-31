from flask import Flask, render_template,request
import model
app = Flask(__name__)
classParams = {}
import json

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/stateDistrictMap',methods=['GET'])
def getStateDistrictMap():
    result = classParams['params']['labels']['State_District_Map']
    return {'result':result}

@app.route('/options')
def getOptions():
    result = ''
    for option in classParams['params']['labels'][request.args.get('param')]:
        result += '<option value=\'{option}\'>{option}</option>'.format(option=option)
    return {'result':result}

@app.route('/predict',methods=['GET','POST'])
def predict():
    body = json.loads(request.data)
    response={}
    try:
        return{ 'result':classParams['obj'].predict(body['district'],body['season'],int(body['year']))}
    except Exception as err:
        response['body'] = str(err)
        response['status'] = 500
        return response

classParams['obj'] = model.start()
f = open('params_from_ml.json')
data = json.load(f)
f.close()
classParams['params'] = data
app.run(debug=False)