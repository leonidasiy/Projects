import nltk
import sys
import os
import string
from itertools import chain
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict.fromkeys(os.listdir(directory))
    for file in files:
        text_file = open(os.path.join(directory, file), "r")
        files[file] = text_file.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    word_list = nltk.tokenize.word_tokenize(document.lower())
    word_list = [word for word in word_list if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]
    return word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set(chain(*documents.values()))
    word_count = dict.fromkeys(words, 0)
    for word in words:
        for document in documents:
            if word in documents[document]:
                word_count[word] += 1
    word_idfs = {word: math.log(len(documents)/count) for word, count in word_count.items()}
    return word_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_values = {}
    for file in files:
        value_sum = 0
        for word in query:
            value_sum += files[file].count(word) * idfs[word]
        file_values[file] = value_sum
    files_ranked = sorted(file_values, key=lambda file: file_values[file])
    files_to_return = []
    for i in range(n):
        files_to_return.append(files_ranked.pop())
    return files_to_return


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_values = {}
    for sentence in sentences:
        value_sum = 0
        for word in query:
            if word in sentences[sentence]:
                value_sum += idfs[word]
        sentence_values[sentence] = value_sum
    sentences_ranked = sorted(sentence_values, key=lambda sentence: sentence_values[sentence])
    sentences_to_return = []
    for i in range(n):
        max = sentence_values[sentences_ranked[-1]]
        if sentence_values[sentences_ranked[-2]] == max:
            sentence_densities = dict.fromkeys([sentence for sentence in sentences_ranked if sentence_values[sentence] == max])
            for sentence in sentence_densities:
                count = 0
                for word in query:
                    if word in sentence:
                        count += 1
                sentence_densities[sentence] = count/len(sentence)
            sentences_ranked_2 = sorted(sentence_densities, key=lambda sentence: sentence_densities[sentence])
            sentences_to_return.append(sentences_ranked_2.pop())
        else:
            sentences_to_return.append(sentences_ranked.pop())
    return sentences_to_return


if __name__ == "__main__":
    main()
