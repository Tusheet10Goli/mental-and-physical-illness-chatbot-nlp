# imports
import joblib 
import numpy as np
import os
import pandas as pd
import platform
from pip_datasets import (
    process_dataset, 
    get_from_file_disease_labels_symptoms, 
    PROCESS_DATASET_CSV_SAVE_PATH, 
    SYMPTOM_EXTRACTION_DATASET_SAVE_PATH
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import f1_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import texthero as hero
from texthero import preprocessing
import traceback


# define constants
CURR_FILE = os.path.abspath(__file__)
CURR_DIR = CURR_FILE[:CURR_FILE.rfind('/') + 1]
if platform.system() == 'Windows':
    CURR_DIR = CURR_FILE[:CURR_FILE.rfind('\\') + 1]
TFIDF_PARAMS = {
    'max_features': 250,
}
SE_NN_HYPERPARAMS = {
    'hidden_layer_sizes': (60, 40),
    'activation': 'relu',
    'solver': 'adam',
    'learning_rate': 'constant',
    'learning_rate_init': 0.0002,
    'max_iter': 10
} 
SE_NN_SAVE_PATH = CURR_DIR + 'pip_se_neural_networks.joblib'
PIP_RF_HYPERPARAMS = {
    'n_estimators': 14, 
    'max_depth': 16,
    'min_samples_split': 40
}
PIP_RF_SAVE_PATH = CURR_DIR + 'pip_random_forest.joblib'
PIP_NN_HYPERPARAMS = {
    'hidden_layer_sizes': (300, 200), 
    'activation': 'relu',
    'solver': 'adam',
    'learning_rate': 'constant',
    'learning_rate_init': 0.00001,
    'max_iter': 250
} 
PIP_NN_SAVE_PATH = CURR_DIR + 'pip_neural_network.joblib'
SE_TEST_SET_SIZE = 0.35
PIP_TEST_SET_SIZE = 0.2
SE_K_SPLITS = 20
PIP_K_SPLITS = 10 
# set to whichever model performs better on unseen data (see model_logs.txt)
# 0 for random forest, any other integer for neural network
DEFAULT_PIP_MODEL_CHOICE = 1 
# update paths for windows 
if platform.system == 'Windows':
    CURR_FILE = CURR_FILE.replace('/', '\\')
    CURR_DIR = CURR_DIR.replace('/', '\\')
    SE_NN_SAVE_PATH = SE_NN_SAVE_PATH.replace('/', '\\')
    PIP_RF_SAVE_PATH = PIP_RF_SAVE_PATH.replace('/', '\\')
    PIP_NN_SAVE_PATH = PIP_NN_SAVE_PATH.replace('/', '\\')


# function for processing text
def process_text(df): 
    # specify cleaning pipeline 
    text_processing_pipeline = [
        preprocessing.lowercase, 
        preprocessing.remove_digits, 
        preprocessing.remove_stopwords, 
        preprocessing.remove_punctuation,
        preprocessing.remove_whitespace
    ] 

    # clean text, assumed to be in first column
    text_name = df.columns.values.tolist()[0]
    df[text_name] = df[text_name].pipe(hero.clean, text_processing_pipeline)

# evaluate model on a single train-test split
def evaluate_model_single_split(model, train_features, test_features, 
    train_labels, test_labels, test_size): 
    print('Evaluating model based on single train-test '
        + f'({round((1 - test_size) * 100)}% - {round(test_size * 100)}%) '
        + 'split...')

    # score model on training data 
    train_acc = model.score(train_features, train_labels)
    print(f'Model train accuracy: {train_acc}')

    # get model f1 score on training data 
    train_preds = model.predict(train_features)
    train_f1 = f1_score(train_preds, train_labels, average='weighted')
    print(f'Model train F1 score: {train_f1}')

    # score model on testing data 
    test_acc = model.score(test_features, test_labels)
    print(f'Model test accuracy: {test_acc}')

    # get model f1 score on testing data 
    test_preds = model.predict(test_features)
    test_f1 = f1_score(test_preds, test_labels, average='weighted')
    print(f'Model test F1 score: {test_f1}')

# evaluate model using k-fold cross validation 
def evaluate_model_k_fold_cross_validation(model, features, labels, k=5): 
    print(f'Evaluating model based on k-fold (k={k}) cross validation...')

    # get k splits and evaluate model on each split 
    kfold = KFold(n_splits=k, random_state=None, shuffle=True)
    split_value = 1
    for _, fold_indices in kfold.split(features, labels):
        fold_features = features.iloc[fold_indices]
        fold_labels = labels.iloc[fold_indices]

        # score model on test split 
        fold_acc = model.score(fold_features, fold_labels)
        print(f'Model accuracy, k-fold split {split_value}: {fold_acc}')

        # get model f1 score on test split 
        test_preds = model.predict(fold_features)
        fold_f1 = f1_score(test_preds, fold_labels, average='weighted')
        print(f'Model F1 score, k-fold split {split_value}: {fold_f1}')
        
        # prepare for next split
        split_value += 1

# function to prepare data for symptom extraction model 
def _prepare_data_for_se_model(symptom_extraction_df): 
    # split data into features and labels 
    column_names = symptom_extraction_df.columns.values.tolist()
    features_df = pd.DataFrame(symptom_extraction_df[column_names[0]])
    labels = symptom_extraction_df[column_names[1:]]

    # process text features 
    process_text(features_df)
    text_column = features_df.columns.values.tolist()[0]
    features = features_df[text_column]
    
    # split data into training and testing sets 
    (train_features, test_features, train_labels, 
        test_labels) = train_test_split(features, labels, 
        test_size=SE_TEST_SET_SIZE, shuffle=True)
    
    # return features and labels 
    return (features, train_features, test_features, labels, train_labels, 
        test_labels)

# function to fit a symptom extraction model 
def _fit_se_model(symptom_extraction_df, model): 
    # split data into training and testing sets 
    (features, train_features, test_features, labels, train_labels, 
        test_labels) = _prepare_data_for_se_model(symptom_extraction_df)

    # fit model 
    model_pipeline = Pipeline([('tfidf_vectorizer', 
        TfidfVectorizer(**TFIDF_PARAMS)), ('model', model)])
    model_pipeline.fit(train_features, train_labels)

    # evaluate model on current split 
    evaluate_model_single_split(model_pipeline, train_features, test_features, 
        train_labels, test_labels, SE_TEST_SET_SIZE)

    # evaluate model using k-fold cross validation 
    evaluate_model_k_fold_cross_validation(model_pipeline, features, labels, 
        SE_K_SPLITS)
    
    # return model
    return model_pipeline

# function to prepare data for physical illness prediction model 
def _prepare_data_for_pip_models(processed_df):
    # split data into features and labels 
    feature_names = processed_df.columns.values.tolist()
    features = processed_df[feature_names[:-1]]
    labels = processed_df[feature_names[-1]]

    # split data into training and testing sets 
    (train_features, test_features, train_labels, 
        test_labels) = train_test_split(features, labels, 
        test_size=PIP_TEST_SET_SIZE, shuffle=True)

    # return train and test features and labels 
    return (features, train_features, test_features, labels, train_labels, 
        test_labels)

# function to fit a physical illness prediction model
def _fit_pip_model(processed_df, model):
    # split data into training and testing sets 
    (features, train_features, test_features, labels, train_labels, 
        test_labels) = _prepare_data_for_pip_models(processed_df)

    # fit model pipeline 
    model_pipeline = Pipeline([('std_scaler', StandardScaler()), ('model', 
        model)])
    model_pipeline.fit(train_features, train_labels)

    # evaluate model on current split 
    evaluate_model_single_split(model_pipeline, train_features, test_features,
        train_labels, test_labels, PIP_TEST_SET_SIZE)

    # evaluate model with k-fold cross validation
    evaluate_model_k_fold_cross_validation(model_pipeline, features, labels, 
        PIP_K_SPLITS)

    # return model pipeline 
    return model_pipeline 

# function to fit all models
def fit_models(proc_data=0, fit_se_nn=2, fit_pip_rf=2, 
    fit_pip_nn=2): 
    # process dataset 
    processed_df, symptom_extraction_df = None, None
    if proc_data == 0: 
        _, processed_df, symptom_extraction_df = process_dataset()
    else: 
        try: 
            print('Loading existing processed datasets...')
            processed_df = pd.read_csv(PROCESS_DATASET_CSV_SAVE_PATH)
            symptom_extraction_df = pd.read_csv(
                SYMPTOM_EXTRACTION_DATASET_SAVE_PATH)
        except Exception as e: 
            # print error information 
            print('An error occurred with loading existing data, shown below:')
            print(e)
            traceback.print_exc()
            print('Exiting...')
            return 

    # fit or load existing model for symptom extraction 
    if fit_se_nn == 0:
        # fit and save model for symptom extraction
        print('Fitting multi-output classifier of neural networks for symptom ' 
            + 'extraction...') 
        se_nn = _fit_se_model(symptom_extraction_df, MultiOutputClassifier(
            MLPClassifier(**SE_NN_HYPERPARAMS)))
        print('Saving neural network model at ' 
            + f'{SE_NN_SAVE_PATH[len(CURR_DIR):]}')
        joblib.dump(se_nn, SE_NN_SAVE_PATH)
    elif fit_se_nn == 1: 
        try: 
            # load existing model for symptom extraction
            print('Loading existing multi-output classifier of neural networks ' 
                + 'for symptom extraction...')
            se_nn = joblib.load(SE_NN_SAVE_PATH)

            # evaluate loaded model 
            (features, train_features, test_features, labels, train_labels, 
                test_labels) = _prepare_data_for_se_model(symptom_extraction_df)
            evaluate_model_single_split(se_nn, train_features, test_features, 
                train_labels, test_labels, SE_TEST_SET_SIZE)
            evaluate_model_k_fold_cross_validation(se_nn, features, labels, 
                SE_K_SPLITS)
        except Exception as e: 
            # print error information 
            print('An error occurred with loading/evaluating existing symptom '
                + 'extraction models, shown below:') 
            print(e)
            traceback.print_exc()
            print('Exiting...')
            return 
    else:
        # skip 
        print('Skipping fitting/loading multi-output classifier of neural ' 
            + 'networks for symptom extraction...')

    # get train and test features and labels from processed data
    (features, train_features, test_features, labels, train_labels, 
        test_labels) = _prepare_data_for_pip_models(processed_df)

    # fit or load existing model for physical illness prediction 
    if fit_pip_rf == 0:
        # fit and save model for physical illness prediction
        print('Fitting random forest model for physical disease ' 
            + 'classification...')
        pip_rf = _fit_pip_model(processed_df, 
            RandomForestClassifier(**PIP_RF_HYPERPARAMS))
        print('Saving random forest model at ' 
            + f'{PIP_RF_SAVE_PATH[len(CURR_DIR):]}') 
        joblib.dump(pip_rf, PIP_RF_SAVE_PATH)
    elif fit_pip_rf == 1: 
        try: 
            # load existing model for physical illness prediction 
            print('Loading existing random forest model for physical disease ' 
                + 'classification...')
            pip_rf = joblib.load(PIP_RF_SAVE_PATH)

            # evaluate loaded model 
            evaluate_model_single_split(pip_rf, train_features, test_features, 
                train_labels, test_labels, PIP_TEST_SET_SIZE)
            evaluate_model_k_fold_cross_validation(pip_rf, features, labels, 
                PIP_K_SPLITS)
        except Exception as e: 
            # print error information 
            print('An error occurred when loading/evaluating existing random '
                + 'forest model for physical disease classification, shown '
                + 'below:') 
            print(e)
            traceback.print_exc()
            print('Exiting...')
            return 
    else:  
        # skip 
        print('Skipping fitting/loading random forest model for physical ' 
            + 'disease classification...')

    # fit or load existing model for physical illness prediction
    if fit_pip_nn == 0:
        # fit and save neural network model for physical illness prediction
        print('Fitting neural network model for physical ' 
            + 'disease classification...')
        pip_nn = _fit_pip_model(processed_df, 
            MLPClassifier(**PIP_NN_HYPERPARAMS))
        print('Saving neural network model at ' 
            + f'{PIP_NN_SAVE_PATH[len(CURR_DIR):]}')
        joblib.dump(pip_nn, PIP_NN_SAVE_PATH)
    elif fit_pip_nn == 1: 
        try: 
            # load existing model for physical illness prediction 
            print('Loading existing neural network model for physical disease '
                + 'classification...')
            pip_nn = joblib.load(PIP_NN_SAVE_PATH) 

            # evaluate loaded model 
            evaluate_model_single_split(pip_nn, train_features, test_features, 
                train_labels, test_labels, PIP_TEST_SET_SIZE)
            evaluate_model_k_fold_cross_validation(pip_nn, features, labels, 
                PIP_K_SPLITS)
        except Exception as e: 
            # print error information
            print('An error occurred when loading/evaluating existing neural '
                + 'network model for physical disease classification, shown '
                + 'below:')
            print(e)
            traceback.print_exc()
            print('Exiting...')
            return 
    else: 
        # skip
        print('Skipping fitting/loading neural network model for physical ' 
            + 'disease classification...')

# function to extract symptoms 
def extract_symptoms(messages):
    # load model
    se_model = joblib.load(SE_NN_SAVE_PATH)

    # process text 
    if type(messages) != list: 
        messages = [messages]
    messages_df = pd.DataFrame(messages)
    process_text(messages_df)
    text_column = messages_df.columns.values.tolist()[0]
    messages = messages_df[text_column]

    # get feature vectors encoding symptom information 
    feature_vectors = se_model.predict(messages)
    _, unique_symptoms = get_from_file_disease_labels_symptoms()
    feature_vectors = pd.DataFrame(feature_vectors, columns=unique_symptoms)

    # return feature vectors 
    return feature_vectors

# function to make a prediction with a PIP model (0 is random forest, 
# anything else is neural network)
def predict_pip(messages, pip_model_type=DEFAULT_PIP_MODEL_CHOICE): 
    # get feature vectors encoding symptom information 
    feature_vectors = extract_symptoms(messages)

    # load model
    pip_model = None 
    if pip_model_type == 0: 
        pip_model = joblib.load(PIP_RF_SAVE_PATH)
    else: 
        pip_model = joblib.load(PIP_NN_SAVE_PATH)

    # make predictions on feature vectors of symptoms 
    preds = pip_model.predict_proba(feature_vectors)
    for i, row in feature_vectors.iterrows(): 
        if row.sum() == 0: 
            preds[i] = np.zeros(preds[i].shape)

    # return predictions
    return preds 
