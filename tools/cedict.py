from dataclasses import dataclass
from typing import List


class EntryNotFound(ValueError):
    pass


@dataclass
class CedictEntry:
    def __init__(self,
                 entry_number: int,
                 traditional: str,
                 simplified: str,
                 pinyin: str,
                 english: str):
        self.entry_number = entry_number
        self.traditional = traditional
        self.simplified = simplified
        self.pinyin = pinyin
        self.english = english

    def __str__(self):
        return f"{self.entry_number}) " \
               f"<b>{self.traditional}</b> " \
               f"[{self.simplified}] " \
               f"<i>{self.pinyin}</i> - " \
               f"<code>{self.english}</code>"


@dataclass
class CedictCollection:
    def __init__(self, entries: List[CedictEntry], has_next_page: bool):
        self.entries = entries
        self.has_next_page = has_next_page

    def entries_list_to_str(self):
        return '\n'.join(str(entry) for entry in self.entries)


class Cedict:
    cedict_data = []

    def __init__(self):
        with open("static/cedict_ts.u8") as origin_file:
            self.cedict_data = origin_file.readlines()

    def get_cedict_result(self,
                          query: str,
                          required_page: int,
                          entries_per_page: int) -> CedictCollection:
        last_page = 0
        result_list: List[List[CedictEntry]] = []
        entries_list: List[CedictEntry] = []
        entry_number = 1
        entry_per_page_index = 0
        for line in self.cedict_data:
            if query.casefold() in line.casefold():
                cedict_entry = _parse_cedict_line(entry_number, line)
                entry_per_page_index += 1

                if entry_per_page_index >= entries_per_page:
                    entry_per_page_index = 0
                    last_page += 1

                if len(result_list) == last_page:
                    entries_list = [cedict_entry]
                    result_list.append(entries_list)
                else:
                    entries_list.append(cedict_entry)

                entry_number += 1

        if not result_list:
            raise EntryNotFound

        return CedictCollection(result_list[required_page],
                                required_page < last_page)


def _parse_cedict_line(line_number: int, line: str) -> CedictEntry:
    line = line.rstrip('/').split('/')
    char_and_pinyin = line[0].split('[')
    characters = char_and_pinyin[0].split()
    return CedictEntry(entry_number=line_number,
                       traditional=characters[0],
                       simplified=characters[1],
                       pinyin=char_and_pinyin[1].rstrip().rstrip("]"),
                       english=line[1])
