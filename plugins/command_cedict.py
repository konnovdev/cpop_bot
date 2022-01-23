import re

from pyrogram import Client, filters, emoji
from pyrogram.types import Message, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton, \
    CallbackQuery

from tools.cedict import Cedict, EntryNotFound
from tools.utils import command_args_to_str

CEDICT_ENTRIES_PER_PAGE = 10

USAGE_MANUAL_TEXT = ("Usage: \n<code>/cedict your query</code>"
                     "\n\nFor example:\n<code>/cedict China</code>"
                     "\n\nYou can also use <code>/dic</code> instead of"
                     " <code>/cedict</code>")

PAGE_PATTERN = re.compile('[0-9]+')

cedict = Cedict()


@Client.on_message(filters.command(["cedict", "dict", "dic"])
                   & filters.incoming
                   & ~filters.edited)
async def command_cedict(_, message: Message):
    """/cedict question - get translation from cedict"""
    query = command_args_to_str(message.command)
    if query:
        first_page = 0
        try:
            cedict_response = cedict.get_cedict_result(query,
                                                       first_page,
                                                       CEDICT_ENTRIES_PER_PAGE)
            text = cedict_response.entries_list_to_str()
            reply_markup = (
                _make_next_page_button()
                if cedict_response.has_next_page
                else None
            )
        except EntryNotFound:
            text = _get_nothing_was_found_message(query)
            reply_markup = None
    else:
        text = USAGE_MANUAL_TEXT
        reply_markup = None

    await message.reply(text, reply_markup=reply_markup, quote=True)


@Client.on_callback_query(filters.regex(
    r"^cedict_(previous|next)_button_pressed$"
))
async def callback_query_cedict_button_pressed(_,
                                               callback_query: CallbackQuery):
    current_page_first_entry_number = PAGE_PATTERN.search(
        callback_query.message.text
    ).group()

    current_page = int(
        int(current_page_first_entry_number) / CEDICT_ENTRIES_PER_PAGE
    )

    if callback_query.data == "cedict_next_button_pressed":
        next_page = current_page + 1
    else:
        next_page = current_page - 1
    original_query = " ".join(
        callback_query.message.reply_to_message.text.split(" ")[1:]
    )

    try:
        cedict_response = cedict.get_cedict_result(original_query,
                                                   next_page,
                                                   CEDICT_ENTRIES_PER_PAGE)
        has_next_page = cedict_response.has_next_page
        has_previous_page = next_page > 0
        text = cedict_response.entries_list_to_str()

        if has_next_page and has_previous_page:
            reply_markup = _make_previous_and_next_page_buttons()
        elif has_previous_page:
            reply_markup = _make_previous_page_button()
        else:
            reply_markup = _make_next_page_button()
    except EntryNotFound:
        text = _get_nothing_was_found_message(original_query)
        reply_markup = None

    await callback_query.message.edit_text(text,
                                           reply_markup=reply_markup)


def _make_next_page_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Next {emoji.NEXT_TRACK_BUTTON}",
                    callback_data="cedict_next_button_pressed"
                )
            ]
        ]
    )


def _make_previous_page_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{emoji.LAST_TRACK_BUTTON} Previous",
                    callback_data="cedict_previous_button_pressed"
                )
            ]
        ]
    )


def _make_previous_and_next_page_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{emoji.LAST_TRACK_BUTTON} Previous",
                    callback_data="cedict_previous_button_pressed"
                ),
                InlineKeyboardButton(
                    f"Next {emoji.NEXT_TRACK_BUTTON}",
                    callback_data="cedict_next_button_pressed"
                )
            ]
        ]
    )


def _get_nothing_was_found_message(query: str):
    return f"Nothing in cedict was found for <b>{query}</b>." \
           f"\nTry a different query"
