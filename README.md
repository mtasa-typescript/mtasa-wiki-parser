# MTASA Wiki Parser

Parses MTASA Wiki functions. Saves parsed data into dump directory.

## Connect [dump repository](https://github.com/mtasa-typescript/mtasa-wiki-dump)

```shell
git clone https://github.com/mtasa-typescript/mtasa-wiki-dump dump
```

## Install and run

*Warning:* You should edit [main.py](parser/main.py) `User values` block

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
cd parser
python3 main.py
```

# TypeScript types definitions generator

## How to run

```shell
cd to_typescript
python3 main.py
```

## Caveats

I. **Maybe one day type definitions generator will be moved to separate repository**

# Definition generation

Please view [Stages Description](docs/FunctionDocPipeline.png) if you to contribute MTASA Function definitions.

**Note:** OOP Declaration should be updated manually (until I write signature replacer)
