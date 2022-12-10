import argparse 
import numpy as np
from pip_datasets import (get_from_file_disease_labels_symptoms,
    get_from_file_disease_precautions)
from pip_models import DEFAULT_PIP_MODEL_CHOICE, fit_models, predict_pip
import time 


# declare constants 
NUM_PIP_PREDS = 3
NUM_DECIMAL_PLACES = 1


# function for building response to pass back to the user 
# model choice is 0 for random forest, anything else for neural network
def build_pip_response(user_messages, model_choice=DEFAULT_PIP_MODEL_CHOICE, 
    num_preds=NUM_PIP_PREDS): 
    # get disease labels
    disease_labels, _ = get_from_file_disease_labels_symptoms()

    # get prediction from PIP model 
    pip_predictions = predict_pip(user_messages, model_choice)

    # get responses for each prediction 
    pip_responses = []
    for pip_prediction in pip_predictions: 
        # check if a physical illness prediction is present 
        if pip_prediction.sum() == 0: 
            pip_responses.append('')
            continue

        # get most likely diseases and probabilities 
        pred_indices = np.argpartition(pip_prediction, 
            -num_preds)[-num_preds:]
        disease_preds = [] 
        for idx in pred_indices: 
            for key in disease_labels.keys(): 
                if disease_labels[key] == idx: 
                    disease_preds.append((pip_prediction[idx], 
                        key))
                    break
        disease_preds.sort()
        disease_preds.reverse()

        # format response, get precautions
        pip_response = f'Your {num_preds} most likely physical illness risks are:\n'
        disease_names = []
        for pred in disease_preds: 
            pip_response += f'{pred[1]} - {round(pred[0] * 100, NUM_DECIMAL_PLACES)}%\n'
            disease_names.append(pred[1])

        # get precautions and add to response 
        pip_response += '\nYour suggested precautions are:\n'
        precautions_dict = get_from_file_disease_precautions(disease_names)
        for disease_name in disease_names: 
            precautions = precautions_dict[disease_name.lower().strip()]
            precaution_extension = disease_name + ' - '
            for i in range(len(precautions)): 
                if len(precautions) == 1: 
                    precaution_extension += f'{precautions[i]}'
                elif i == len(precautions) - 1:
                    precaution_extension += f'and {precautions[i]}'
                else: 
                    precaution_extension += f'{precautions[i]}, '
            pip_response += precaution_extension + '\n'
        
        # store response 
        pip_responses.append(pip_response)
    
    # return responses
    return pip_responses


# run fit_models function if file is run via command line
if __name__=='__main__':
    # process command line arguments 
    parser = argparse.ArgumentParser(description='parses command line '
        + 'arguments for processing/loading datasets and fitting/loading '
        + 'machine learning models for physical illness prediction')
    parser.add_argument(
        '--proc_data', 
        help=('set to 0 to process initial physical diseases dataset from '
            + 'scratch, set to any other integer to use existing processed '
            + 'datasets'), 
        type=int,
        default=0
    )
    parser.add_argument(
        '--fit_se_nn', 
        help=('set to 0 to fit/evaluate multi-output classifier of neural '
            + 'networks for  symptom extraction from scratch, set to 1 to ' 
            + 'load/evaluate existing model, set to any other integer to '
            + 'skip (default value is 2)'), 
        type=int,
        default=2
    )
    parser.add_argument(
        '--fit_pip_rf', 
        help=('set to 0 to fit/evaluate random forest classifier for symptom '
            + 'extraction from scratch, set to 1 to load/evaluate existing ' 
            + 'model, set to any other integer to skip (default value is 2)'),  
        type=int,
        default=2
    )
    parser.add_argument(
        '--fit_pip_nn', 
        help=('set to 0 to fit/evaluate neural network classifier for symptom '
            + 'extraction from scratch, set to 1 to load/evaluate existing ' 
            + 'model, set to any other integer to skip (default value is 2)'), 
        type=int,
        default=2
    )
    args = parser.parse_args()

    # process/load datasets, fit/load machine learning models 
    start = time.time()
    fit_models(
        proc_data=args.proc_data,
        fit_se_nn=args.fit_se_nn, 
        fit_pip_rf=args.fit_pip_rf, 
        fit_pip_nn=args.fit_pip_nn
    )
    end = time.time()
    print(f'Time elapsed: {(end - start) / 60} minutes.')