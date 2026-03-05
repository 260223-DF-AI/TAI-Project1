import re
from collections import Counter

# import nltk
# nltk.download("punkt")
# from nltk.tokenize import sent_tokenize

def tokenize(text):
    """
    Split text into words.
    - Convert to lowercase
    - Remove punctuation
    - Remove extra whitespace
    Returns: List of words
    """
    wordList = []
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip()
    wordList = text.split(" ")
    wordList = [word for word in wordList if word != ""]
    return wordList


def get_sentences(text):
    """
    Split text into sentences.
    - Handle abbreviations (Dr., Mr., etc.)
    - Handle multiple punctuation (!! or ...)
    Returns: List of sentences
    """
    #\
    sentenceList = []
    sentenceList = text.split(".")
    # #sentenceList = sent_tokenize(text)
    # abbreviations = r'(Mr|Mrs|Ms|Dr|Prof|Rev|Jr|Sr|St|Mt)'
    # domains = r'(com|org|net|edu|gov|co|io|uk|ca)'
    
    # pattern = r'(?<!Mr)(?<!Mrs)(?<!Ms)(?<!Dr)(?<!Prof)(?<!Rev)(?<!Jr)(?<!Sr)(?<!St)(?<!Mt)\.'

    # #pattern = rf'(?s)(.*?)(?<!\d)(?<!\b{abbreviations})\.(?<!\d)(?<!\.(?:{domains}))[.!?](?:\s+|$)'
    # sentenceList = re.findall(pattern, text)
    
    # return [sentence.strip() for sentence in sentenceList if sentence.strip()]
    return sentenceList


def get_ngrams(words, n):
    """
    Generate n-grams from a list of words.
    Example: get_ngrams(['a', 'b', 'c'], 2) -> [('a', 'b'), ('b', 'c')]
    Returns: List of tuples
    """
    ngramList = []
    for i, word in enumerate(words):
        if i == len(words) - n:
            break
        ngram = []
        for j in range(n):
            ngram.append(words[j + i])
        ngramList.append(tuple(ngram))
        #ngram.clear()
    return ngramList


def remove_stopwords(words, stopwords=None):
    """
    Remove common stopwords from word list.
    Use a default set if stopwords not provided.
    Returns: Filtered list of words
    """
    if stopwords == None:
        stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]    
    
    return [word for word in words if word not in stopwords]
