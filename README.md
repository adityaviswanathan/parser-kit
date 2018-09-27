## Requirements/Setup

System requirements:
- Python 3.x (`brew install python3`)
- `pip` package manager for Python (the latest stable install script can be found on [their website](https://pip.pypa.io/en/stable/installing/))

### Managing dependencies
I recommend using a tool like `virtualenvwrapper` to manage dependencies from project to project, particularly because this project is written in Python3 while MacOS ships with Python2. You can install it via `pip`: 
```
$ sudo pip install virtualenvwrapper
...
$ source /usr/local/bin/virtualenvwrapper.sh
```

Once that's installed, find the path of (newly installed) Python3 on your system with:
```
$ which python3
> PATH_TO_PY3
```
Use that path when you create your virtualenv for this project, and then install the Python prerequisites via `pip`:
```
$ mkvirtualenv --python=PATH_TO_PY3 parser-kit 
(parser-kit)$ pip install -r requirements.txt
```

## Tools to build a parser

`parser-kit` provides tools to build a language model from the ground up. Start with:
- Example text ***T***
- Custom `Semantics` ***S*** (entity types that have arcs to other entities in the dependency tree)

With these inputs, we can build a parser with the following workflow:
- `labeler.py` is a CLI labeling tool of the form `f(T, S)`; it emits labeled training data ***L*** (**T** annotated with ***S***)
```
$ python labeler.py --inputfile=examples/examples.txt --outfile=training/labeled.out
```
- `model_generator.py` is a tool of the form `f(L)`; it emits a language model ***M***
```
$ python model_generator.py --inputfile=training/labeled.out --outfile=models/model1
```

With a language model, suppose we want to parse a new blob of text ***B***:
- `parser.py` is a tool of the form `f(M, B)`; it emits a parse that adheres to ***S***
```
$ python parser.py --text "how many wood could a wood chuck chuck if a wood chuck could chuck wood" --inputfile=models/model1
...
```

## HTTP interface (WIP)

`parser-kit` wraps a static language model with a HTTP server that handles inbound text blobs and returns their parses according to ***M***. Parses will be serialized via protobuf so clients will need to import the parse proto defined in this repo.

Clients can serialize/deserialize messages to the server by using interfaces in `semantics.proto`.
