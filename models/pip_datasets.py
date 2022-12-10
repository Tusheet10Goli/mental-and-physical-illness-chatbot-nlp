# imports
import itertools
import os
import json 
import pandas as pd 
import numpy as np
import platform


# define constants 
CURR_FILE = os.path.abspath(__file__)
CURR_DIR = CURR_FILE[:CURR_FILE.rfind('/') + 1]
if platform.system() == 'Windows':
    CURR_DIR = CURR_FILE[:CURR_FILE.rfind('\\') + 1]
DATASET_PATH = CURR_DIR + '../datasets/physical_illness/dataset.csv'
LABEL_COLUMN = 'Disease'
PROCESS_DATASET_CSV_SAVE_PATH = (CURR_DIR 
    + 'pip_processed_dataset.csv')
PHYSICAL_DISEASE_PRECAUTIONS_CSV_PATH = (CURR_DIR 
    + '../datasets/physical_illness/symptom_precaution.csv')
EMOTION_TRAIN_PATH = (CURR_DIR 
    + '../datasets/sentiment_analysis/emotions_dataset_for_nlp/train.txt')
EMOTION_TEST_PATH = (CURR_DIR 
    + '../datasets/sentiment_analysis/emotions_dataset_for_nlp/train.txt')
PROCESS_DATASET_JSON_SAVE_PATH = CURR_DIR + 'pip_disease_labels_symptoms.json'
PROCESS_DATASET_JSON_DISEASE_LABELS = 'disease_labels'
PROCESS_DATASET_JSON_UNIQUE_SYMPTOMS = 'unique_symptoms'
MIN_NUM_SYMPTOMS_USER_MESSAGE = 1
MAX_NUM_SYMPTOMS_USER_MESSAGE = 4
USER_MESSAGE_PREFIXES = [
    'I am not feeling well, I don\'t know what is happening.',
    'This is weird, some sickness might be going around at my office.',
    # 'I am in pain and I do not know why. I have', 
    # 'Hey, this hurts. I\'m not used to this. I got'
]
USER_MESSAGE_SUFFIXES = [
    'I am not sure if there is a sickness going around, I hope I can feel better soon.', 
    'Why is this happening? Definitely not used to being in pain like this.', 
    # 'What am I dealing with? Why am I feeling all these symptoms?',
    # 'Do you know what is going on? I hope I am okay and nothing too serious is happening.'
]
SYMPTOM_VERBS = [
    'I am experiencing',
    'I am also feeling',
    'I might be having',
    'I think I am also getting'
]
SYMPTOM_EXTRACTION_DATASET_SAVE_PATH = (CURR_DIR 
    + 'pip_symptom_extraction_dataset.csv')
REVERSE_SYMPTOM_THRESHOLD = 0.4
SUBSAMPLE_PROBS = [1, 1, 0.2, 0.08] # must have length MAX_NUM_SYMPTOMS - MIN_NUM_SYMPTOMS + 1
RNG = np.random.default_rng()
# update paths for Windows 
if platform.system() == 'Windows':
    CURR_FILE = CURR_FILE.replace('/', '\\')
    CURR_DIR = CURR_DIR.replace('/', '\\')
    DATASET_PATH = DATASET_PATH.replace('/', '\\')
    PROCESS_DATASET_CSV_SAVE_PATH = PROCESS_DATASET_CSV_SAVE_PATH.replace('/', '\\')
    PHYSICAL_DISEASE_PRECAUTIONS_CSV_PATH = PHYSICAL_DISEASE_PRECAUTIONS_CSV_PATH.replace('/', '\\')
    EMOTION_TRAIN_PATH = EMOTION_TRAIN_PATH.replace('/', '\\')
    EMOTION_TEST_PATH = EMOTION_TEST_PATH.replace('/', '\\')
    PROCESS_DATASET_JSON_SAVE_PATH = PROCESS_DATASET_JSON_SAVE_PATH.replace('/', '\\')


# function to get disease labels 
def _get_disease_labels(df):
    # get unique diseases, sorted alphabetically 
    unique_diseases = list(set(df[LABEL_COLUMN]))
    for i in range(len(unique_diseases)):
        unique_diseases[i] = unique_diseases[i].strip().lower()
    unique_diseases.sort()

    # assign disease labels 
    label = 0
    disease_labels = dict() 
    for d in unique_diseases: 
        disease_labels[d] = label
        label += 1
    
    # return disease labels 
    return disease_labels

# function to get unique symptoms
def _get_unique_symptoms(df):
    # get unique symptoms, sorted alphabetically
    unique_symptoms = set()
    for _, row in df.iterrows(): 
        for i in range(1, 18):
            if not pd.isna(row[f'Symptom_{i}']): 
                unique_symptoms.add(row[f'Symptom_{i}'].strip().lower())
    unique_symptoms = list(unique_symptoms)
    unique_symptoms.sort() 

    # return unique symptoms 
    return unique_symptoms 

def create_symptom_extraction_dataset(unique_symptoms): 
    # creating symptom extraction dataset 
    print('Creating symptom extraction dataset...')

    # create list of symptoms
    symptoms = []
    reverse_symptoms = []
    for symptom in unique_symptoms: 
        tokenized_symptom = symptom.split('_')
        for i in range(len(tokenized_symptom)):
            tokenized_symptom[i] = tokenized_symptom[i].strip()
        symptoms.append(' '.join(tokenized_symptom))
        tokenized_symptom.reverse()
        reverse_symptoms.append(' '.join(tokenized_symptom))
    
    # write messages and labels to file 
    indices = list(range(len(unique_symptoms)))
    columns = ['text'] + unique_symptoms
    data = []
    for i in range(MIN_NUM_SYMPTOMS_USER_MESSAGE, MAX_NUM_SYMPTOMS_USER_MESSAGE + 1): 
        # consider each permutation of symptoms
        for combination in itertools.combinations(indices, i): 
            # subsample by skipping according to defined probability
            subsample_prob = min(SUBSAMPLE_PROBS)
            if i <= len(SUBSAMPLE_PROBS) - 1: 
                subsample_prob = SUBSAMPLE_PROBS[i]
            if RNG.random() > subsample_prob: 
                continue
            
            # used reversed symptoms based on probability threshold
            symptoms_list = symptoms
            if RNG.random() < REVERSE_SYMPTOM_THRESHOLD: 
                symptoms_list = reverse_symptoms

            # determine extension (listed symptoms)
            extension=''
            if i == 1:  
                extension += f'{symptoms_list[combination[0]]}.'
            else:
                for j in range(i): 
                    if j == i - 1:
                        extension = (extension 
                            + f'and feeling {symptoms_list[combination[j]]}.')
                    else: 
                        extension_prefix = RNG.integers(low=0, 
                            high=len(SYMPTOM_VERBS))
                        extension = (extension + f'{SYMPTOM_VERBS[extension_prefix]} ' 
                            + f'{symptoms_list[combination[j]]}, ')

            # produce labels vector (0 or 1 for each symptom)
            labels = [0] * len(indices)
            for j in range(i): 
                labels[combination[j]] = 1

            # create data point
            for j in range(min(len(USER_MESSAGE_PREFIXES), 
                len(USER_MESSAGE_SUFFIXES))): 
                prefix = USER_MESSAGE_PREFIXES[j]
                suffix = USER_MESSAGE_SUFFIXES[j]
                message = f'{prefix} {extension} {suffix}'
                data.append([message] + labels)
    symptom_extraction_df = pd.DataFrame(data, columns=columns)
    symptom_extraction_df.to_csv(SYMPTOM_EXTRACTION_DATASET_SAVE_PATH, index=False)
    print('Saving feature extraction dataset at ' 
        + f'{SYMPTOM_EXTRACTION_DATASET_SAVE_PATH[len(CURR_DIR):]}')
    
    # return symptom extraction dataset 
    return symptom_extraction_df

# function to create fully numeric representation of phyiscal illness dataset
def process_dataset():
    # process dataset
    print('Processing dataset...')

    # load data 
    df = pd.read_csv(DATASET_PATH) 

    # get disease labels 
    disease_labels = _get_disease_labels(df)

    # get unique symptoms, sorted alphabetically
    unique_symptoms = _get_unique_symptoms(df)

    # create numeric representation of physical illness dataset  
    columns = unique_symptoms + [LABEL_COLUMN]
    data = [] 
    for _, row in df.iterrows():
        # initialize feature vector and label 
        label = [disease_labels[row[LABEL_COLUMN].strip().lower()]]
        feature_vector = []
        
        # check for symptom matches 
        for symptom in unique_symptoms: 
            match = False
            for i in range(1, 18):
                if (not pd.isna(row[f'Symptom_{i}']) and 
                    row[f'Symptom_{i}'].strip().lower() == symptom): 
                    match = True
            if match: 
                feature_vector.append(1)
            else: 
                feature_vector.append(0)

        # add new feature vector and label 
        data.append(feature_vector + label)
    processed_df = pd.DataFrame(data=data, columns=columns)

    # save disease labels, unique symptoms, and processed dataset 
    disease_labels_symptoms = dict() 
    disease_labels_symptoms[
        PROCESS_DATASET_JSON_DISEASE_LABELS] = disease_labels
    disease_labels_symptoms[
        PROCESS_DATASET_JSON_UNIQUE_SYMPTOMS] = unique_symptoms
    with open(PROCESS_DATASET_JSON_SAVE_PATH, 'w') as file: 
        print('Saving disease labels and symptom names at ' 
            + f'{PROCESS_DATASET_JSON_SAVE_PATH[len(CURR_DIR):]}')
        json.dump(disease_labels_symptoms, file, indent=4)
    print('Saving processed dataset at ' 
        + f'{PROCESS_DATASET_CSV_SAVE_PATH[len(CURR_DIR):]}')
    processed_df.to_csv(PROCESS_DATASET_CSV_SAVE_PATH, index=False)

    # create symptom extraction dataset 
    symptom_extraction_df = create_symptom_extraction_dataset(unique_symptoms)

    # return disease labels, unique symptoms, and numeric representation of 
    # physical illness dataset 
    return disease_labels_symptoms, processed_df, symptom_extraction_df 

# function to get disease labels and list of unique symptoms from file
def get_from_file_disease_labels_symptoms():
    # read json file 
    disease_labels = None
    unique_symptoms = None
    with open(PROCESS_DATASET_JSON_SAVE_PATH, 'r') as file: 
        disease_labels_symptoms = json.load(file)
        disease_labels = disease_labels_symptoms[
            PROCESS_DATASET_JSON_DISEASE_LABELS]
        unique_symptoms = disease_labels_symptoms[
            PROCESS_DATASET_JSON_UNIQUE_SYMPTOMS]

    # return disease labels and unique symptoms 
    return disease_labels, unique_symptoms

# function to get disease precautions from file 
def get_from_file_disease_precautions(disease_names): 
    # read CSV file 
    precautions_df = pd.read_csv(PHYSICAL_DISEASE_PRECAUTIONS_CSV_PATH)
    column_names = precautions_df.columns.values.tolist()

    # make sure disease names is a list if not 
    if type(disease_names) != list: 
        disease_names = list(disease_names)

    # find precautions of disease
    symptoms = dict()
    for disease_name in disease_names: 
        for _, row in precautions_df.iterrows(): 
            if (row[column_names[0]].lower().strip() 
                == disease_name.lower().strip()): 
                symptoms_list = [] 
                for i in range(1, 5): 
                    precaution = row[column_names[i]]
                    if pd.isna(precaution):
                        continue
                    symptoms_list.append(precaution)
                symptoms[disease_name.lower().strip()] = symptoms_list

    # return symptoms dictionary 
    return symptoms
