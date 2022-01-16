import re

from pyrogram import Client, filters
from pyrogram.types import Message, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton, \
    CallbackQuery

from tools.cedict import get_cedict_result
from tools.utils import command_args_to_str

CEDICT_ENTRIES_PER_PAGE = 10


@Client.on_message(filters.command(["cedict", "dict", "dic"])
                   & filters.incoming
                   & ~filters.edited)
async def command_cedict(_, message: Message):
    """/cedict question - get translation from cedict"""
    query = command_args_to_str(message.command)
    if query:
        first_page = 0
        cedict_response = get_cedict_result(query,
                                            first_page,
                                            CEDICT_ENTRIES_PER_PAGE)

        reply_markup = None
        if cedict_response.has_next_page:
            reply_markup = _make_next_page_button()

        await message.reply(cedict_response.formatted_result,
                            reply_markup=reply_markup, quote=True)
    else:
        await message.reply("Usage: \n<code>/cedict your query</code>"
                            "\n\nFor example:\n<code>/cedict China</code>"
                            "\n\nYou can also use <code>/dic</code> instead of"
                            " <code>/cedict</code>",
                            quote=True)


@Client.on_callback_query(filters.regex("cedict_next_button_pressed")
                          | filters.regex("cedict_previous_button_pressed"))
async def callback_query_cedict_button_pressed(_,
                                               callback_query: CallbackQuery):
    current_page_first_entry_number = re.search(
        '[0-9]+',
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
        callback_query.message.reply_to_message.text.split(" ")[1:])

    cedict_response = get_cedict_result(original_query,
                                        next_page,
                                        CEDICT_ENTRIES_PER_PAGE)
    has_next_page = cedict_response.has_next_page
    has_previous_page = next_page > 0

    if has_next_page and has_previous_page:
        reply_markup = _make_previous_and_next_page_buttons()
    elif has_previous_page:
        reply_markup = _make_previous_page_button()
    else:
        reply_markup = _make_next_page_button()

    await callback_query.message.edit_text(cedict_response.formatted_result,
                                           reply_markup=reply_markup)


def _make_next_page_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Next page / 下一頁",
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
                    "Previous page / 上一頁",
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
                    "Next page / 下一頁",
                    callback_data="cedict_next_button_pressed"
                )
            ],
            [
                InlineKeyboardButton(
                    "Previous page / 上一頁",
                    callback_data="cedict_previous_button_pressed"
                )
            ]
        ]
    )
