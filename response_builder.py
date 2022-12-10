# import modules
import os
import sys 
CURR_FILE = os.path.abspath(__file__)
CURR_DIR = CURR_FILE[:CURR_FILE.rfind('/') + 1]
sys.path.append(CURR_DIR + 'models/')
from physical_illness_prediction import build_pip_response
from pip_models import DEFAULT_PIP_MODEL_CHOICE
from mental_illness_prediction import build_mip_response
from models.physical_illness_prediction import build_pip_response, NUM_PIP_PREDS
from models.pip_models import DEFAULT_PIP_MODEL_CHOICE
import platform 
# updates paths for windows 
if platform.system == 'Windows':
    CURR_FILE = CURR_FILE.replace('/', '\\')
    CURR_DIR = CURR_DIR.replace('/', '\\')

# function for building response to pass back to the user 
# pip model choice is 0 for random forest, anything else for neural network
def build_response(user_messages, pip_model_choice=DEFAULT_PIP_MODEL_CHOICE, num_preds=NUM_PIP_PREDS): 
    # get pip responses 
    pip_responses = build_pip_response(user_messages, pip_model_choice, num_preds)

    # get mip response
    mip_response = build_mip_response(user_messages)
    

    # produce responses
    responses = {
        'pip': pip_responses, 
        'mip': mip_response
    }

    # return responses
    return responses