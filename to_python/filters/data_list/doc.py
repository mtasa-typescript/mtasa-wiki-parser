import re
import sys
from copy import deepcopy
from typing import Dict, Optional, Tuple, List

from wikitextparser import WikiText, Section

from to_python.core.filter import FilterAbstract
from to_python.core.types import FunctionDoc


class FilterParseDocs(FilterAbstract):
    """
    Parse function documentation
    """

    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__(context_type)

    @staticmethod
    def get_sections_title_contains(wiki: WikiText, expected: str) -> \
            List[Tuple[Section, int]]:
        arg_sections = []
        for index, section in enumerate(wiki.sections):
            if section.title and expected in section.title.lower():
                arg_sections.append((section, index))

        return arg_sections

    @staticmethod
    def clean_line(line: str) -> str:
        return re.sub(r'[\[\]\'\"]', '', line).strip()

    @staticmethod
    def section_line_can_be_skipped(line: str) -> bool:
        if line == '' or line == '}}':
            return True

        if line.startswith('=') \
                or line.startswith('<!--') \
                or line.endswith('-->'):
            return True

        if re.match(r'^\{\{.*\}?\}?$', line):
            return True

        if re.match(r'^\[\[.+\]\]$', line):
            return True

        if re.match(r'.?.?.?None', line, re.IGNORECASE):
            return True

        if re.match(r'.+no arguments.+', line, re.IGNORECASE):
            return True

    @staticmethod
    def filter_raw_text(raw: str) -> str:
        result = ''
        for line in raw.split('\n'):
            line = line.strip()
            if FilterParseDocs.section_line_can_be_skipped(line):
                continue
            result += FilterParseDocs.clean_line(line) + '\n'

        return result.strip()

    def get_return_docs(self, f_name: str, raw: str, wiki: WikiText) -> str:
        """
        Accumulates documentation about returning value
        """
        arg_sections = self.get_sections_title_contains(wiki, 'return')

        result = ''
        for section, _ in arg_sections:
            content = str(section).lower()
            result += content + '\n'

        return self.filter_raw_text(result)

    ARG_NAME_REGEX = re.compile(r"\* *'+([^':]+):?'+")

    def parse_section_to_args(self, f_name: str, section) -> \
            Tuple[Dict[str, str], str]:
        """
        Parses single section to arguments dictionary and misc
        :return: Dictionary <argument name, docs> and misc (undetermined)
        """
        result = dict()
        misc = ''

        name: Optional[str] = None
        for line in str(section).split('\n'):
            line = line.strip()

            if self.section_line_can_be_skipped(line):
                continue

            arg_name = re.search(self.ARG_NAME_REGEX, line)
            if arg_name is None:
                if name is None:
                    if 'optional' not in section.title.lower():
                        print(
                            f'\u001b[33m[WARN] \u001b[0m'
                            f'Undetermined line in function '
                            f'"{f_name}"\u001b[0m'
                        )

                    continue

                result[name] += line + '\n'
                continue

            name = arg_name.group(1)
            name = self.clean_line(name)

            line = line[arg_name.end():].strip()
            line = self.clean_line(line)

            result[name] = line + '\n'

        for key in result:
            result[key] = result[key].strip()

        return result, misc

    def get_args_docs(self, f_name: str, raw: str, wiki: WikiText) -> \
            Tuple[Dict[str, str], str]:
        """
        Accumulates arguments description
        """
        from to_python.filters.data_list.signature import \
            FilterParseFunctionSignature

        arg_sections = self.get_sections_title_contains(wiki, 'argument')
        if not arg_sections:
            arg_sections = deepcopy(
                self.get_sections_title_contains(wiki, 'parameters'))

            # Clear section from code
            for section_info in arg_sections:
                section_info[0].contents = \
                    re.sub(FilterParseFunctionSignature.SELECT_CODE_REGEX, "",
                           section_info[0].contents)

        result = dict()
        misc_doc = ''
        # TODO: filter code for events parameters
        for section, _ in arg_sections:
            partial, misc = self.parse_section_to_args(f_name, section)
            misc_doc += misc + '\n'
            result.update(partial)

        return result, self.filter_raw_text(misc_doc)

    def get_docs(self, wiki_raw, f_name: str) -> str:
        """
        Accumulates description
        """
        wiki = wiki_raw[f_name]
        description_raw = str(wiki.sections[0])

        description_raw = re.sub(r'__NOTOC__\n?', '', description_raw,
                                 re.IGNORECASE)
        description_raw = description_raw.replace(str(wiki.templates[0]), '')
        description_raw = description_raw.strip()
        return self.filter_raw_text(description_raw)

    def apply(self):
        for f_name in self.context_data.parsed:
            raw_content = self.context_data.side_data[f_name]
            wiki_content = self.context_data.wiki_side[f_name]
            description = self.get_docs(self.context_data.wiki_raw, f_name)
            if not description:
                print(f'[ERROR] Page without a description: {f_name}',
                      file=sys.stderr)

            # TODO: refactor
            if raw_content.client is not None:
                return_doc = self.get_return_docs(f_name, raw_content.client,
                                                  wiki_content.client)
                args_doc, description_mixin = self.get_args_docs(
                    f_name,
                    raw_content.client,
                    wiki_content.client
                )
                self.context_data.parsed[f_name].client[0].docs = FunctionDoc(
                    description=(
                            description + '\n' + description_mixin).strip(),
                    arguments=args_doc,
                    result=return_doc
                )

            if raw_content.server is not None:
                return_doc = self.get_return_docs(f_name, raw_content.server,
                                                  wiki_content.server)
                args_doc, description_mixin = self.get_args_docs(
                    f_name,
                    raw_content.server,
                    wiki_content.server
                )
                self.context_data.parsed[f_name].server[0].docs = FunctionDoc(
                    description=(
                            description + '\n' + description_mixin).strip(),
                    arguments=args_doc,
                    result=return_doc
                )

        print('Docs parse complete\u001b[0m')
