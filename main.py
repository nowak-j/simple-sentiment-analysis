import json
import matplotlib.pyplot as plt
from itertools import islice
import requests
from bs4 import BeautifulSoup
import re
import string
from matplotlib.ticker import MaxNLocator

def main():
    parameters = get_run_parameters()
    negative_words, positive_words, stopwords = load_positive_negative_and_stopwords()
    
    if parameters["compare"] == True:
        results1 = get_text_and_process(parameters, negative_words, positive_words, stopwords)
        results2 = get_text_and_process(parameters, negative_words, positive_words, stopwords)
        comparative_results = calculate_comparative_results(results1, results2)
        visualise_comparative_results(results1, results2, comparative_results)
        if parameters["save_file"] == True:
            all_results = {"file1_results": results1, "file2_results": results2, "comparative_results": comparative_results}
            results_file = open("results_file.json", "w")
            results_file.write(json.dumps(all_results))
            results_file.close()
            save_plots()
    else:
        results = get_text_and_process(parameters, negative_words, positive_words, stopwords)
        visualise_results(results)
        if parameters["save_file"] == True:
            results_file = open("results_file.json", "w")
            results_file.write(json.dumps(results))
            results_file.close()
            save_plots()

    plt.show(block=True)
    input("Press enter to exit. ")

def get_text_and_process(parameters, negative_words, positive_words, stopwords):
    text = get_text(parameters)

    if parameters["filter_by_keywords"] == True:
        text = filter_by_keywords(text)

    text = remove_punctuation(text)
    text = text.lower()

    if parameters["exclude_stopwords"] == True:
        text = exclude_stopwords(stopwords, text) 
    
    results = calculate_results(text, positive_words, negative_words)
    return results

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def filter_by_keywords(text):
    keywords = input("Write your selected keywords and press enter: ").lower().split()
    sentences = split_text_into_sentences(text)
    sentences_with_keywords = []
    for sentence in sentences:
        sentence = sentence.lower()
        for keyword in keywords:
            if keyword in sentence:
                sentences_with_keywords.append(sentence)
                break

    if len(sentences_with_keywords) == 0:
        print("Selected keyword/keywords cannot be found in the given text.")      
        exit()

    text = ' '.join(sentences_with_keywords) 
    return text

def split_text_into_sentences(text):
    pattern = re.compile(r"([A-Z][^\.!?]*[\.!?])", re.M)
    return pattern.findall(text)

def exclude_stopwords(stopwords, text):
    without_stopwords = []
    text = text.split()
    for word in text:
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
            print("The input is incorrect. Write file, url or terminal. ") 

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
        elif user_input == "y":
            return True
        else:
            print("The input is incorrect.")

def get_text_from_url():
    url = input("Input url: ")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    paragraphs = soup.find_all("p")
    only_paragraphs = []
    for paragraph in paragraphs:
        processed = paragraph.get_text()
        processed = processed.strip()
        if len(processed) > 1:
            only_paragraphs.append(processed)

    text = ' '.join(only_paragraphs)
    return text

def load_positive_negative_and_stopwords():
    positive_words_file = open("positive.txt", "r")
    positive_words = positive_words_file.read().split("\n")
    positive_words_file.close()
    negative_words_file = open("negative.txt", "r")
    negative_words = negative_words_file.read().split("\n")
    negative_words_file.close()
    stopwords_file = open("stopwords.txt", "r")
    stopwords = stopwords_file.read().split("\n")
    stopwords_file.close()
    return negative_words, positive_words, stopwords

def calculate_results(text, positive_words, negative_words):
    result = 0
    counter_positive = 0
    counter_negative = 0
    positive_dict = {}
    negative_dict = {}
    text = text.split()
    number_of_words = len(text)

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
      
    if result > 0:
        sentiment = "positive"
    elif result == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"

    positive_dict = dict(sorted(positive_dict.items(), key = lambda item: item[1], reverse=True))
    negative_dict = dict(sorted(negative_dict.items(), key = lambda item: item[1], reverse=True))

    positive_words_percentage = (counter_positive/number_of_words)*100
    negative_words_percentage = (counter_negative/number_of_words)*100

    results = {"sentiment": sentiment, "sentiment_count": result, "number_of_all_words": number_of_words, "number_of_positive_words": 
    counter_positive, "number_of_negative_words": counter_negative, "positive_words_counts": positive_dict, "negative_words_counts": 
    negative_dict, "positive_words_percentage": positive_words_percentage, "negative_words_percentage": negative_words_percentage}
    return results
    # zaokrąglić percentage?

def visualise_results(results):
    if results["sentiment"] == "positive":
        print("The opinion is positive.")
    elif results["sentiment"] == "neutral":
        print("The opinion is neutral.")
    elif results["sentiment"] == "negative":
        print("The opinion is negative.")

    print("The first ten most frequent positive words and the number of their occurrences: ", take(10, results["positive_words_counts"].items()))
    print("The first ten most frequent negative words and the number of their occurrences: ", take(10, results["negative_words_counts"].items()))
    print(f"The percentage of positive words is: {results['positive_words_percentage']:.2f}%")
    print(f"The percentage of negative words is: {results['negative_words_percentage']:.2f}%")   
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    draw_positive_negative_words_counts_plot(ax, results["number_of_positive_words"], results["number_of_negative_words"])
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    draw_most_frequent_words_plot(ax, take_and_form_dict(10, results["positive_words_counts"]), "The most frequent positive words")
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    draw_most_frequent_words_plot(ax, take_and_form_dict(10, results["negative_words_counts"]), "The most frequent negative words")
  
def draw_positive_negative_words_counts_plot(ax, counter_positive, counter_negative): 
    x = ["positive words", "negative words"]
    y = [counter_positive, counter_negative]
    ax.bar(x,y, color=("b","g"))
    ax.set_title("Number of positive and negative words")
    ax.set_xlabel("Type of word")
    ax.set_ylabel("Occurrences")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True)

def draw_most_frequent_words_plot(ax, words_count_dict, title):
    x = words_count_dict.keys()
    y = words_count_dict.values()
    ax.bar(x, y)
    ax.set_title(title)
    ax.set_xlabel("Words")
    ax.tick_params(axis="x", labelrotation=90)
    ax.set_ylabel("Frequency")
    ax.grid(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def calculate_comparative_results(result1, result2):
    results = {}
    results["sentiment_count_difference"] = result1["sentiment_count"] - result2["sentiment_count"]
    results["positive_words_percentage_difference"] = result1["positive_words_percentage"] - result2["positive_words_percentage"]
    results["negative_words_percentage_difference"] = result1["negative_words_percentage"] - result2["negative_words_percentage"]
    return results

def visualise_comparative_results(results1, results2, comparative_results):
    print("The analysis for the first text given:")
    print("The first ten most frequent positive words and the number of their occurrences: ", take(10, results1["positive_words_counts"].items()))
    print("The first ten most frequent negative words and the number of their occurrences: ", take(10, results1["negative_words_counts"].items()))
    print(f"The percentage of positive words is: {results1['positive_words_percentage']:.2f}%")
    print(f"The percentage of negative words is: {results1['negative_words_percentage']:.2f}%")

    print("The analysis for the second text given:")
    print("The first ten most frequent positive words and the number of their occurrences: ", take(10, results2["positive_words_counts"].items()))
    print("The first ten most frequent negative words and the number of their occurrences: ", take(10, results2["negative_words_counts"].items()))
    print(f"The percentage of positive words is: {results2['positive_words_percentage']:.2f}%")
    print(f"The percentage of negative words is: {results2['negative_words_percentage']:.2f}%") 

    print("The results of the comparative analysis:")
    print("The difference in sentiment is: ", comparative_results["sentiment_count_difference"])
    print(f"The difference in positive words percentage is: {comparative_results['positive_words_percentage_difference']:.2f}%")
    print(f"The difference in negative words percentage is: {comparative_results['negative_words_percentage_difference']:.2f}%")
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_tight_layout(True)
    draw_positive_negative_words_counts_plot(ax1, results1["number_of_positive_words"], results1["number_of_negative_words"])
    draw_positive_negative_words_counts_plot(ax2, results2["number_of_positive_words"], results2["number_of_negative_words"])
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_tight_layout(True)
    draw_most_frequent_words_plot(ax1, take_and_form_dict(10, results1["positive_words_counts"]), "The most frequent positive words (text 1)")
    draw_most_frequent_words_plot(ax2, take_and_form_dict(10, results2["positive_words_counts"]), "The most frequent positive words (text 2)")
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_tight_layout(True)
    draw_most_frequent_words_plot(ax1, take_and_form_dict(10, results1["negative_words_counts"]), "The most frequent negative words (text 1)")
    draw_most_frequent_words_plot(ax2, take_and_form_dict(10, results2["negative_words_counts"]), "The most frequent negative words (text 2)")

def take_and_form_dict(n, dict):
    new_dict = {}
    for key in list(dict.keys())[:n]:
        new_dict[key] = dict[key]
    return new_dict

def save_plots():
    plt.figure(1)
    plt.savefig("positive_negative_words.jpg")
    plt.figure(2)
    plt.savefig("most_frequent_positive_words.jpg")
    plt.figure(3)
    plt.savefig("most_frequent_negative_words.jpg")

if __name__ == "__main__":
    main()