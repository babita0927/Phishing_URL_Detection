import streamlit as st
import validators
import sklearn
import numpy as np
import pickle
import xgboost as xgb
from feature_extraction_function import main

# Load the XGBoost model using the save_model method to ensure compatibility with newer versions
booster = xgb.Booster()
booster.load_model('XGBClassifier_Final.model')
XGBClassifier1 = xgb.XGBClassifier()
XGBClassifier1._Booster = booster

# Define the Streamlit app
def app():
    # Define the main page
    st.title('Phishing URL Detection')
    st.write('Enter a URL below to check if it is safe or not.')

    # Create an input field for the URL
    url = st.text_input("Enter your site here:")

    # Create a button to run the model
    if st.button('Check URL'):
        # Run the model on the input URL
        features_test = main(url)
        features_test = np.array(features_test).reshape((1, -1))
        prediction = XGBClassifier1.predict(features_test)

        # Check if the URL is valid and show the appropriate result
        if validators.url(url):
            if prediction[0] == 0:
                if "@" in url:
                    result = "Provided URL is might be Phishing URL and unsafe to use"
                else:
                    result = "Provided URL is Safe to use"
            else:
                result = "Provided URL is might be Phishing URL and unsafe to use"
            st.write(result)
        else:
            st.write("Provided URL is might be Phishing URL and unsafe to use")


if __name__ == '__main__':
    app()
