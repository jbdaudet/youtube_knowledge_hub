Youtube Knowledge Hub:

- scans the videos of a YouTube Channel
- captures the sound & converts the speech to text
- index the text in 30 seconds sections 
- creates a flask webpage to search the youtube channel for a specific topic 
- return the list of videos addressing the subject with the right timestamp, and displays a summary of the 30s section generated with AI. 

1/ src/Youtube_knowledge_base.ipynb to generate the transcription_with_summary.csv file from the Youtube channel videos.
2/ Paste the csv file in flask_app/data/
3/ run in a cmd prompt:
    python index_transcriptions.py to index the contents
    python app.py to run the flask app
