import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

BOT_TOKEN = "8692303406:AAHeYoxivGz5FhuKJ7rkHjWP3SlnVwlO_Po"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

INFO = {
    "ism_familiya": "Nazarov Behruz",
    "yosh": 15,
    "haqida": "Men dasturlashni yaxshi ko'raman. Python va web dasturlash bilan shug'ullanaman.",

    "maktab": "79-sonli Denov maktabi",
    "yunalish": "Dasturiy ta'minot muhandisligi",

    "dasturlash_tillari": ["Python", "JavaScript", "HTML/CSS"],
    "texnologiyalar": ["Aiogram", "Django", "Git"],

    "telefon": "+998 99 123 77 74",
    "telegram": "username qo'yilmagan.",

    "shahar": "Surxondaryo viloyati",
    "manzil": "Denov tumani",

    "rasm": "nazarov_behruz_logo.jpg"
}


def asosiy_menyu() -> InlineKeyboardMarkup:
    tugmalar = [
        [InlineKeyboardButton(text="👤 Men haqimda", callback_data="men_haqimda")],
        [InlineKeyboardButton(text="🎓 Ta'limim", callback_data="talimim")],
        [InlineKeyboardButton(text="💻 Ko'nikmalarim", callback_data="konikmalar")],
        [InlineKeyboardButton(text="📞 Aloqa", callback_data="aloqa")],
        [InlineKeyboardButton(text="📍 Manzil", callback_data="manzil")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=tugmalar)


def ortga_tugma() -> InlineKeyboardMarkup:
    tugmalar = [
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="bosh_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=tugmalar)


async def caption_tahrirlash(callback: CallbackQuery, matn: str, reply_markup: InlineKeyboardMarkup):
    """
    Xabarni xavfsiz tahrirlash. Rasm bor bo'lsa caption,
    yo'q bo'lsa oddiy text tahrirlaydi.
    """
    try:

        await callback.message.edit_caption(
            caption=matn,
            reply_markup=reply_markup
        )
    except TelegramBadRequest as e:
        if "there is no caption" in str(e).lower() or "message is not modified" in str(e).lower():
            try:

                await callback.message.edit_text(
                    text=matn,
                    reply_markup=reply_markup
                )
            except TelegramBadRequest:

                pass
        else:
            raise e
    finally:

        await callback.answer()


@dp.message(CommandStart())
async def start(message: Message):
    xabar = (
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        f"Men {INFO['ism_familiya']} ning shaxsiy portfolio botiman.\n"
        f"Quyidagi tugmalar orqali men haqimda ma'lumot olishingiz mumkin! 👇"
    )

    try:
        photo = FSInputFile(INFO["rasm"])
        await message.answer_photo(
            photo=photo,
            caption=xabar,
            reply_markup=asosiy_menyu()
        )
    except Exception:
        # Rasm topilmasa yoki xato bo'lsa — oddiy matn yuborish
        await message.answer(
            text=xabar,
            reply_markup=asosiy_menyu()
        )


@dp.callback_query(F.data == "bosh_menu")
async def bosh_menu(callback: CallbackQuery):
    xabar = (
        f"{INFO['ism_familiya']} ning shaxsiy portfolio boti\n\n"
        f"Quyidagi tugmalardan birini tanlang 👇"
    )
    await caption_tahrirlash(callback, xabar, asosiy_menyu())


@dp.callback_query(F.data == "men_haqimda")
async def men_haqimda(callback: CallbackQuery):
    matn = (
        "👤 Men haqimda\n"
        "─────────────────\n"
        f"📛 Ism Familiya: {INFO['ism_familiya']}\n"
        f"🎂 Yosh: {INFO['yosh']}\n\n"
        f"📝 Qisqacha:\n{INFO['haqida']}"
    )
    await caption_tahrirlash(callback, matn, ortga_tugma())


@dp.callback_query(F.data == "talimim")
async def talimim(callback: CallbackQuery):
    matn = (
        "🎓 Ta'limim\n"
        "─────────────────\n"
        f"🏫 O'quv muassasasi:\n{INFO['maktab']}\n\n"
        f"📚 Yo'nalish:\n{INFO['yunalish']}"
    )
    await caption_tahrirlash(callback, matn, ortga_tugma())


@dp.callback_query(F.data == "konikmalar")
async def konikmalar(callback: CallbackQuery):
    dasturlash = "\n".join(
        [f"▪️ {til}" for til in INFO["dasturlash_tillari"]]
    )
    texnologiyalar = "\n".join(
        [f"▪️ {tex}" for tex in INFO["texnologiyalar"]]
    )
    matn = (
        "💻 Ko'nikmalarim\n"
        "─────────────────\n"
        f"🖥 Dasturlash tillari:\n{dasturlash}\n\n"
        f"⚙️ Texnologiyalar:\n{texnologiyalar}"
    )
    await caption_tahrirlash(callback, matn, ortga_tugma())


@dp.callback_query(F.data == "aloqa")
async def aloqa(callback: CallbackQuery):
    matn = (
        "📞 Aloqa\n"
        "─────────────────\n"
        f"📱 Telefon: {INFO['telefon']}\n"
        f"✈️ Telegram: {INFO['telegram']}"
    )
    await caption_tahrirlash(callback, matn, ortga_tugma())


@dp.callback_query(F.data == "manzil")
async def manzil_handler(callback: CallbackQuery):
    matn = (
        "📍 Manzil\n"
        "─────────────────\n"
        f"🌆 Shahar: {INFO['shahar']}\n"
        f"🏠 Tuman: {INFO['manzil']}"
    )
    await caption_tahrirlash(callback, matn, ortga_tugma())


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot ishlayapti... Ctrl+C bilan to'xtating.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
