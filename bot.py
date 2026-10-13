import asyncio
import logging
from math import ceil
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

logging.basicConfig(level=logging.INFO)

# ⚠️ ВСТАВЬ СЮДА СВОЙ ТОКЕН ИЗ @BOTFATHER
TELEGRAM_BOT_TOKEN = "8730847952:AAHN5sw-C9lq-p5FP2Al7O8KA_ZTmFiSv-w"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Главное меню бота (Все 8 кнопок)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗣️ Speaking & Slang"),
            KeyboardButton(text="💪 Gym & Fitness"),
        ],
        [
            KeyboardButton(text="🧱 Body & Kitchen"),
            KeyboardButton(text="🧭 Map & Navigation"),
        ],
        [
            KeyboardButton(text="💰 Finance & Business"),
            KeyboardButton(text="📚 Irregular Verbs"),
        ],
        [
            KeyboardButton(text="🔬 Science & Tech"),
            KeyboardButton(text="🎯 IELTS C1 & Linking"),
        ],
    ],
    resize_keyboard=True,
)

# 🔥 ВСЕ ТВОИ СЛОВА И ФРАЗЫ БЕЗ ИСКЛЮЧЕНИЯ
VOCAB_DATABASE = {
    "Body & Kitchen": [
        "1. **Head / Face** `[hed / feɪs]` — *голова / лицо*\n   • *Example:* Keep your head up and stay focused.",
        "2. **Shoulder / Chest** `[ˈʃəʊldə / tʃest]` — *плечо / грудь*\n   • *Example:* He trained shoulders and chest today at the gym.",
        "3. **Arm / Elbow / Wrist** `[ɑːm / ˈelbəʊ / rɪst]` — *рука / локоть / запястье*\n   • *Example:* My wrist hurts after lifting heavy weights.",
        "4. **Hand / Finger / Thumb** `[hænd / ˈfɪŋɡə / θʌm]` — *кисть / палец / большой палец*\n   • *Example:* Give me a thumbs up if you understand.",
        "5. **Leg / Knee / Ankle** `[leɡ / niː / ˈæŋkl]` — *нога / колено / лодыжка*\n   • *Example:* He injured his knee during training.",
        "6. **Foot / Feet / Toes** `[fʊt / fiːt / təʊz]` — *стопа / стопы / пальцы ног*\n   • *Example:* Tap your feet to the rhythm of the music.",
        "7. **Stomach / Waist / Back** `[ˈstʌmək / weɪst / bæk]` — *живот / талия / спина*\n   • *Example:* Keep your back straight during deadlifts.",
        "8. **Spoon / Teaspoon** `[spuːn / ˈtiːspuːn]` — *ложка / чайная ложка*\n   • *Example:* Grab a spoon to eat the soup.",
        "9. **Fork** `[fɔːk]` — *вилка*\n   • *Example:* Pass me the fork and knife, please.",
        "10. **Knife / Knives** `[naɪf / naɪvz]` — *нож / ножи*\n   • *Example:* Be careful with that sharp knife.",
        "11. **Plate / Bowl / Dish** `[pleɪt / bəʊl / dɪʃ]` — *тарелка / глубокая миска / блюдо*\n   • *Example:* Put the fried rice in a deep bowl.",
        "12. **Cup / Glass / Mug** `[kʌp / ɡlɑːs / mʌɡ]` — *чашка / стакан / кружка*\n   • *Example:* I drank a big mug of coffee this morning.",
        "13. **Frying pan / Pot** `[ˈfraɪɪŋ pæn / pɒt]` — *сковорода / кастрюля*\n   • *Example:* Heat up some oil in the frying pan.",
        "14. **Cutting board** `[ˈkʌtɪŋ bɔːd]` — *разделочная доска*\n   • *Example:* Chop the vegetables on the cutting board.",
        "15. **Kettle / Teapot** `[ˈketl / ˈtiːpɒt]` — *чайник / заварочный чайник*\n   • *Example:* Boil the kettle to make hot tea.",
    ],
    "Speaking & Slang": [
        "1. **Watch your mouth!** `[wɒtʃ jɔː maʊθ]` — *следи за своим языком! / выбирай выражения!*",
        "2. **I'm broke** `[aɪm brəʊk]` — *я на мели / у меня нет денег*",
        "3. **Let's bounce** `[lets baʊns]` — *погнали / сматываемся*",
        "4. **That's a steal** `[ðæts ə stiːl]` — *это почти бесплатно / очень выгодно*",
        "5. **I'm down / I'm in** — *я за / я в теме*",
        "6. **Have a lot on my plate** — *у меня куча дел / завал*",
        "7. **Call it a day** — *закончить работу / закруглиться*",
        "8. **Out of the blue** — *совершенно внезапно / из ниоткуда*",
        "9. **Spill the tea** `[spɪl ðə tiː]` — *рассказывай сплетни / выкладывай секрет*",
        "10. **Low-key / High-key** — *втайне, скрытно / явно, открыто*",
        "11. **Rizz / Flex / Cap / No cap** — *харизма / понтоваться / ложь / без вранья*",
        "12. **GOAT** — *величайший всех времен*",
        "13. **Ghosted me** — *перестал отвечать / заигнорил*",
        "14. **What the fuck / Are you serious?** — *какого черта / ты серьезно?*",
        "15. **No fucking idea** — *без понятия / понятия не имею*",
        "16. **Scoot over** `[skuːt ˈəʊvə]` — *подвинься*",
        "17. **Keep the change** `[kiːp ðə tʃeɪndʒ]` — *сдачи не надо*",
        "18. **Not a big deal / No biggie** — *ничего страшного / пустяк*",
        "19. **Gonna / Wanna / Hafta / Gotta / Lemme / Gimme** — *сокращения разговорной речи*",
    ],
    "💪 Gym & Fitness": [
        "1. **No pain, no gain** — *без боли нет результата*",
        "2. **Built, not born** — *сделан своими руками, а не рожден таким*",
        "3. **Lift heavy, earn your rest** — *поднимай тяжело, заслужи отдых*",
        "4. **Train like a beast** — *тренируйся как зверь*",
        "5. **One more rep!** — *еще одно повторение!*",
        "6. **Feel the burn** — *почувствуй жжение в мышцах*",
        "7. **Mind over body** — *разум сильнее тела*",
        "8. **Outwork everyone** — *работай усерднее всех*",
        "9. **Sweat now, shine later** — *потей сейчас, сияй потом*",
    ],
    "🧭 Map & Navigation": [
        "1. **North / South / East / West** — *север / юг / восток / запад*",
        "2. **Northeast / Northwest / Southeast / Southwest** — *промежуточные стороны света*",
        "3. **Across from / Opposite** — *напротив / через дорогу*",
        "4. **In front of / Behind / Next to / Beside** — *спереди / сзади / рядом / около*",
        "5. **Adjacent to / Adjoining** — *примыкающий / смежный*",
        "6. **Roundabout / Junction / Crossroads / Dead end** — *кольцо / перекресток / развилка / тупик*",
        "7. **Go straight ahead / Turn left / Turn right** — *идите прямо / поверните налево / направо*",
    ],
    "💰 Finance & Business": [
        "1. **Bill** `[bɪl]` — *счет*",
        "2. **Fine** `[faɪn]` — *штраф*",
        "3. **Insurance** `[ɪnˈʃʊərəns]` — *страховка*",
        "4. **Contract** `[ˈkɒntrækt]` — *контракт, договор*",
        "5. **Expenses / Income** `[ɪkˈspensɪz / ˈɪnkʌm]` — *расходы / доходы*",
        "6. **Bankruptcy** `[ˈbæŋkrʌptsi]` — *банкротство*",
        "7. **Investments** `[ɪnˈvestmənts]` — *инвестиции*",
        "8. **Driver's license** `[ˈdraɪvəz ˈlaɪsns]` — *водительские права*",
    ],
    "🎯 IELTS C1 & Linking": [
        "1. **From my point of view** — *с моей точки зрения*",
        "2. **I couldn't agree more** — *абсолютно согласен*",
        "3. **To be honest, I've never really thought about that before but...** — *фраза-филлер для IELTS Part 3*",
        "4. **Easier said than done** — *легче сказать, чем сделать*",
        "5. **More often than not** — *чаще всего*",
        "6. **Once in a blue moon** — *крайне редко*",
        "7. **Tangible improvement** — *ощутимое улучшение*",
    ],
    "Irregular Verbs": [
        "1. **Be — Was/Were — Been** — *быть*",
        "2. **Become — Became — Become** — *становиться*",
        "3. **Begin — Began — Begun** — *начинать*",
        "4. **Break — Broke — Broken** — *ломать*",
        "5. **Build — Built — Built** — *строить*",
        "6. **Choose — Chose — Chosen** — *выбирать*",
        "7. **Drive — Drove — Driven** — *водить*",
        "8. **Find — Found — Found** — *находить*",
        "9. **Give — Gave — Given** — *давать*",
        "10. **Know — Knew — Known** — *знать*",
    ],
    "Science & Tech": [
        "1. **Computational** — *вычислительный*",
        "2. **Simulate** — *моделировать*",
        "3. **Digitized** — *оцифрованный*",
        "4. **Variables** — *переменные факторы*",
        "5. **Fossilized** — *окаменелый*",
        "6. **Extinct / Prehistoric** — *вымерший / доисторический*",
    ],
}

ITEMS_PER_PAGE = 4


def get_pagination_keyboard(category: str, page: int, total_pages: int):
    buttons = []
    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад", callback_data=f"page:{category}:{page-1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"📄 {page+1}/{total_pages}", callback_data="ignore"
        )
    )

    if page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️", callback_data=f"page:{category}:{page+1}"
            )
        )

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет, Илхом! Твой личный карманный словарь полностью готов.\n\n"
        "Выбирай нужную категорию на клавиатуре снизу:",
        reply_markup=main_keyboard,
    )


@dp.message(F.text)
async def show_category(message: types.Message):
    text = message.text
    category_key = None

    if "Speaking" in text:
        category_key = "Speaking & Slang"
    elif "Gym" in text:
        category_key = "💪 Gym & Fitness"
    elif "Body" in text:
        category_key = "Body & Kitchen"
    elif "Map" in text:
        category_key = "🧭 Map & Navigation"
    elif "Finance" in text:
        category_key = "💰 Finance & Business"
    elif "IELTS" in text:
        category_key = "🎯 IELTS C1 & Linking"
    elif "Irregular" in text:
        category_key = "Irregular Verbs"
    elif "Science" in text:
        category_key = "Science & Tech"

    if category_key and category_key in VOCAB_DATABASE:
        items = VOCAB_DATABASE[category_key]
        total_pages = ceil(len(items) / ITEMS_PER_PAGE)
        page = 0

        start_idx = page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_items = items[start_idx:end_idx]

        content = f"📚 **Категория: {category_key}**\n\n" + "\n\n".join(
            page_items
        )
        kb = get_pagination_keyboard(category_key, page, total_pages)

        await message.answer(content, parse_mode="Markdown", reply_markup=kb)
    else:
        await message.answer(
            "Воспользуйся кнопками на клавиатуре снизу!",
            reply_markup=main_keyboard,
        )


@dp.callback_query(F.data.startswith("page:"))
async def process_page_change(callback: types.CallbackQuery):
    _, category_key, page_str = callback.data.split(":")
    page = int(page_str)

    if category_key in VOCAB_DATABASE:
        items = VOCAB_DATABASE[category_key]
        total_pages = ceil(len(items) / ITEMS_PER_PAGE)

        start_idx = page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_items = items[start_idx:end_idx]

        content = f"📚 **Категория: {category_key}**\n\n" + "\n\n".join(
            page_items
        )
        kb = get_pagination_keyboard(category_key, page, total_pages)

        await callback.message.edit_text(
            content, parse_mode="Markdown", reply_markup=kb
        )
    await callback.answer()


async def main():
    print("🚀 Мега-Словарь Илхома успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())