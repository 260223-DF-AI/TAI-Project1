from collections import Counter, defaultdict
from models import WordFrequency, NGram, DocumentStats, AnalysisResult
from tokenizer import tokenize, get_sentences, get_ngrams, remove_stopwords

class TextAnalyzer:
    """Analyzes text documents for various metrics."""
    
    def __init__(self, text):
        self.text = text
        self.words = tokenize(text)
        self.sentences = get_sentences(text)
        self.word_counter = Counter(self.words)
    
    def get_word_frequencies(self, top_n=20, exclude_stopwords=True):
        """
        Get top N word frequencies.
        Returns: List of WordFrequency namedtuples
        """
        return self.word_counter.most_common(top_n)
    
    def get_bigrams(self, top_n=10):
        """
        Get top N bigrams (2-word phrases).
        Returns: List of NGram namedtuples
        """
        ngrams = Counter(get_ngrams(self.words, 2)).most_common(top_n)
        return [NGram(ngram[0], ngram[1]) for ngram in ngrams]
    
    def get_trigrams(self, top_n=10):
        """
        Get top N trigrams (3-word phrases).
        Returns: List of NGram namedtuples
        """
        ngrams = Counter(get_ngrams(self.words, 3)).most_common(top_n)
        return [NGram(ngram[0], ngram[1]) for ngram in ngrams]
    
    def get_document_stats(self):
        """
        Calculate overall document statistics.
        Returns: DocumentStats namedtuple
        """
        # word count
        numWords = len(self.words)
        # unique words
        numUnique = len(set(self.words))
        # sentence count
        sentCount = len(self.sentences)
        # average word length
        lenWords = [len(word) for word in self.words]
        avgWords = sum(lenWords) / len(lenWords)
        # average sentence length
        lenSent = [len(sent.split(" ")) for sent in self.sentences]
        avgSent = sum(lenSent) / len(lenSent)
        return DocumentStats(numWords, numUnique, sentCount, avgWords, avgSent)

    def get_word_length_distribution(self):
        """
        Group words by length.
        Returns: defaultdict mapping length -> list of words
        """
        distDict = {}
        for element in self.words:
            if len(element) not in distDict:
                distDict[len(element)] = [element]
            else:
                distDict[len(element)] += [element]
        return distDict
    
    def analyze(self):
        """
        Run complete analysis.
        Returns: AnalysisResult namedtuple
        """
        # Document stats
        docStats = self.get_document_stats()
        # top words
        topWords = self.get_word_frequencies()
        # top bi and trigrams
        bigrams = self.get_bigrams()
        trigram = self.get_trigrams()
        # readability score
        words = len(self.words)
        sentences = len(self.sentences)
        lenWords = [len(word) for word in self.words]
        chars = sum(lenWords)
        score = int((4.71 * (chars / words)) + (0.5 * (words/sentences)) - 21.43)
        return AnalysisResult(docStats, topWords, bigrams, trigram, score)