def search_query(query_str):
    # Open the existing index
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("text", ix.schema).parse(query_str)
        results = searcher.search(query, limit=None)
        return results

# Example usage
if __name__ == "__main__":
    query_str = input("Enter your search query: ")
    results = search_query(query_str)
    for result in results:
        start_time = float(result['start_time'])
        video_url = result['video_url']
        video_link = f"{video_url}&t={int(start_time)}s"
        print(f"Text: {result['text']}\nLink: {video_link}\n")