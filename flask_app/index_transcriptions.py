import os
import pandas as pd
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

import time



# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Ensure the input is a string
    if isinstance(text, float):
        return ""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text, language='english')
    filtered_text = ' '.join(word.lower() for word in words if word.isalpha() and word.lower() not in stop_words)
    return filtered_text

# Define the schema for the index
schema = Schema(start_time=ID(stored=True), text=TEXT(stored=True), video_url=ID(stored=True), summary=TEXT(stored=True))

# Create an index directory
index_dir = "indexdir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

# Create an index
ix = create_in(index_dir, schema)

# Load transcriptions from the CSV file
df = pd.read_csv('data/transcriptions_with_summary.csv', sep=',')

# Index the transcriptions
writer = ix.writer()
for _, row in df.iterrows():
    processed_text = preprocess_text(row['text'])
    writer.add_document(start_time=str(row['start_time']), text=processed_text, video_url=row['video_url'], summary=row['summary'])
writer.commit()

print("Indexing completed.")