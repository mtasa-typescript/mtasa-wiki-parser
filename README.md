# 🔁 MTASA Wiki Parser

Parses MTASA Wiki functions and events. Saves parsed data into dump directory.

Minimal expected Python version: 3.7

# 💠 Prepare the project

## 📦 Connect Dump Repositories

```shell
git clone https://github.com/mtasa-typescript/mtasa-wiki-dump to_python/dump
git clone https://github.com/mtasa-typescript/mtasa-mediawiki-dump crawler/dump_html
git clone https://github.com/mtasa-typescript/mtasa-lua-types to_typescript/output
```

## 🗃 Install venv

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

# 🏃‍♂️ Run application

## ▶ Crawler

Used for dumping MediaWiki content about functions and events from MTASA Wiki.

### ⏯ Execute

```bash
cd crawler
python3 main.py
```

## ▶ To Python

Tool for transforming Media Wiki content into Python objects.

### ⏯ Execute

```bash
cd to_python
python3 main.py
```

## ▶ To TypeScript

Tool for transforming Python objects into TypeScript definitions.

### ⏯ Execute

```bash
cd to_typescript
python3 main.py
```

# 🛠 How to contribute

1. Create an issue with the bug or the idea.
2. If you would like to create the Merge Request (Pull Request), 
suggest the solution you would like to provide in the issue.
3. Wait 1-2 days for an answer.
4. If the maintainer agreed with your suggestion 
(or if there is no answer in 1-2 days), create the Merge Request 
with your solution. 


Rules:
- Use `flake8` to validate code style
- Use `pytest` to cover code with tests
