import fire
import pickle
import pprint
from ngrams import calculate_ngrams

with open("_Users_p_github_decoder.pkl", "rb") as f:
    decoder = pickle.loads(f.read())
with open("_Users_p_github_index.pkl", "rb") as f:
    index = pickle.loads(f.read())

pp = pprint.PrettyPrinter()


def search(query: str):
    ngrams_query = calculate_ngrams(query, 3)
    results = set()
    candidate_results = []
    for ngram in ngrams_query:
        if ngram in index:
            candidate_results.append(index[ngram])
    if len(candidate_results) == 0:
        print("no results")
    results = candidate_results[0]
    result_paths = []
    for i in range(1, len(candidate_results)):
        results.intersection_update(candidate_results[i])
    if len(results) == 0:
        print("no results")
    else:
        pp.pprint(results)
        for res in results:
            pp.pprint(decoder[res])
            result_paths.append(decoder[res])
    matching_files = []
    print(f"Found {len(results)} candidate files. Verifying...")
    for file_path in result_paths:
        try:
            # Read file content again for verification
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
            if query in content: # Direct string search within the candidate file
                matching_files.append(file_path)
        except Exception as e:
            print(f"Error verifying file {file_path}: {e}") # Log error but continue
    if len(matching_files) > 0:
        pp.pprint(f"Found {len(matching_files)} files containing exact matches")
        pp.pprint(matching_files)

# if __name__ == "__main__":
#     fire.Fire(search)
