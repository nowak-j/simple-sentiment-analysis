import matplotlib.pyplot as plt



# wyświetlić najczęstsze pozytywne/negatywne, procent pozytywnych/negatywnych, 
# inne statystyki poprzedzone wykresami

# dokonanie analizy w oparciu o słowa kluczowe

# menu programu 

# format JSON

# możliwość zapisu wyniku w programie (analiza i wykresy)

# możliwość porównania dwóch tekstów tą samą metodą (powieści)

# możliwość pobierania i analizowania tekstów z sieci


def main():
    text = input("Please enter text in English: ").split()      
    
    positive_words_file = open('positive.txt', 'r')
    positive_words = positive_words_file.read()
    positive_words_file.close()

    negative_words_file = open('negative.txt', 'r')
    negative_words = negative_words_file.read()
    negative_words_file.close()

    stopwords_file = open('stopwords.txt', 'r')
    stopwords = stopwords_file.read()
    stopwords_file.close()

    analyse(text, positive_words, negative_words)

    # możliwość zrobienia ponownej analizy po usunięciu stopwords

    without_stopwords = []

    for word in text:
        if word not in stopwords:
            without_stopwords.append(word)


def analyse(text, positive_words, negative_words):
    result = 0
    for word in text:
        if word in positive_words:
            result += 1
        if word in negative_words:
            result -= 1

    if result > 0:
        print("The opinion is positive")
    elif result == 0:
        print("The opinion is neutral")
    else:
        print("The opinion is negative")




if __name__ == "__main__":
    main()