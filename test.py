# imports
from response_builder import build_response
from models.pip_models import extract_symptoms


# define constants 
PIP_TEST_CASES = [
    {
        'message': 'my skin is really itchy, I got rashes and patches all over, what is happening?',
        'symptoms': ['itching', 'skin_rash', 'dischromic _patches'],
        'illness': 'fungal infection'
    },
    {
        'message': 'I am sneezing so much, I have a cough, my throat hurts, and I have a headache. I also think I might be getting a fever.',
        'symptoms': ['continuous_sneezing', 'cough', 'throat_irritation', 'headache', 'mild_fever'],
        'illness': 'common cold'
    },
    {
        'message': 'I keep on sneezing and my eyes are very watery. What am I dealing with?',
        'symptoms': ['continuous_sneezing', 'watering_from_eyes'],
        'illness': 'allergy'
    },
    {
        'message': 'I feel very nauseous, my head is hurting and I am throwing up. I have not felt anything like this before, what is it?', 
        'symptoms': ['nausea', 'headache', 'vomiting'],
        'illness': 'typhoid'
    },
    {
        'message': 'I have a headache and I feel very dizzy. It is hard for me to walk or stand, I can\'t balance well. My chest also hurts a bit too. What do I have?',
        'symptoms': ['headache', 'dizziness', 'loss_of_balance', 'chest_pain'],
        'illness': 'hypertension'
    },
    {
        'message': 'I have rashes and red spots all over my skin, my head hurts and I feel like I might be getting a fever. What is going on?',
        'symptoms': ['skin_rash', 'red_spots_over_body', 'headache', 'mild_fever'],
        'illness': 'chicken pox'
    },
    {
        'message': 'I feel very weak and stiff. I try to move but I can\'t. Like it is painful to walk and lift things. What is happening?',
        'symptoms': ['muscle_weakness', 'movement_stiffness', 'painful_walking'],
        'illness': 'arthritis'
    },
    {
        'message': 'I feel some pain in my bladder, my urine smells weird and I keep feeling like I have to pee... what is going on?',
        'symptoms': ['bladder_discomfort', 'foul_smell_of_urine', 'continuous_feel_of_urine'],
        'illness': 'urinary tract infection'
    }, 
    {
        'message': 'I have these weird blister and sore looking things showing up on my face that are reddish-yellow. What sickness do I have?', 
        'symptoms': ['blister', 'red_sore_around_nose', 'yellow_crust_ooze'],
        'illness': 'impetigo'
    },
    {
        'message': 'I have a lot of pain in my muscles and my joints, my eyes are a bit yellow, and I feel very tired. What is happening?', 
        'symptoms': ['muscle_pain', 'join_pain', 'yellowing_of_eyes', 'nausea'],
        'illness': 'hepatitis a'
    }
]
PIP_NO_SYMPTOM_CASES = [
    {
        'message': 'Hey hey, this is just testing to see that no symptoms are picked up and no PIP response is produced.', 
        'symptoms': [],
        'illness': 'None'
    }, 
    {
        'message': 'A message with no physical illness symptoms at all. No symptoms should be detected and no PIP response should be provided.', 
        'symptoms': [],
        'illness': 'None'
    }, 
    {
        'message': 'This message does not contain any information regarding physical illnesses, so no response should be generated.', 
        'symptoms': [],
        'illness': 'None'
    }, 
    {
        'message': 'Just another test message, no important information here.', 
        'symptoms': [],
        'illness': 'None'
    }
]

MIP_TEST_CASES = [
    {
        'message': 'I hate everything! I have been feeling bad for so long, which does not make sense. I have no idea why I am always sad, what is going on?',
        'illness' : 'depression'
    },
    {
        'message': 'I just don\'t get it, I am so confused about why I am suffering like this. Not sure what to do about all this, I am so nervous about it all. I am really worried and nervous all the time, why do I feel this way?', 
        'illness' : 'anxiety'
    }
]


# function to run tests
def run_pip_tests():
    # run pip tests 
    print('=================================================================')
    print('PHYSICAL ILLNESS PREDICTION (PIP) PIPELINE TEST CASES AND RESULTS')
    print('=================================================================\n')

    # assemble list of test cases 
    test_cases = PIP_TEST_CASES + PIP_NO_SYMPTOM_CASES

    # get messages, ground truth symptoms, and ground truth illnesses 
    messages, ground_truth_symptoms, ground_truth_illnesses = [], [], []
    for test_case in test_cases: 
        messages.append(test_case['message'])
        ground_truth_symptoms.append(test_case['symptoms'])
        ground_truth_illnesses.append(test_case['illness'])

    # get extracted symptoms 
    symptoms = extract_symptoms(messages)
    symptom_names = symptoms.columns.values.tolist()

    # get responses from random forest/neural network PIP models
    rf_responses = build_response(messages, pip_model_choice=0)['pip']
    nn_responses = build_response(messages, pip_model_choice=1)['pip']

    # iterate through each test case and print results 
    rf_count, nn_count = 0, 0
    for i in range(len(test_cases)):
        # print original message 
        print('-----------------------------------------------------------------\n')
        print(f'Provided message: {messages[i]}')

        # print extracted symptoms 
        extracted_symptoms = [] 
        for symptom_name in symptom_names: 
            if symptoms.iloc[i][symptom_name] == 1: 
                extracted_symptoms.append(symptom_name)
        print(f'Extracted symptoms: {extracted_symptoms}')
        print(f'Ground truth symptoms: {ground_truth_symptoms[i]}')
        print(f'Ground truth illness: {ground_truth_illnesses[i]}\n')

        # print response 
        print('Generated response (random forest PIP model): \n'
            + f'{rf_responses[i]}')
        print('Generated response (neural network PIP model): \n'
            + f'{nn_responses[i]}')

        # check if the random forest PIP model responses are correct 
        rf_passed = False
        if (ground_truth_illnesses[i].lower().strip() == 'none'
            and len(rf_responses[i].lower().strip()) == 0):
            # response is empty for no symptoms cases
            rf_count += 1 
            rf_passed = True
        else: 
            rf_predictions = (rf_responses[i].lower().split('\n'))[-4:-1]
            for j in range(len(rf_predictions)): 
                rf_predictions[j] = rf_predictions[j][:rf_predictions[j]
                    .find('-')].strip()
            if ground_truth_illnesses[i].lower().strip() in rf_predictions: 
                # response contains ground truth illness 
                rf_count += 1 
                rf_passed = True
        if rf_passed: 
            print('PASS (random forest PIP model)')
        else: 
            print('FAIL (random forest PIP model)')

        # check if the neural network PIP model responses are correct
        nn_passed = False
        if (ground_truth_illnesses[i].lower().strip() == 'none'
            and len(nn_responses[i].lower().strip()) == 0):
            # response is empty for no symptoms cases
            nn_count += 1 
            nn_passed = True
        else: 
            nn_predictions = (nn_responses[i].lower().split('\n'))[-4:-1]
            for j in range(len(nn_predictions)): 
                nn_predictions[j] = nn_predictions[j][:nn_predictions[j]
                    .find('-')].strip()
            if ground_truth_illnesses[i].lower().strip() in nn_predictions: 
                # response is empty for no symptoms cases
                nn_count += 1 
                nn_passed = True
        if nn_passed: 
            print('PASS (neural network PIP model)')
        else: 
            print('FAIL (neural network PIP model)')
        print('-----------------------------------------------------------------\n')
        
    # print accuracy
    print('Ratio of passed test cases to total test cases (random forest '
        + f'PIP model): {rf_count} / {len(test_cases)}\n')
    print('Ratio of passed test cases to total test cases (neural network '
        + f'PIP model): {nn_count} / {len(test_cases)}\n')
    print('=================================================================\n')

def run_mip_tests():
    # run mip tests 
    print('=================================================================')
    print('MENTAL ILLNESS PREDICTION (MIP) PIPELINE TEST CASES AND RESULTS')
    print('=================================================================\n')

    # assemble list of test cases 
    test_cases = MIP_TEST_CASES

    # get messages, ground truth symptoms, and ground truth illnesses 
    messages, ground_truth_illnesses = [], []
    for test_case in test_cases: 
        messages.append(test_case['message'])
        ground_truth_illnesses.append(test_case['illness'])

    lr_responses = build_response(messages, pip_model_choice=0)['mip']

    # iterate through each test case and print results
    lr_count = 0 
    for i in range(len(test_cases)):
        # print original message 
        print('-----------------------------------------------------------------\n')
        print(f'Provided message: {messages[i]}')

        # print ground truth illness 
        print(f'Ground truth illness: {ground_truth_illnesses[i]}\n')

        # print response 
        print('Generated response (Logistic Regression MIP model): \n'
            + f'{lr_responses[i]}\n')

        # check if the responses are correct 
        if ground_truth_illnesses[i].lower().strip() in lr_responses[i].lower().strip(): 
            print('PASS (Logistic Regression MIP model)')
            lr_count += 1
        else: 
            print('FAIL (Logistic Regression MIP model)')
        
        print('-----------------------------------------------------------------\n')
        
    # print accuracy
    print('Ratio of passed test cases to total test cases (Logistic Regression '
        + f'MIP model): {lr_count} / {len(test_cases)}\n')
    print('=================================================================\n')


# make predictions when run as script 
if __name__=='__main__':
    run_pip_tests()
    run_mip_tests()