# cli-create-filesystem-index

Example usage
```
python indexer.py --help

NAME
    indexer.py - Indexes files in a directory based on their content using n-grams.

SYNOPSIS
    indexer.py TARGET_DIRECTORY <flags>

DESCRIPTION
    Indexes files in a directory based on their content using n-grams.

POSITIONAL ARGUMENTS
    TARGET_DIRECTORY
        Type: str
        The root directory to search for files.

FLAGS
    -m, --max_file_size_mb=MAX_FILE_SIZE_MB
        Type: int
        Default: 1
        Maximum file size in megabytes to consider for indexing. Files larger than this will be skipped. Defaults to 1 MB.
    --n_grams_min=N_GRAMS_MIN
        Type: int
        Default: 4
        The minimum length of n-grams to generate. Defaults to 4.
    --n_grams_max=N_GRAMS_MAX
        Type: int
        Default: 4
        The maximum length of n-grams to generate. Defaults to 10.
    -s, --supported_extensions=SUPPORTED_EXTENSIONS
        Type: set
        Default: {'....
        A set of file extensions to include in the indexing. Only files with these extensions will be processed. Defaults to {".txt", ".py", ".md", ".json", ".yml", ".yaml"}.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```