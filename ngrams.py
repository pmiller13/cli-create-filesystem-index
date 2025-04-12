def calculate_ngrams(text: str, n: int) -> list[str]:
    """Calculates all n-grams of length n from the input text."""
    if len(text) < n:
        return []
    return [text[i : i + n] for i in range(len(text) - n + 1)]


def generate_ngram_range(text: str, n_min: int, n_max: int) -> list[str]:
    """Generates n-grams for a range of n values [n_min, n_max]."""
    if n_min > n_max:
        raise ValueError("n_min cannot be greater than n_max")

    results = []
    for n in range(n_min, n_max + 1):
        results.extend(calculate_ngrams(text, n))
    return results
