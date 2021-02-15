# MTASA Wiki Parser

Parses MTASA Wiki functions. Saves parsed data into dump directory. 

## Connect [dump repository](https://gitlab.toliak.ru/mtasa/typescript/wiki-dump)

```shell
git clone https://gitlab.toliak.ru/mtasa/typescript/wiki-dump dump --depth 1
```

## Install and run

*Warning:* You should edit [main.py](main.py) `User values` block

### Install venv

For Windows:

```shell
python3 -m venv .\venv\
.\venv\Scripts\activate
```

For Linux:

```shell
python3 -m venv ./venv/
source ./venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

### Run parser

After setting up variables in `User values` in `main.py` execute the command:
 
```shell
python3 main.py
```

# TypeScript types definitions generator

## How to run

```shell
python3 to_typescript/main.py
```

## Caveats

I. **Maybe one day type definitions generator will be moved to separate repository**

# All stages between MTASA Wiki and TypeScript type declarations

Please view [Stages Description](docs/FunctionDocPipeline.png) if you to contribute MTASA Function definitions.

# Repository information

[comment]: <> (TODO: Link)
[Repository with Issues, Merge Request, etc..](github.com)

[Mirror repository with CI/CD](https://gitlab.toliak.ru/mtasa/typescript/wiki-parser-python) 