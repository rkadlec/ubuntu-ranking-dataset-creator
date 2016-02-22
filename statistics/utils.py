import unicodecsv
import matplotlib.pyplot as plt
import numpy
from collections import defaultdict
from scipy.stats import chisquare, ttest_ind


def n_utterances_counts(f_name, eou='__eou__'):
    n_utterances = []
    reader = unicodecsv.reader(open(f_name))
    next(reader)    # skip header
    for line in reader:
        n_utterances.append(line[0].count(eou))
    return n_utterances


def train_stats(f_name, eou='__eou__', eot='__eot__'):
    pos_utterances = []
    pos_turns = []
    pos_words = []
    neg_utterances = []
    neg_turns = []
    neg_words = []

    reader = unicodecsv.reader(open(f_name))
    next(reader)    # skip header
    for line in reader:
        if int(float(line[2])) == 1:
            pos_utterances.append(line[0].count(eou))
            pos_turns.append(line[0].count(eot))
            pos_words.append(len(line[0].split()))
        elif int(float(line[2])) == 0:
            neg_utterances.append(line[0].count(eou))
            neg_turns.append(line[0].count(eot))
            neg_words.append(len(line[0].split()))
        else:
            print line[2]

    return pos_utterances, pos_turns, pos_words, neg_utterances, neg_turns, neg_words


def normalize(data):
    total = float(sum(data))
    return data/total


def distribution(data, max_utt):
    counts = defaultdict(int)
    for d in data:
        counts[d] += 1

    total = float(len(data))
    distr = numpy.zeros(max_utt)

    for key, val in counts.iteritems():
        distr[key] = val

    return distr, normalize(distr)


def plot_histogram(data, title, x_label, y_label, **kwargs):
    n, bins, patches = plt.hist(data, 500, facecolor='green', alpha=0.75, **kwargs)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)

    plt.show()


if __name__ == "__main__":

    # load lists of number of utterances
    train_n_uterrances = n_utterances_counts("/home/petrbel/ubuntu-ranking-dataset-creator/src/train.csv")
    test_n_uterrances = n_utterances_counts("/home/petrbel/ubuntu-ranking-dataset-creator/src/test.csv")
    valid_n_uterrances = n_utterances_counts("/home/petrbel/ubuntu-ranking-dataset-creator/src/valid.csv")

    max_utt = max(max(train_n_uterrances), max(test_n_uterrances), max(valid_n_uterrances)) + 1

    # train distribution
    train_counts, train_distr = distribution(train_n_uterrances, max_utt=max_utt)

    # test
    expected_test_counts = train_distr * len(test_n_uterrances)
    real_test_counts, test_distr = distribution(test_n_uterrances, max_utt=max_utt)
    _, pvalue = chisquare(real_test_counts+1, expected_test_counts+1)
    print("TestDataset: ChiSq pvalue={}".format(pvalue))

    # valid
    expected_valid_counts = train_distr * len(valid_n_uterrances)
    real_valid_counts, valid_distr = distribution(valid_n_uterrances, max_utt=max_utt)
    _, pvalue = chisquare(real_valid_counts+1, expected_valid_counts+1)
    print("ValidDataset: ChiSq pvalue={}".format(pvalue))

    # histograms
    plot_histogram(train_n_uterrances, "Train Utterances", "Number of utterances", "Count")
    plot_histogram(test_n_uterrances, "Test Utterances", "Number of utterances", "Count")
    plot_histogram(valid_n_uterrances, "Valid Utterances", "Number of utterances", "Count")

    # train stats
    print("Train Min: {}".format(min(train_n_uterrances)))
    print("Train Max: {}".format(max(train_n_uterrances)))
    print("Train Mean: {}".format(numpy.mean(train_n_uterrances)))
    print("Train Std: {}".format(numpy.std(train_n_uterrances)))

    # test stats
    print("Test Min: {}".format(min(test_n_uterrances)))
    print("Test Max: {}".format(max(test_n_uterrances)))
    print("Test Mean: {}".format(numpy.mean(test_n_uterrances)))
    print("Test Std: {}".format(numpy.std(test_n_uterrances)))

    # valid stats
    print("Valid Min: {}".format(min(valid_n_uterrances)))
    print("Valid Max: {}".format(max(valid_n_uterrances)))
    print("Valid Mean: {}".format(numpy.mean(valid_n_uterrances)))
    print("Valid Std: {}".format(numpy.std(valid_n_uterrances)))

    # ttest of means
    pvalue = ttest_ind(train_n_uterrances, test_n_uterrances, equal_var=False)
    print("ttest: train-test, pvalue={}".format(pvalue))
    pvalue = ttest_ind(train_n_uterrances, valid_n_uterrances, equal_var=False)
    print("ttest: train-valid, pvalue={}".format(pvalue))

    pos_utterances, pos_turns, pos_words, neg_utterances, neg_turns, neg_words = train_stats("/home/petrbel/ubuntu-ranking-dataset-creator/src/train.csv")