# Predicting Manifesto Alignment of Danish Political Parties 🏛️🇩🇰

## Overview

This repository contains code and data for predicting manifesto alignment of Danish political parties based on parliamentary speech using tree-based (XGBoost and Random Forest) models. The repository is organized into three main folders: `nbs`, `data`, and `results` and is part of an exam in the course Data Science, Prediction, & Forecasting (S24) at the MSc Cognitive Science programme at Aarhus University.

## Note on Data Files

Due to the large size of the data files (both for raw and preprocessed), they cannot be uploaded directly to GitHub. As a workaround, should a viewer want to download the data files I prepared, the repository contains `.txt` files in the appropriate folders including links to Google Drive folders where the data can be downloaded for unpacking locally. These links will remain active until September 2024.

As the raw data can be found online (see sources below) only the preprocessed versions and files for modeling are provided in the zip files. For any issues, please feel free to contact me at [au650502@cas.au.dk](mailto:au650502@cas.au.dk).

### Sources for Raw Data
#### Danish Parliamentary Dialogue (ranging 1997-2022)

* ParlaMint 3.0: Erjavec, Tomaž; et al., 2023, Multilingual comparable corpora of parliamentary debates ParlaMint 3.0, CLARIN.SI, ISSN 2820-4042, http://hdl.handle.net/11356/1486.
* Danish Parliament Corpus: Hansen, Dorte Haltrup, 2018, The Danish Parliament Corpus 2009 - 2017, v1, CLARIN-DK-UCPH Centre Repository, http://hdl.handle.net/20.500.12115/8.
* ParlSpeech: Rauh, Christian; Schwalbach, Jan, 2020, "The ParlSpeech V2 data set: Full-text corpora of 6.3 million parliamentary speeches in the key legislative chambers of nine representative democracies", https://doi.org/10.7910/DVN/L4OAKN, Harvard Dataverse, V1

#### Manifestos

Manifestos between 1997-2022 for Danish political parties were downloaded from the Manifesto Project: https://manifesto-project.wzb.eu/information/documents/corpus

## Folder Structure

### 📂 nbs
The `nbs` folder contains all Jupyter notebooks and .py scripts used for preprocessing, modeling, and data exploration:

- **preprocess**
- Preprocessing and cleaning the textual data.
- Feature engineering, adding variables, and calculating manifesto alignment.
  - **make_embeddings**
- Creating embeddings for manifestos and parliamentary dialogue
- **modelling**
- Tuning, training, and testing models using *cycle*-based cross-validation using Rolling Origin.
- Tuning, training, and testing models using *political-quarter*-based cross-validation using Rolling Origin.
- **descriptives_explorations**
  - Correlation and data exploration in R and descriptives and visualizations of the data in python.
  - **figures**
    - Contains figures used in the paper coupled to this repository.

### 📂 data
The `data` folder contains the datasets used in this study. 

- **preprocessed**
  - **clean**
  - Contains cleaned manifesto and parliamentary dialogue data used to make embeddings.
  - **embeddings**
    - Contains BERT embeddings for both manifestos and parliamentary dialogue.
  - **modelling_data**
    - **final**
      - Contains the final dataset (in complete-dates form (rows for missing days too) and incomplete form (no missing values in the target variable)) used in modelling.
- **raw** [not uploaded, but described for context and for clarity, because the code refers to these folders]
  - **added_variables**
    - Contains additional variables from ParlGov [not uploaded]: https://www.parlgov.org/data-info/
  - **manifestos**
    - Contains raw manifesto data files [not uploaded]
  - **parliamentary_dialogue**
    - Contains raw parliamentary dialogue data files [not uploaded]

### 📂 results
The `results` folder contains performance metrics as for tuning validation and test results for the models.

- **fits_RO_cycle**
  - Contains performance metrics from best models selected in *cycle*-based cross-validation.
- **fits_RO_quarter**
  - Contains performance metrics from best models selected in *political quarter*-based cross-validation.
- **tunings_RO_cycle**
  - Contains tuning results for models in *cycle*-based cross-validation.
- **tunings_RO_quarter**
  - Contains tuning results for models in *political quarter*-based cross-validation.

## Contact

For any questions or further assistance, please reach out to [au650502@cas.au.dk](mailto:au650502@cas.au.dk).