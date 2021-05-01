# MTASA Wiki Parser

Parses MTASA Wiki functions. Saves parsed data into dump directory.

Minimal expected Python version: 3.7

## Connect [dump repository](https://github.com/mtasa-typescript/mtasa-wiki-dump)

### For developers

```shell
git clone https://github.com/mtasa-typescript/mtasa-wiki-dump to_python/dump
mkdir -p crawler/dump_html
git clone https://github.com/mtasa-typescript/mtasa-lua-types to_typescript/output
```

### For internal developers

```shell
git clone https://github.com/mtasa-typescript/mtasa-wiki-dump to_python/dump
git clone https://github.com/mtasa-typescript/mtasa-wiki-dump_html crawler/dump_html
git clone https://github.com/mtasa-typescript/mtasa-lua-types to_typescript/output
```

## Install and run

*Warning:* You should edit [main.py](to_python/main.py) `User values` block

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
