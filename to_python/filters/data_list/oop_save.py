import collections
import os
import re
from typing import DefaultDict, List, Set

from crawler.filters.save_function_fetched import FilterSaveFetched
from to_python.core.context import ContextData
from to_python.core.filter import FilterAbstract
from to_python.core.types import CompoundOOPData


class FilterSaveFunctionDataError(RuntimeError):
    pass


class FilterSaveFunctionOOPData(FilterAbstract):
    """
    Saves all data into files
    """
    DUMP_FOLDER_ROOT = 'dump'
    DUMP_FOLDER = 'dump/oops'

    def get_context_data(self) -> ContextData:
        return getattr(self.context, self.context_type)

    def __init__(self):
        super().__init__('functions')

        self.categories: DefaultDict[
            str, List[CompoundOOPData]] = collections.defaultdict(lambda: [])
        self.files_to_import: Set[str] = set()

    def collect_by_category(self, f_name: str, data: CompoundOOPData):
        """
        Accumulates the data into the self.categories
        """
        url = self.get_context_data().urls[f_name]
        if url is None:
            raise FilterSaveFunctionDataError(
                f'Url no found for function name: {f_name}')

        self.categories[url.category].append(data)

    @staticmethod
    def clean_file_name(name: str) -> str:
        """
        Cleans file name (replaces spaces and redundant characters)
        """
        name = re.sub(r'[ \]\[\-=+.,:;]', '_', name)
        return name.lower().strip()

    def save_category_data(self, category: str):
        """
        Saves all parsed data for a single category
        """
        data_list = self.categories[category]

        if not os.path.exists(self.DUMP_FOLDER):
            os.mkdir(self.DUMP_FOLDER)

        category = self.clean_file_name(category)
        self.files_to_import.add(category)

        cache_file = os.path.join(self.DUMP_FOLDER, f'{category}.py')

        list_text = ',\n    '.join(repr(data) for data in data_list)
        text = f'''# Autogenerated file. ANY CHANGES WILL BE OVERWRITTEN
from to_python.core.types import FunctionType, \\
    FunctionArgument, \\
    FunctionArgumentValues, \\
    FunctionReturnTypes, \\
    FunctionSignature, \\
    FunctionDoc, \\
    FunctionOOP, \\
    FunctionOOPField, \\
    CompoundOOPData, \\
    FunctionData, \\
    CompoundFunctionData

DUMP_PARTIAL = [
    {list_text}
]
'''
        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(text)

    def save_init_file(self):
        """
        Generates __init__.py file
        """
        cache_file = os.path.join(self.DUMP_FOLDER_ROOT, '__init__.py')
        files = sorted(self.files_to_import)

        sections_text = '\n'.join(
            f'from to_python.dump.oops.{category} import '
            f'DUMP_PARTIAL as DP_O_{category.upper()}'
            for category in files
        )
        dump_text = f',\n{" " * 4}'.join(
            f'*DP_O_{category.upper()}'
            for category in files
        )
        text = f'''

{sections_text}

DUMP_OOPS = [
    {dump_text}
]
'''

        with open(cache_file, 'a', encoding='UTF-8', newline='\n') as cache:
            cache.write(text)

    def save_url_list(self):
        """
        Saves fetched url list
        """
        cache_file = os.path.join(self.DUMP_FOLDER_ROOT, 'url_list.py')

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(FilterSaveFetched.text_url_list(
                [self.get_context_data().urls[k] for k in
                 self.get_context_data().urls]
            ))

    def save_data(self):
        """
        Saves all parsed data from self.context.parsed into the files
        """
        for category in self.categories:
            self.save_category_data(category)
        print('Saved data\u001b[0m')

        self.save_init_file()
        print('Generated __init__.py file\u001b[0m')

        self.save_url_list()
        print('Save url_list.py file\u001b[0m')

    def apply(self):
        for f_name in self.context.oops:
            data = self.context.oops[f_name]
            self.collect_by_category(f_name, data)

        self.save_data()
