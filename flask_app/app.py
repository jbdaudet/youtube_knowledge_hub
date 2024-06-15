from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from urllib.parse import urlparse, parse_qs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

app = Flask(__name__)

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_text = ' '.join(word.lower() for word in words if word.isalpha() and word.lower() not in stop_words)
    return filtered_text

def get_embed_url(video_url, start_time):
    query = urlparse(video_url).query
    video_id = parse_qs(query).get('v')
    if video_id:
        video_id = video_id[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?start={int(float(start_time))}"
        return embed_url
    return None

def get_base_video_url(video_url):
    base_url = video_url.split('start=')[0]
    return base_url

def search_query(query_str):
    ix = open_dir("indexdir")
    results_list = []
    processed_query = preprocess_text(query_str)
    
    with ix.searcher() as searcher:
        query = QueryParser("text", ix.schema).parse(processed_query)
        results = searcher.search(query, limit=None)
        
        for result in results:
            embed_url = get_embed_url(result['video_url'], result['start_time'])
            if embed_url:
                results_list.append({
                    'start_time': float(result['start_time']),
                    'text': result['text'],
                    'video_url': embed_url,
                    'summary': result['summary']
                })

    # Sort results by video URL and start time
    results_list.sort(key=lambda x: (get_base_video_url(x['video_url']), x['start_time']))

    # Filter to include only the first result from each video
    filtered_results = []
    included_videos = set()

    for result in results_list:
        base_video_url = get_base_video_url(result['video_url'])
        if base_video_url not in included_videos:
            filtered_results.append(result)
            included_videos.add(base_video_url)

    return filtered_results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_str = request.form['query']
        results = search_query(query_str)
        return render_template('index.html', query=query_str, results=results)
    return render_template('index.html', query='', results=[])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
