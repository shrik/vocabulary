import nltk
import collections
import re
from nltk.corpus import wordnet as wn


# TODO
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


def filter_known(words_counter):
    know_words = get_words_from_file("dicts/known.txt")
    words_counter = filter_words(words_counter, know_words)
    return words_counter

def filter_skip(words_counter):
    words1 = get_words_from_file("dicts/skip.txt")
    words2 = get_words_from_file("dicts/skip/top_3000_common.txt")
    words3 = get_words_from_file("dicts/skip/mayuchao_mastered.txt")
    words = words1 + words2 + words3
    words_counter = filter_words(words_counter, words)
    return words_counter


def filter_words(words_counter, words):
    keys = set(list(words_counter.keys()))
    for word in words:
        if word in keys:
            words_counter.pop(word)
    return words_counter

def word_stem(word):
    # TODO Log these words
    word_synsets = wn.synsets(word)
    if len(word_synsets) == 0:
        return "."
    lemmas = word_synsets[0].lemma_names()
    if len(lemmas) == 0:
        return "."
    return lemmas[0]

def analysis(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [word_stem(token) for token in tokens]
    words_counter = collections.Counter(tokens)
    words_counter = filter_known(words_counter)
    words_counter = filter_skip(words_counter)
    words_counter = filter_not_words(words_counter)
    res = {k: v for k, v in sorted(words_counter.items(), key=lambda item: -item[1])}
    return res

def filter_not_words(words_counter):
    invalid = []
    for key in words_counter.keys():
        if not is_valid_word(key):
            invalid.append(key)
    [words_counter.pop(key) for key in invalid]
    return words_counter

def is_valid_word(word):
    only_alphabet = re.match("^[a-z]+$", word)
    not_short = (len(word) > 3)
    return only_alphabet and not_short



def get_words_from_file(filepath):
    lines = open(filepath, "r").readlines()
    return [line.strip() for line in lines]

def pp(words_counter):
    print("total words: ", len(words_counter.keys()))
    for key, value in words_counter.items():
        print(f"{key}\t{value}")

def read_from_file(filepath):
    return open(filepath, "r").read()

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    text = read_from_file(options.filename)
    words_counter = analysis(text)
    pp(words_counter)