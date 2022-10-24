import re
import string
import numpy as np
import pandas as pd
from collections import Counter

def process_data(file_name):
    words = []
    with open(file_name, "r") as f:
        data = f.read()
        data_lower = data.lower()
        words = re.findall(r"\w+", data_lower)
    return words

def process_freq(file_name):
    freqs = []
    with open(file_name, "r") as f:
        data = f.read()
        freqs = list(map(int, re.findall(r"\w+", data)))
    return freqs

def save_vocab():
    word_l = process_data("words.txt")
    vocab = set(word_l)
    print(f"The first 10 words in the text are : \n{word_l[0:10]}")
    print(f"There are {len(vocab)} words in the vocabulary.\n")
    return word_l

def get_count(word_l, word, freq):
    word_count_dict = {}
    for i in range(len(word_l)):
        word_count_dict[word_l[i]] = freq[i]
    # word_count_dict = Counter(word_l)
    # print(f"There are {len(word_count_dict)} key values pairs")
    # print(f"The count for the word {word} is {word_count_dict.get(word, 0)}")
    return word_count_dict

# fix this function calculations
def get_probabilities(word_count_dict, word, freq):
    probabilities = {}
    total = sum(word_count_dict.values())
    for i in word_count_dict:
        probabilities[i] = word_count_dict[i] / total
    # print(f"Length of probabilities is {len(probabilities)}")
    # print(f"P(\"{word}\") is {probabilities[word]:.4f}\n")
    return probabilities

def delete_letter(word, verbose=False):
    delete_l = []
    delete_l = [word[0:i] + word[i+1 : len(word)] for i in range(len(word))]
    if verbose:
        print(f"input word = {word}, delete_l = {delete_l}\n")
    return delete_l

def switch_letter(word, verbose=False):
    switch_l = []
    word1 = list(word)
    for i in range(len(word1)-1):
        a1 = list(word1)
        a1[i], a1[i+1] = a1[i+1], a1[i]
        b = "".join(a1)
        switch_l.append(b)
    if word in switch_l:
        switch_l.remove(word)
    if verbose:
        print(f"Input word = {word}, switch_l = {switch_l}\n")
    return switch_l

def replace_letter(word, verbose=False):
    replace_l = []
    replace_set = []
    lower = string.ascii_lowercase
    for i in range(len(word)):
        temp = [word[0:i] + j + word[i+1:len(word)] for j in lower]
        temp.remove(word)
        replace_set.extend(temp)
    replace_l = sorted(list(replace_set))
    if verbose:
        print(f"Input word = {word}, replace_l = {replace_l}\n")
    return replace_l

def insert_letter(word, verbose=False):
    insert_l = []
    lower = string.ascii_lowercase
    for i in range(len(word)+1):
        temp = [word[0:i] + j + word[i:len(word)] for j in lower]
        insert_l.extend(temp)
    if verbose:
        print(f"Input word = {word}, insert_l = {insert_l}")
        print(f"len(insert_l) = {len(insert_l)}\n")
    return insert_l

def edit_1_letter(word):
    edit_1_set = set(delete_letter(word) + insert_letter(word) + replace_letter(word) + switch_letter(word))
    return edit_1_set

def edit_2_letters(word, allow_switches=True):
    edit_2_set = set()
    insert_letter1 = []
    replace_letter1 = []
    switch_letter1 = []
    delete_letter1 = []
    l = list(edit_1_letter(word))
    temp = []
    for i in l:
        temp = delete_letter(i)
        delete_letter1.extend(temp)
    for i in l:
        temp = replace_letter(i)
        replace_letter1.extend(temp)
    for i in l:
        temp = switch_letter(i)
        switch_letter1.extend(temp)
    for i in l:
        temp = insert_letter(i)
        insert_letter1.extend(temp)
    edit_2_set = set(replace_letter1 + switch_letter1 + delete_letter1 + insert_letter1)
    return edit_2_set

def get_corrections(word, probabilities, vocab, n=2, verbose=True):
    suggestions = []
    n_best = []
    if word in vocab:
        suggestions = word
    elif len(edit_1_letter(word)) != 0:
        suggestions = edit_1_letter(word).intersection(set(vocab))
    elif len(edit_2_letters(word)) != 0:
        suggestions = edit_2_letters(word).intersection(set(vocab))
    else:
        suggestions = word
    best_words = {i:probabilities[i] for i in suggestions if i in probabilities}
    best_words = [(k, v) for k, v in sorted(best_words.items(), key=lambda item: item[1], reverse=True)]
    n_best = best_words[:n]
    if verbose:
        print(f"Enter word : {word}, suggestions = {suggestions}")
    return n_best

def min_edit_distance(source, target, insert_cost=1, delete_cost=1, replace_cost=2):
    a, b, c = 0, 0, 0
    d = []
    len_src = len(source)
    len_target = len(target)
    Dimension = np.zeros((len_src+1, len_target+1), dtype=int)
    for row in range(0, len_src+1):
        Dimension[row, 0] = row
    for col in range(0, len_target+1):
        Dimension[0, col] = col
    for row in range(1, len_src+1):
        for col in range(1, len_target+1):
            r_cost = replace_cost
            if source[row-1] == target[col-1]:
                r_cost = 0
            a = Dimension[row-1, col] + delete_cost
            b = Dimension[row, col-1] + insert_cost
            c = Dimension[row-1, col-1] + r_cost
            d = [a, b, c]
            Dimension[row, col] = min(d)
    minimum_edit_distance = Dimension[len_src, len_target]
    return Dimension, minimum_edit_distance


word = input("Enter word : ")

word_l = save_vocab()
freqs = process_freq("freq.txt")
word_count_dict = get_count(word_l, word, freqs)
probabilities = get_probabilities(word_count_dict, word, freqs)
# edit_1_l = sorted(list(edit_1_letter(word)))
# edit_2_set = sorted(list(edit_2_letters(word)))

corrections = get_corrections(word, probabilities, word_l, 10, True)
for i, word_probs in enumerate(corrections):
    print(f"\nword {i}: {word_probs[0]}, probability = {word_probs[1]:.6f}")
    matrix, min_edit = min_edit_distance(word, word_probs[0])
    print(f"minimum edits = {min_edit}\n")
    idx = list("#" + word)
    cols = list("#" + word_probs[0])
    df = pd.DataFrame(matrix, index=idx, columns=cols)
    print(df)
    print("-"*50)