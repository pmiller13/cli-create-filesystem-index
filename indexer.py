import os
import pickle
import collections
import fire

from ngrams import generate_ngram_range


def find_small_files(
    directory: str,
    max_file_size: int,
    supported_extensions: set[str],
    ignore_dirs: set[str],
) -> list[str]:

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    matching_files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        # Modify dirs in place https://docs.python.org/3/library/os.html#os.walk
        dirs[:] = [
            d
            for d in dirs
            if d not in ignore_dirs
            and not os.path.exists(os.path.join(root, d, "pyvenv.cfg"))
        ]

        for filename in files:

            file_path = os.path.join(root, filename)
            try:
                if not os.path.isfile(file_path) or os.path.islink(file_path):
                    continue

                if supported_extensions:
                    _, file_ext = os.path.splitext(filename)
                    if file_ext.lower() not in supported_extensions:
                        continue

                file_size = os.path.getsize(file_path)
                if file_size > max_file_size:
                    continue

                matching_files.append(file_path)

            except OSError as e:
                print(f"Warning: Could not access {file_path}. Error: {e}")
                continue
            except Exception as e:
                print(f"Warning: Error processing path {file_path}. Error: {e}")
                continue

    return matching_files


def generate_index(
    file_paths: list[str],
    n_grams_min: int,
    n_grams_max: int,
) -> dict[str, set[str]]:

    decoder = {}
    index = collections.defaultdict(set)

    for i, file_path in enumerate(file_paths):
        decoder[i] = file_path
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError as e:
            print(f"Warning: Could not read file {file_path}. Error: {e}")
            continue
        except Exception as e:
            print(f"Warning: Unexpected error reading file {file_path}. Error: {e}")
            continue

        ngrams = generate_ngram_range(text, n_grams_min, n_grams_max)
        for ngram in ngrams:
            index[ngram].add(i)

    return decoder, dict(index)


def run_indexer(
    target_directory: str,
    max_file_size_mb: int = 1,
    n_grams_min: int = 4,
    n_grams_max: int = 10,
    supported_extensions: set[str] = {".txt", ".py", ".md", ".json", ".yml", ".yaml"},
):
    """
    Indexes files in a directory based on their content using n-grams.

    Args:
        target_directory: The root directory to search for files.
        max_file_size_mb: Maximum file size in megabytes to consider for indexing.
                          Files larger than this will be skipped. Defaults to 1 MB.
        n_grams_min: The minimum length of n-grams to generate. Defaults to 4.
        n_grams_max: The maximum length of n-grams to generate. Defaults to 10.
        supported_extensions: A set of file extensions to include in the indexing.
                              Only files with these extensions will be processed.
                              Defaults to {".txt", ".py", ".md", ".json", ".yml", ".yaml"}.
    """
    max_file_size_bytes = max_file_size_mb * 1024 * 1024

    default_ignore_dirs = {
        ".git",
        ".svn",
        ".hg",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        ".ruff_cache",
        "venv",
        ".venv",
        "env",
        ".env",
        "virtualenv",
        ".virtualenv",
        "node_modules",
        "bower_components",
        "build",
        "dist",
        "target",
        "out",
        ".next",
        "*.egg-info",
        "site-packages",
        "lib",
        "Lib",
    }
    print(f"Searching for files in: {target_directory}")
    print(f"Max file size: {max_file_size_mb} MiB ({max_file_size_bytes} bytes)")
    print(f"Supported extensions: {supported_extensions or 'All'}")
    print(f"N-gram range: [{n_grams_min}, {n_grams_max}]")

    try:
        small_files = find_small_files(
            target_directory,
            max_file_size_bytes,
            supported_extensions,
            default_ignore_dirs,
        )

        if not small_files:
            print("No files found matching criteria. Exiting.")
            return

        print(f"\nFound {len(small_files)} files to index.")
        print("Generating n-gram index...")
        decoder, index = generate_index(small_files, n_grams_min, n_grams_max)
        print(f"Index generated with {len(index)} unique n-grams.")

        output_decoder_file = f"{target_directory.replace('/', '_')}_decoder.pkl"
        output_index_file = f"{target_directory.replace('/', '_')}_index.pkl"
        print(f"\nSaving decoder to {output_decoder_file}...")
        try:
            with open(output_decoder_file, "wb") as f_out:
                pickle.dump(decoder, f_out)
            print("Index saved successfully.")
        except (OSError, pickle.PicklingError) as e:
            print(f"Error saving index file: {e}")
            raise
        print(f"\nSaving index to {output_index_file}...")
        try:
            with open(output_index_file, "wb") as f_out:
                pickle.dump(index, f_out)
            print("Index saved successfully.")
        except (OSError, pickle.PicklingError) as e:
            print(f"Error saving index file: {e}")
            raise

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    fire.Fire(run_indexer)
