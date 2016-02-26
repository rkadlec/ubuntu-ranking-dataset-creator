#README -- Ubuntu Dialogue Corpus v2.0

We describe the files for generating the Ubuntu Dialogue Corpus, and the dataset itself.

##UPDATES FROM UBUNTU CORPUS v1.0:

There are several updates and bug fixes that are present in v2.0. The updates are significant enough that results on the two datasets will not be equivalent, and should not be compared. However, models that do well on the first dataset should transfer to the second dataset (with perhaps a new hyperparameter search).

- Separated the train/validation/test sets by time. The training set goes from the beginning (2004) to about April 27, 2012, the  validation set goes from April 27 to August 7, 2012, and the test set goes from August 7 to December 1, 2012. This more closely mimics real life implementation, where you are training a model on past data to predict future data.
- Changed the sampling procedure for the context length in the validation and test sets, from an inverse distribution to a uniform distribution (between 2 and the max context size). This increases the average context length, which we consider desirable since we would like to model long-term dependencies.
- Changed the tokenization and entity replacement procedure. After complaints stating v1 was too aggressive, we've decided to remove these. It is up to each person using the dataset to come up with their own tokenization/ entity replacement scheme. We plan to use the tokenization internally.
- Added differentiation between the end of an utterance (`__eou__`) and end of turn (`__eot__`). In the original dataset, we concatenated all consecutive utterances by the same user in to one utterance, and put `__EOS__` at the end. Here, we also denote where the original utterances were (with `__eou__`). Also, the terminology should now be consistent between the training and test set (instead of both `__EOS__` and `</s>`).
- Fixed a bug that caused the distribution of false responses in the test and validation sets to be different from the true responses. In particular, the number of words in the false responses was shorter on average than for the true responses, which could have been exploited by some models.

##UBUNTU CORPUS GENERATION FILES:

###generate.sh:
####DESCRIPTION:
Script that calls `create_ubuntu_dataset.py`. This is the script you should run in order to download the dataset. The parameters passed to this script will be passed to `create_ubuntu_dataset.py`. Example usage: `./generate.sh -t -s -l`.

###create_ubuntu_dataset.py:
####DESCRIPTION:
Script for generation of train, test and valid datasets from Ubuntu Corpus 1 on 1 dialogs.
The script downloads 1on1 dialogs from internet and then it randomly samples all the datasets with positive and negative examples.
Copyright IBM 2015

####ARGUMENTS:
- `--data_root`: directory where 1on1 dialogs will downloaded and extracted, the data will be downloaded from [cs.mcgill.ca/~jpineau/datasets/ubuntu-corpus-1.0/ubuntu_dialogs.tgz](cs.mcgill.ca/~jpineau/datasets/ubuntu-corpus-1.0/ubuntu_dialogs.tgz) (default = '.')
- `--seed`: seed for random number generator (default = 1234)
- `-o`, `--output`: output file for writing to csv (default = None)
- `-t`, `--tokenize`: tokenize the output (`nltk.word_tokenize`)
- `-s`, `--stem`: stem the output (`nltk.stem.SnowballStemmer`) - applied only when `-t` flag is present
- `-l`, `--lemmatize`: lemmatize the output (`nltk.stem.WorldNetLemmatizer`) - applied only when `-t` flag is present

*Note:* if both `-s` and `-l` are present, the stemmer is applied before the lemmatizer.

####Subparsers:
`train`: train set generator
- `-p`: positive example probability, ie. the ratio of positive examples to total examples in the training set (default = 0.5)
- `-e`, `--examples`: number of training examples to generate. Note that this will generate slightly fewer examples than desired, as there is a 'post-processing' step that filters  (default = 1000000)

`valid`: validation set generator
- `-n`: number of distractor examples for each context (default = 9)

`test`: test set generator
- `-n`: number of distractor examples for each context (default = 9)


###meta folder: trainfiles.csv, valfiles.csv, testfiles.csv:
####DESCRIPTION:
Maps the original dialogue files to the training, validation, and test sets.


##UBUNTU CORPUS FILES (after generating):

###train.csv:
Contains the training set. It is separated into 3 columns: the context of the conversation, the candidate response or 'utterance', and a flag or 'label' (= 0 or 1) denoting whether the response is a 'true response' to the context (flag = 1), or a randomly drawn response from elsewhere in the dataset (flag = 0). This triples format is described in the paper. When generated with the default settings, train.csv is 463Mb, with 1,000,000 lines (ie. examples, which corresponds to 449,071 dialogues) and with a vocabulary size of ~~1,344,621~~. Note that, to generate the full dataset, you should use the `--examples` argument for the `create_ubuntu_dataset.py` file.

###valid.csv:
Contains the validation set. Each row represents a question. Separated into 11 columns: the context, the true response or 'ground truth utterance', and 9 false responses or 'distractors' that were randomly sampled from elsewhere in the dataset. Your model gets a question correct if it selects the ground truth utterance from amongst the 10 possible responses. When generated with the default settings, `valid.csv` is 27Mb, with 19,561 lines and a vocabulary size of 115,688.

###test.csv:
Contains the test set. Formatted in the same way as the validation set. When generated with the default settings, test.csv is 27Mb, with 18,921 lines and a vocabulary size of 115,623.

##BASELINE RESULTS

####Dual Encoder LSTM model:
```
1 in 2:
	recall@1: 0.868730970907
1 in 10:
	recall@1: 0.552213717862 
	recall@2: 0.72099120433, 
	recall@5: 0.924285351827 
```

####Dual Encoder RNN model:
```
1 in 2:
	recall@1: 0.776539210705,
1 in 10:
	recall@1: 0.379139142954, 
	recall@2: 0.560689786585, 
	recall@5: 0.836350355691,
```

####TF-IDF model:
```
1 in 2:
	recall@1:  0.749260042283
1 in 10:
	recall@1:  0.48810782241
	recall@2:  0.587315010571
	recall@5:  0.763054968288
```

##HYPERPARAMETERS USED

Code for the model can be found here (might not be up to date with the new dataset): https://github.com/npow/ubottu

####Dual Encoder LSTM model:
```
act_penalty=500
batch_size=256
conv_attn=False 
corr_penalty=0.0
emb_penalty=0.001
fine_tune_M=True
fine_tune_W=False
forget_gate_bias=2.0
hidden_size=200
is_bidirectional=False
lr=0.001
lr_decay=0.95
max_seqlen=160
n_epochs=100
n_recurrent_layers=1
optimizer='adam'
penalize_activations=False
penalize_emb_drift=False
penalize_emb_norm=False
pv_ndims=100
seed=42
shuffle_batch=False
sort_by_len=False
sqr_norm_lim=1
use_pv=False
xcov_penalty=0.0
```

####Dual Encoder RNN model:
```
act_penalty=500
batch_size=512
conv_attn=False
corr_penalty=0.0
emb_penalty=0.001
fine_tune_M=False
fine_tune_W=False
forget_gate_bias=2.0
hidden_size=100
is_bidirectional=False
lr=0.0001
lr_decay=0.95
max_seqlen=160
n_epochs=100
n_recurrent_layers=1
optimizer='adam'
penalize_activations=False
penalize_emb_drift=False
penalize_emb_norm=False
pv_ndims=100
seed=42
shuffle_batch=False
sort_by_len=False
sqr_norm_lim=1
use_pv=False
xcov_penalty=0.0
```
