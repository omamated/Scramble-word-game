from py2exe import freeze

freeze(
    windows=[
        {
            "script": "main.py",
            "dest_base": "WordScramble"
        }
    ],
    options={
        "packages": [
            "nltk",
            "customtkinter",
            "wordfreq",
            "PyDictionary"
        ],
        "includes": [
            "requests",
            "certifi",
            "urllib3"
        ],
        "dist_dir": "dist",
        "bundle_files": 3,
        "verbose": 2
    }
)