import os
import csv
from textblob import TextBlob
import textstat

# Function to calculate FOG Index
def calculate_fog_index(words, sentences):
    complex_word_count = len([w for w in words if textstat.syllable_count(w) > 2])
    avg_words_per_sentence = len(words) / len(sentences)
    fog_index = 0.4 * (avg_words_per_sentence + complex_word_count)
    return fog_index

# Function to perform text analysis and write to the CSV file
def analyze_text(file_name, positive_words, negative_words, stop_words):
    try:
        # Read the text file
        file_path = os.path.join('output', file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Tokenize text using split and split into sentences
        sentences = text.split('.')
        words = text.split()

        # Sentiment analysis using TextBlob
        blob = TextBlob(text)
        sentiment = blob.sentiment
        negative_score = sentiment.polarity  # Negative Score
        polarity_score = sentiment.polarity  # Polarity Score
        subjectivity_score = sentiment.subjectivity  # Subjectivity Score

        # Text statistics using textstat library
        avg_sentence_length = len(sentences)
        percentage_complex_words = len([w for w in words if len(w) > 5]) / len(words)
        fog_index = calculate_fog_index(words, sentences)
        complex_word_count = len([w for w in words if len(w) > 5])
        word_count = len(words)
        avg_words_per_sentence = word_count / avg_sentence_length  # Average Words per Sentence
        syllables_per_word = textstat.syllable_count(text) / word_count
        personal_pronouns = sum(1 for word in words if word.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'])
        avg_word_length = sum(len(word) for word in words) / word_count

        # Extract the URL_ID from the file name
        url_id = os.path.splitext(file_name)[0]

        # Create a dictionary with metrics
        metrics = {
            "URL_ID": url_id,
            "NEGATIVE SCORE": negative_score,
            "POLARITY SCORE": polarity_score,
            "SUBJECTIVITY SCORE": subjectivity_score,
            "AVG SENTENCE LENGTH": avg_sentence_length,
            "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
            "FOG INDEX": fog_index,
            "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
            "COMPLEX WORD COUNT": complex_word_count,
            "WORD COUNT": word_count,
            "SYLLABLE PER WORD": syllables_per_word,
            "PERSONAL PRONOUNS": personal_pronouns,
            "AVG WORD LENGTH": avg_word_length
        }

        # Write the metrics to the CSV file
        with open('output_metrics.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            fieldnames = metrics.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write headers if the file is empty
            if os.stat('output_metrics.csv').st_size == 0:
                writer.writeheader()

            writer.writerow(metrics)

        print(f"Analysis completed for {url_id}")

    except Exception as e:
        print(f"Error analyzing data for {file_name}: {str(e)}")

# Clear existing data in the CSV file
open('output_metrics.csv', 'w').close()

# Load positive and negative words
with open('MasterDictionary/negative-words.txt', 'r', encoding='latin-1') as f:
    negative_words = set(f.read().splitlines())

with open('MasterDictionary/positive-words.txt', 'r', encoding='latin-1') as f:
    positive_words = set(f.read().splitlines())

# Load stop words from multiple files
stop_words = set()
stopwords_files = [
    'StopWords/StopWords_Auditor.txt',
    'StopWords/StopWords_Currencies.txt',
    'StopWords/StopWords_DatesandNumbers.txt',
    'StopWords/StopWords_Generic.txt',
    'StopWords/StopWords_GenericLong.txt',
    'StopWords/StopWords_Geographic.txt',
    'StopWords/StopWords_Names.txt'
]

for file in stopwords_files:
    with open(file, 'r', encoding='latin-1') as f:
        stop_words.update(set(f.read().splitlines()))

# Iterate through the text files in the "output" folder
output_folder = "output"
for file_name in os.listdir(output_folder):
    if file_name.endswith(".txt"):
        analyze_text(file_name, positive_words, negative_words, stop_words)

print("Analysis completed for all files. Data saved in 'output_metrics.csv'.")
