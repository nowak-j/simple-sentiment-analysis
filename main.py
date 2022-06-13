import ast
import matplotlib.pyplot as plt
from itertools import islice
import numpy as np
from pyrsistent import l
import requests
from bs4 import BeautifulSoup
import re
import string
from matplotlib.ticker import MaxNLocator

figure_number = 0

# TODO błąd usuwa punctuation niektóre dywizy

def main():

    #parameters = get_run_parameters()
    parameters = {'compare': False, 'text_source': 'text', 'exclude_stopwords': True, 'filter_by_keywords': False, 'save_file': False}
    negative_words, positive_words, stopwords = load_positive_negative_and_stopwords()

    # TODO obsługa compare, jeden plot, różnica w wynikach
    # if parameters["compare"] == True:
    #     text_1 = get_text(parameters)
    #     text_2 = get_text(parameters)
    # else:
    #     text = get_text(parameters) 

    text = "The Jagiellon dynasty spanned the late Middle Ages and early Modern Era of Polish history. Beginning with the Lithuanian Grand Duke Jogaila (Władysław II Jagiełło), the Jagiellon evil bad shit wrong furious aggresive nice good strong weak dynasty (1386–1572) formed the Polish–Lithuanian union. The partnership brought vast Lithuania-controlled Rus' areas into Poland's sphere of influence and proved beneficial for the Poles and Lithuanians, who coexisted and cooperated in one of the largest political entities in Europe for the next four centuries. In the Baltic Sea region the struggle of Poland and Lithuania with the Teutonic Knights continued and culminated in the Battle of Grunwald (1410), where a combined Polish-Lithuanian army inflicted a decisive victory against the Teutonic Knights, allowing for territorial expansion of both nations into the far north region of Livonia. In 1466, after the Thirteen Years' War, King Casimir IV Jagiellon gave royal consent to the Peace of Thorn, which created the future Duchy of Prussia, a Polish vassal. The Jagiellon dynasty at one point also established dynastic control over the kingdoms of Bohemia (1471 onwards) and Hungary. In the south, Poland confronted the Ottoman Empire and the Crimean Tatars (by whom they were attacked on 75 separate occasions between 1474 and 1569),and in the east helped Lithuania fight the Grand Duchy of Moscow. Some historians estimate that Crimean Tatar slave-raiding cost Poland-Lithuania one million of its population between the years of 1494 and 1694."
    #text = get_text(parameters) 
    
    if parameters["filter_by_keywords"] == True:
        text = filter_by_keywords(text)

    text = remove_punctuation(text)
    text = text.lower()

    if parameters["exclude_stopwords"] == True:
        text = exclude_stopwords(stopwords, text) 
    
    analyse(text, positive_words, negative_words)
    input("Insert any key to exit.")
    # TODO : save into file
    # TODO format JSON

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def filter_by_keywords(text):
    keywords = input("Write your selected keywords and press enter: ").split()
    sentences = split_text_into_sentences(text)
    sentences_with_keywords = []
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence:
                sentences_with_keywords.append(sentence)
        
    text = ' '.join(sentences_with_keywords) 
    return text

def split_text_into_sentences(text):
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pattern.findall(text)


def exclude_stopwords(stopwords, text):
    without_stopwords = []
    text = text.split()
    for word in text:
        if word == "a":
            None
        if word not in stopwords:
            without_stopwords.append(word)
    without_stopwords = ' '.join(without_stopwords)
    return without_stopwords

def get_run_parameters():
    parameters = {}

    parameters["compare"] = get_true_or_false_input("Do you want to compare two texts?")

    while True:
        user_input =  input("How would like to provide text? Write file, url or terminal: ")
        if user_input == "file":
            parameters["text_source"] = "file"
            break
        elif user_input == "url":
            parameters["text_source"] = "url"
            break
        elif user_input == "terminal":
            parameters["text_source"] = "terminal"
            break
        else:
            print("The input is incorrect. Write file, url or terminal ") 

    parameters["exclude_stopwords"] = get_true_or_false_input("Do you want to conduct analysis after removing stopwords?")
    parameters["filter_by_keywords"] = get_true_or_false_input("Do you want to conduct analysis by selected keywords?")
    parameters["save_file"] = get_true_or_false_input("Do you want to save results to file?")

    return parameters

def get_text(parameters):
    if parameters["text_source"] == "file":
        return get_text_from_file()
    elif parameters["text_source"] == "url":
        return get_text_from_url()
    elif parameters["text_source"] == "terminal":
        return input("Please enter your text: ")

def get_text_from_file():
    file = input("Enter file name with its extension: ")
    input_file = open(file, 'r')
    text = input_file.read()
    input_file.close()
    return text

def get_true_or_false_input(message):
    while True:
        user_input = input(message + " Press y or n: ")
        if user_input == "n":
            return False
            break
        elif user_input == "y":
            return True
            break
        else:
            print("The input is incorrect.")

def get_text_from_url():
    url = input("Input url: ")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    paragraphs = soup.find_all('p')
    only_paragraphs = []
    for paragraph in paragraphs:
        processed = paragraph.get_text()
        processed = processed.strip()
        if len(processed) > 1:
            only_paragraphs.append(processed)

    text = ' '.join(only_paragraphs)
    return text

def load_positive_negative_and_stopwords():
    positive_words_file = open('positive.txt', 'r')
    positive_words = positive_words_file.read().split("\n")
    positive_words_file.close()
    negative_words_file = open('negative.txt', 'r')
    negative_words = negative_words_file.read().split("\n")
    negative_words_file.close()
    stopwords_file = open('stopwords.txt', 'r')
    stopwords = stopwords_file.read().split("\n")
    stopwords_file.close()
    return negative_words, positive_words, stopwords

def analyse(text, positive_words, negative_words):
    result = 0
    counter_positive = 0
    counter_negative = 0
    positive_dict = {}
    negative_dict = {}
    number_of_words = len(text)
    text = text.split()

    for word in text:
        if word in positive_words:
            result += 1
            counter_positive += 1
            if word not in positive_dict:
                positive_dict[word] = 1
            else:
                positive_dict[word] +=1

        if word in negative_words:
            result -= 1
            counter_negative += 1
            if word not in negative_dict:
                negative_dict[word] = 1
            else:
                negative_dict[word] += 1
            
    positive_dict = dict(sorted(positive_dict.items(), key = lambda item: item[1], reverse=True))
    negative_dict = dict(sorted(negative_dict.items(), key = lambda item: item[1], reverse=True))

    if result > 0:
        print("The opinion is positive.")
    elif result == 0:
        print("The opinion is neutral.")
    else:
        print("The opinion is negative.")
    
    print("The first ten most frequent positive words and the number of their occurrences: ", take(10, positive_dict.items()))
    print("The first ten most frequent negative words and the number of their occurrences: ", take(10, negative_dict.items()))
    print("The percentage of positive words is: ", counter_positive/number_of_words)
    print("The percentage of negative words is: ", counter_negative/number_of_words)   
    positive_negative_words_number_plot(counter_positive, counter_negative)
    most_frequent_words_plot(positive_dict, "The most frequent positive words")
    most_frequent_words_plot(negative_dict, "The most frequent negative words")
    
def positive_negative_words_number_plot(counter_positive, counter_negative): 
    x = ['positive words', 'negative words']
    y = [counter_positive, counter_negative]
    global figure_number
    figure_number += 1
    fig, ax = plt.subplots()
    plt.figure(figure_number)
    plt.bar(x,y, color=('b','g'))
    plt.title('Number of positive and negative words', fontsize=16)
    plt.xlabel('Type of word')
    plt.ylabel('Occurrences')
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(True)
    fig.tight_layout()
    plt.show(block=False)

def most_frequent_words_plot(words_count_dict, title):
    x = words_count_dict.keys()
    y = words_count_dict.values()
    global figure_number 
    figure_number += 1
    fig, ax = plt.subplots()
    plt.figure(figure_number)
    plt.bar(x, y)
    plt.title(title, fontsize=16)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.xticks(rotation=90, fontsize=8)
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig.tight_layout()
    plt.show(block=False)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

if __name__ == "__main__":
    main()