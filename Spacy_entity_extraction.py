import pandas as pd
df = pd.read_csv('./data_augmented_2.csv')

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df['request'], df[['pages', 'name']], test_size = 0.3, 
                                                   shuffle = True, random_state = 7)

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()
print(y_train[0])

import json

training_data = {'classes' : ['DocName', "NbPages"], 'annotations' : []}
last = 0
annot_error = 0
for i, example in enumerate(X_train):
  temp_dict = {'text': example, 'entities': []}
  dn, np = y_train[i]
  result = example.find(str(dn))
  if result == -1:
    annot_error += 1
    continue
  temp_dict['entities'].append((result, result + len(str(dn)), "NbPages"))
  result = example.find(np.split('.')[0])
  if result == -1:
    annot_error += 1
    continue
  temp_dict['entities'].append((result, result + len(np), "DocName"))
  training_data['annotations'].append(temp_dict)

print(f"Number of annotation erros: {annot_error}")
print(len(training_data['annotations']))
print(training_data['annotations'][5])

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

nlp = spacy.blank("en") # load a new spacy model
doc_bin = DocBin() # create a DocBin object

from spacy.util import filter_spans

span_error = 0

for training_example  in tqdm(training_data['annotations']): 
    text = training_example['text']
    labels = training_example['entities']
    doc = nlp.make_doc(text) 
    ents = []
    for start, end, label in labels:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            span_error += 1
        else:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents 
    doc_bin.add(doc)
print(f"Number of annotation erros: {span_error}")

doc_bin.to_disk("training_data.spacy") # save the docbin object

## To run the training first edit the basic_config.cfg then run this cmd:
## python -m spacy init fill-config base_config.cfg config.cfg
## python -m spacy train config.cfg --output ./ --paths.train ./training_data.spacy --paths.dev ./training_data.spacy --gpu-id 0

