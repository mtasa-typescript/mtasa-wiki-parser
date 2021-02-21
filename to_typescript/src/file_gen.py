import re


def prepare_category_file_name(category: str) -> str:
    result = category.strip().lower()
    result = re.sub(r'[ -=+\[\].]', '_', result)
    result = result.replace('_functions', '')

    return f'{result}.d.ts'
