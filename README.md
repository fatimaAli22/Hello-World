# ChatBot Support

## Requirements

Install these dependencies:
`pip install tqdm beautifulsoup4 requests spacy python-telegram-bot`

Register your application to get the API key:
https://stackapps.com/apps/oauth/register

## SpaCy NER Model Training

1. The `base_config.cfg` is used to generate the `config.cfg` file which we will be using to train our model.
   - To generate `config.cfg` run: `python -m spacy init fill-config ./config/base_config.cfg ./config/config.cfg`
2. Anotate the training data using this website [ner-annotator](https://tecoholic.github.io/ner-annotator/)
3. Create `.spacy` training files from the anotated json data by using `preprocess.py`.
   - Make sure to use the anotated data for both train and dev.
   - The json folder should have `train.json` & `dev.spacy` available.
4. Run `python -m spacy train ./config/config.cfg --output ./output` to train  model.
5. To use the new model with SpaCy in your application, you add the path of model:
   - `nlp = spacy.load("./output/model-last")`
