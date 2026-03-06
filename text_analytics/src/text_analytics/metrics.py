from analyzer import TextAnalyzer
from math import sqrt

def flesch_reading_ease(word_count, sentence_count, syllable_count):
    """
    Calculate Flesch Reading Ease score.
    Formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
    
    Score interpretation:
    - 90-100: Very easy (5th grade)
    - 60-70: Standard (8th-9th grade)
    - 30-50: Difficult (college)
    - 0-30: Very difficult (college graduate)
    """
    frc = round((206.835 - 1.015 * (word_count/sentence_count) - 84.6 * (syllable_count/word_count)),2)
    if frc > 100:
        return 100
    return frc

def count_syllables(word):
    """
    Count syllables in a word.
    Simple heuristic: count vowel groups.
    """
    count = 0
    prev = word.lower()[0]
    for i, ch in enumerate(word.lower()): # I'm pretty sure it is already lower, but just for safety
        if ch in 'aeiou':
            if((i == len(word) - 1 and ch == 'e') or (ch == prev)):
                continue
            count += 1
            prev = ch
    return count

def calculate_readability(analyzer):
    """
    Calculate readability metrics for an analyzed document.
    Returns: Dict with various readability scores
    """
    tAnalyzer = TextAnalyzer("We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America.")
    results = tAnalyzer.analyze()
    syllableCounts = [count_syllables(word) for word in tAnalyzer.text]
    syllables = sum(syllableCounts)

    # flesch reading score
    fre = flesch_reading_ease(len(tAnalyzer.words), len(tAnalyzer.sentences), syllables)

    # SMOG Readability Score = 1.043 × sqrt(Polysyllabic Words)​ + 3.1291
    # num > 3 syllable words per 30 sentences
    multiSyllabicWords = [syllables for syllables in syllableCounts if syllables >= 3]
    numMultiSyllabicWords = len(multiSyllabicWords) * 30 / len(tAnalyzer.sentences)
    smogScore = round((1.043 * sqrt(numMultiSyllabicWords) + 3.1291),2)
    return {
        'automated_readability_score': results.readability_score,
        'flesch_reading_score': fre,
        'smog_index_score': smogScore
    }

print(calculate_readability(TextAnalyzer("We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America.")))