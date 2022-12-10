# Team-2-Mental-Illness-Chatbot
This is a practicum project for the CS 6440 Intro to Health Informatics course at Georgia Tech. We have built a chatbot app that allows a user to message a chatbot, when they are unable to immediately consult their healthcare provider, about symptoms they are experiencing and receive responses that tell them what physical illnesses (illnesses pertaining to physical health, like influenza, common cold, etc.) and mental illnesses (illnesses pertaining to mental health, specifically depression, anxiety, and bipolar disorder) they may be at risk of and what precautions/treatments they can take. This app does not provide official medical feedback, diagnoses, treatments, etc. The user must consult their healthcare provider to receive official medical care.

There are three parts to the chatbot system: the mobile user interface, the server (including the database), and the machine learning suite.

## Getting Started 
Create a Python virtual environment as described here: `https://docs.python.org/3/library/venv.html`. With your virtual environment activated and `pip3` installed on your system, install the dependencies with the command `pip3 install -r requirements.txt`.

## Machine Learning Suite

### Physical Illness Prediction 
The physical illness prediction (PIP) pipeline trains and evaluates machine learning models that extract the symptoms the user is experiencing from their message and use that information to predict the physical illnesses the user may be at risk of given their symptoms. These models are trained on data from a Kaggle physical diseases dataset, found here: https://www.kaggle.com/itachi9604/disease-symptom-description-dataset. Citation: Patil, P. (2020, May 24). Disease Symptom Prediction. Kaggle. Retrieved March 6, 2022, from https://www.kaggle.com/itachi9604/disease-symptom-description-dataset

The PIP pipeline can be run by executing the `./models/physical_illness_prediction.py` script via command line and specifying the according arguments, which are described below. 

`--proc_data`: set to 0 (default) to process initial physical diseases dataset from scratch, set to any other integer (or omit this argument) to use existing processed datasets. 

`--fit_se_nn`: set to 0 to fit and evaluate multi-output classifier of neural networks for symptom extraction from scratch, set to 1 to load existing model, set to any other integer (or omit this argument) to skip (default value is 2). 

`--fit_pip_rf`: set to 0 to fit and evaluate random forest classifier for symptom extraction from scratch, set to 1 to load and evaluate existing model, set to any other integer (or omit this argument) to skip (default value is 2). 

`--fit_pip_nn`: set to 0 to fit and evaluate neural network classifier for symptom extraction, from scratch, set to 1 to load and evaluate existing model, set to any other integer (or omit this argument) to skip (default value is 2). 

Example command to process dataset and fit/evaluate all models from scratch: 
`python3 ./models/physical_illness_prediction.py --fit_se_nn 0 --fit_pip_rf 0 --fit_pip_nn 0 > ./models/physical_illness_prediction_logs.txt`

Example command to load existing dataset and load/evaluate all existing models:  
`python3 ./models/physical_illness_prediction.py --proc_data 1 --fit_se_nn 1 --fit_pip_rf 1 --fit_pip_nn 1 > ./models/physical_illness_prediction_logs.txt`

Example command to load existing dataset, load/evaluate symptom extraction model, and fit/evaluate physical illness prediction models from scratch: 
`python3 ./models/physical_illness_prediction.py --proc_data 1 --fit_se_nn 1 --fit_pip_rf 0 --fit_pip_nn 0 > ./models/physical_illness_prediction_logs.txt`

Example command to process dataset, fit/evaluate symptom extraction model, and skip other physical illness prediction models: 
`python3 ./models/physical_illness_prediction.py --fit_se_nn 0 > ./models/physical_illness_prediction_logs.txt`

The first step in the PIP pipeline processing the physical diseases dataset into two datasets, one that can be used to train a symptom extraction model (`./models/pip_symptom_extraction_dataset.csv.zip`, stored as a ZIP file due to size) and another that can be used to train physical illness prediction models (`./models/processed_pip_dataset.csv`). Additionally, a JSON file is created to store the names/numerical labels of the diseases and the unique symptoms of the dataset (`./models/pip_disease_labels_symptoms.json`). 

The second step is training, evaluating, and saving the symptom extraction model, which is a multi-output classifier consisting of several neural networks that predicts the symptoms described in a user's message. This model is saved in the `./models/pip_se_neural_network.joblib` file as a pipeline that consists of a TF-IDF vectorizer and the multi-output classifier itself. 

The third step is training, evaluating, and saving a random forest model for physical illness prediction. This model is saved in the `./models/pip_random_forest.joblib` file as a pipeline that consists of a standard scaler and the random forest model itself. 

The fourth step is training, evaluating, and saving a neural network model for physical illness prediction. This model is saved in the `./models/pip_neural_network.joblib` file as a pipeline that consists of a standard scaler and the random forest itself. 

The models' respective performances on training data, testing data, and various folds of data can be seen in the log file `./models/physical_illness_prediction_logs.txt` file. 

### Mental Illness Prediction 
The mental illness prediction (MIP) model aims to predict the mental illnesses the user may be at risk of given what symptoms they are experiencing. 

The MIP pipeline can be run by executing the `./models/mental_illness_prediction.py` script via command line.

The first step in the MIP pipeline processing the emotions testing, training, and validation datasets through a Logistic Regressional model to train the classifier. This is done by utilizing the pandas framework to convert the csv's into dataframes that can be used by the sklearn model. The features and labels are then seperated and passed in to begin training.

The second step is the training of the logistical regression model and saving the model to be used for the entire duration of the application's lifecycle. Similar to the PIP Pipleine, the produced models are saved with the `./models/mip_classifier_logistic_regression.joblib` and `./models/mip_vectorizer_logistic_regression.joblib`, and they can be continuously loaded when required.
  
The final step is analyizing the  the messages sent by the user and determining the most probable mental illness by the distribution of sentiments from the messages. The probable illnesses are as follows:
- Depression
- Bipolar Disorder
- Anxiety

### Chatbot (Response Builder)
The response builder uses the results from the PIP and the MIP model to format a response to send back the user. For communicating physical illness risks, the response builder sends the user's message to the PIP models which determine the user's most likely physical illness risks, which are formatted into a simple, easily readable message that is sent back to the user. The specific number of physical illness risks that are shown in the response is defined in the `./response_builder.py` file and can be updated as needed. 

The chatbot is tested for physical illness prediction and mental illness prediction in the `./test.py` script, which can be run with the following command: `python3 ./test.py > ./response_builder_test_logs.txt`. The results of the tests can be inspected in the `./response_builder_test_logs.txt` file. 
