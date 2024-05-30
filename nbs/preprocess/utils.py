
# -- Code for unpacking Danish Parliament Corpus zip files

import os
import zipfile

def unpack_zip_files(directory):
    """ Unpack zipfile into output folder """

    # Directory containing the zip files
    os.chdir(directory)
    
    # List all zip files in the directory
    zip_files = [f for f in os.listdir() if f.endswith('.zip')]
    
    # Loop through the list of zip files
    for zip_file in zip_files:

        # Create a directory name based on the zip file name (without extension)
        output_folder = zip_file.rsplit('.', 1)[0]
        
        # Create the directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Unpack the zip file into the directory
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        
        print(f"Unpacked {zip_file} into {output_folder}")

# Usage: 
# # Specify the directory containing the zip files
# directory_path = '/path/to/files'

# unpack_zip_files(directory_path)

# -- Code for getting all texts in
import os
import pandas as pd

def find_files(directory, pattern):
    """ Recursively finds all files matching the pattern """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if pattern in filename:
                yield os.path.join(root, filename)

def read_and_concatenate(files):
    """ Read each file and concatenate them into one df """
    
    # List to hold dfs
    df_list = []
    
    for file in files:
        
        # Read the file
        temp_df = pd.read_csv(file, sep='\t', on_bad_lines='skip')
                
        df_list.append(temp_df)
    
    # Concatenate all dfs
    final_df = pd.concat(df_list, ignore_index=True)
    return final_df

# # USAGE: 
# # Specify directory containing the unpacked folders
# base_directory = '/path/to/unzipped/folders'

# # Find all files matching the pattern of file names
# files = list(find_files(base_directory, '_helemoedet-memberinfo-subjects.txt'))

# # Read and concatenate the files
# big_dataframe = read_and_concatenate(files)

# # Inspect the first few rows of the concatenated df
# big_dataframe

# -- Code for unwrapping manifestos
import pandas as pd
import os
import re

def read_and_concatenate_manif(files):
    """ Read each file and concatenate them into one df, including source filename, party number, year, and party name. """
    df_list = []
    
    # Mapping of party numbers to party names
    party_dict = {
        '13001': 'Liberal Alliance',
        '13229': 'Enhedslisten',
        '13230': 'Socialistisk Folkeparti',
        '13320': 'Socialdemokratiet',
        '13410': 'Det Radikale Venstre',
        '13420': 'Venstre',
        '13620': 'Konservative Folkeparti',
        '13720': 'Dansk Folkeparti',
        '13110': 'Alternativet',
        '13730': 'Nye Borgerlige'
    }
    
    for file in files:
        # Read the file
        temp_df = pd.read_csv(file, sep=',', on_bad_lines='skip')
        
        # Extract filename from the path
        filename = os.path.basename(file)
        temp_df['Source_File'] = filename
        
        # Extract the first 5 digits and the following four digits after an underscore from the filename
        match = re.search(r'(\d{5})_(\d{4})', filename)
        if match:
            party_number = match.group(1)  # This captures the first occurrence of 5 consecutive digits
            year = match.group(2)          # This captures the four digits after the underscore
        else:
            party_number = None  # In case the pattern isn't found
            year = None         # In case the pattern isn't found
        
        temp_df['Party_Number'] = party_number
        temp_df['Year'] = year
        
        # Map the party number to the party name
        temp_df['Party_Name'] = temp_df['Party_Number'].map(party_dict)
        
        df_list.append(temp_df)
    
    # Concatenate all dfs
    final_df = pd.concat(df_list, ignore_index=True)
    return final_df

# - Functions for making new vars
import pandas as pd

def count_words_sentences(df, text_column):
    """
    Adds word count and sentence count to a df for a specified text column.

    """
    # Calculate word count
    df['word_count'] = df[text_column].apply(lambda x: len(str(x).split()))

    # Calculate sentence count
    df['sentence_count'] = df[text_column].apply(lambda x: str(x).count('.'))

    return df


# - Functions for preparing the data lightly for making BERT embeddings

# -- Updating list of stopwords
import pandas as pd
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Loading Danish stopwords from NLTK
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')

danish_stopwords = stopwords.words('danish') 

def update_stopwords(party_names):
    extended_stopwords = set(danish_stopwords)  # Use a set for faster operations
    for name in party_names:

        # Ensure that we handle possible missing values and type issues
        if pd.notna(name):
            lower = name.lower()
            capitalized = name.capitalize()
            plural = lower + 's'
            plural_cap = capitalized + 's'

            # Add the variations to the set
            extended_stopwords.update([lower, capitalized, plural, plural_cap])
    return extended_stopwords

# -- Preprocessing names
import re
import string
#import spacy
from nltk.tokenize import word_tokenize

def preprocess_names(names):
    cleaned_names = set()
    for name in names:
        # Remove punctuation and numbers, and convert to lowercase
        name = re.sub(r'[\d' + string.punctuation + ']', '', name).lower()
        # Split names into individual units (first and last names)
        parts = name.split()
        cleaned_names.update(parts)
    return cleaned_names

# -- Preprocessing text (utterances / manifestos)

def preprocess_text(text, stopwords, remove_stopwords=True, remove_party_names=True, remove_names_flag=True, names_list=set()):
    # Convert text to lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove punctuation, numbers, names, stopwords
    text = re.sub(r'[\d' + string.punctuation + ']', '', text)

    if remove_names_flag:
        for name in names_list:
            text = re.sub(r'\b{}\b'.format(name), '', text)

    if remove_stopwords:
        tokens = word_tokenize(text, language='danish')
        text = ' '.join([word for word in tokens if word not in stopwords])
    
    # Remove specific party names
    if remove_party_names:
        party_names_etc = [
            'liberal alliance', 'liberal alliances', 
            'radikale venstre', 'radikale venstres', 'radikale', 'radikale b',
            'dansk folkeparti', 'dansk folkepartis', 
            'konservative folkeparti', 'konservative folkepartis', 
            'socialdemokraterne', 'socialdemokraternes', 'socialdemokratiet','socialdemokratiets',
            'socialistisk folkeparti', 'socialistisk folkepartis', 'sf', 'sf`s', 
            'ny alliance', 'ny alliances', 'alliance',
            'ny borgerlige', 'nye borgerlige', 'ny borgerliges', 'nye borgerliges','borgerlige','borgerliges',
            'venstre', 'venstres', 
            'enhedslisten', 'enhedslistens', 
            'alternativet', 'alternativets', 
            'folkepartis','dansk folkeparti','dansk folkepartis',
            'siumut', 'siumuts',
            'inali', 'inalis',
            'inali parti', 'inalis parti',
            'kalaali', 'kalaalis',
            'ordfører', 'ordføreren','ordførerne', 'ministeren', 'ministerens', 'statsministerens', 'statsministeren', 
            'minister', 'formand', 'formanden', 'fru', 'hr', 'tak', 'tusind',

            # More terms for MPs adressing each other
            "statsminister", "minister", "ordfører", "formand", "formanden", "næstformand", "næstformanden", "rådmand", "borgmester", "regionsrådsformand", "parlamentsmedlem", "parlamentariker", "politiker",

            # Politeness markers and misc.
            "tak", "venligst", "tusind", "mange", "takker", "venlig", "hilsen", "kære", "helt sikkert",'og', 'eller', 'men', 'så', 'det', 'der', 
            'en', 'et', 'de', 'den', 'det', 'deres', 'vores', 'jeres', 'min','din'
        ]
        for name in party_names_etc:
            text = re.sub(r'\b{}\b'.format(name), '', text)
    return text