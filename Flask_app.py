from flask import Flask, request, render_template
from feature_extraction_function import main
import numpy as np
import pickle
import validators

app = Flask(__name__)
# read our pickle file and label our XGBClassifier as model
XGBClassifier = pickle.load(open('XGBClassifier_Final.pkl', 'rb'))
urlError = {"Please enter url field"}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',  methods=['POST'])
def predict():
    url = request.form.get("EnterYourSite")
    features_test = main(url)
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = np.array(features_test).reshape((1, -1))
    prediction = XGBClassifier.predict(features_test)
    if validators.url(url):
        if prediction[0] == 0:
            if "@" in url:
                result = "Provided URL is might be Phishing URL and unsafe to use"
            else:
                result = "Provided URL is Safe to use"
        else:
            result = "Provided URL is might be Phishing URL and unsafe to use"
        return render_template('index.html', prediction_text=result)
    else:
        return render_template('index.html', prediction_text="Provided URL is might be Phishing URL and unsafe to use")


if __name__ == '__main__':
    app.run()
    #app.run(debug=True, port=5000, threaded=True)
