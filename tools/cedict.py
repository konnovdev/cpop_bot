class Cedict:
    def __init__(self, result: str, has_next_page: bool):
        self.formatted_result = result
        self.has_next_page = has_next_page


with open("static/cedict_ts.u8") as origin_file:
    cedict_data = origin_file.readlines()


def get_cedict_result(query: str,
                      required_page: int,
                      entries_per_page: int) -> Cedict:
    last_page = 0
    result_list = []
    entry_number = 1
    entry_per_page_index = 0
    for line in cedict_data:
        if query.casefold() in line.casefold():
            parsed_line = _parse_cedict_line(line)
            parsed_line_formatted = f"{entry_number}) " \
                                    f"<b>{parsed_line['traditional']}</b> " \
                                    f"[{parsed_line['simplified']}] " \
                                    f"<i>{parsed_line['pinyin']}</i> - " \
                                    f"<code>{parsed_line['english']}</code>\n"
            entry_per_page_index += 1

            if entry_per_page_index >= entries_per_page:
                entry_per_page_index = 0
                last_page += 1

            if len(result_list) == last_page:
                result_list.append("")

            result_list[last_page] += parsed_line_formatted
            entry_number += 1

    if not result_list:
        return Cedict(f"Nothing in cedict was found for <b>{query}</b>."
                      f"\nTry a different query", False)

    return Cedict(result_list[required_page], required_page < last_page)


def _parse_cedict_line(line) -> dict:
    parsed_cedict_line = {}
    line = line.rstrip('/')
    line = line.split('/')
    english = line[1]
    char_and_pinyin = line[0].split('[')
    characters = char_and_pinyin[0]
    characters = characters.split()
    traditional = characters[0]
    simplified = characters[1]
    pinyin = char_and_pinyin[1]
    pinyin = pinyin.rstrip()
    pinyin = pinyin.rstrip("]")
    parsed_cedict_line['traditional'] = traditional
    parsed_cedict_line['simplified'] = simplified
    parsed_cedict_line['pinyin'] = pinyin
    parsed_cedict_line['english'] = english
    return parsed_cedict_line
