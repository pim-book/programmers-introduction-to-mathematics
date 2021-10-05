# Preprocess raw data

To re-run the raw data preprocessing, make sure you're in a python environment
with the base directory's `requirements.txt` installed. Then run

```
# install the word corpora from nltk
bash setup.sh

# process the documents
python cleaner.py
```

The cleaner takes about two minutes (probably could be faster, but it's a
one-time computation). The output is `all_stories.json`
