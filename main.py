import matplotlib.pyplot as plt

# sprawdzić język?
text = input("Please enter text in English: ").split()      

# jakoś słowa pozytywne i negatywne pobrać 
positive = open('positive.txt', 'r')
positive_words = positive.read()
positive.close()

negative = open('negative.txt', 'r')
negative_words = negative.read()
negative.close()

stopwords = open('stopwords.txt', 'r')
stopwords_lines = stopwords.read()
stopwords.close()

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


# możliwość zrobienia ponownej analizy po usunięciu stopwords

without_stopwords = []

for word in text:
    if word not in stopwords_lines:
        without_stopwords.append(word)

# wyświetlić najczęstsze pozytywne/negatywne, procent pozytywnych/negatywnych, 
# inne statystyki poprzedzone wykresami

# dokonanie analizy w oparciu o słowa kluczowe

# menu programu 

# format JSON

# możliwość zapisu wyniku w programie (analiza i wykresy)

# możliwość porównania dwóch tekstów tą samą metodą (powieści)

# możliwość pobierania i analizowania tekstów z sieci

# repozytorium na github