import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ВСТАВЬТЕ СЮДА НОВЫЙ ТОКЕН (после отзыва старого в @BotFather)
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Каталог товаров (вложенные категории) ---
catalog = {
    "monster": {
        "name": "😈 Monster Energy",
        "lines": {
            "ultra": {
                "name": "Ultra",
                "items": [
                    {"id": "m_ultra_red", "name": "Monster Ultra Red", "price": "250 ₽"},
                    {"id": "m_ultra_white", "name": "Monster Ultra White", "price": "250 ₽"},
                    {"id": "m_ultra_black", "name": "Monster Ultra Black", "price": "250 ₽"},
                    {"id": "m_ultra_gold", "name": "Monster Ultra Gold", "price": "250 ₽"},
                    {"id": "m_ultra_strawberry_dreams", "name": "Monster Ultra Strawberry Dreams", "price": "250 ₽"},
                    {"id": "m_ultra_rosa", "name": "Monster Ultra Rosa", "price": "250 ₽"},
                    {"id": "m_ultra_vice_guava", "name": "Monster Ultra Vice Guava", "price": "250 ₽"},
                    {"id": "m_ultra_paradise", "name": "Monster Ultra Paradise", "price": "250 ₽"},
                    {"id": "m_ultra_fantasy_ruby_red", "name": "Monster Ultra Fantasy Ruby Red", "price": "250 ₽"}
                ]
            },
            "original": {
                "name": "Original",
                "items": [
                    {"id": "m_orig_01", "name": "Monster Original", "price": "250 ₽"},
                    {"id": "m_orig_02", "name": "Monster Nitro", "price": "250 ₽"},
                    {"id": "m_orig_03", "name": "Monster Lando Norris World", "price": "250 ₽"},
                    {"id": "m_orig_04", "name": "Monster Full Throttle", "price": "250 ₽"},
                    {"id": "m_orig_05", "name": "Monster VR|46", "price": "250 ₽"}
                ]
            },
            "juiced": {
                "name": "Juiced",
                "items": [
                    {"id": "m_juic_viking_berry", "name": "Monster Juiced Viking Berry", "price": "250 ₽"},
                    {"id": "m_juic_aussie_lemonade", "name": "Monster Juiced Aussie Lemonade", "price": "250 ₽"},
                    {"id": "m_juic_monarch", "name": "Monster Juiced Monarch", "price": "250 ₽"}
                ]
            },
            "punch": {
                "name": "Punch",
                "items": [
                    {"id": "m_pun_rio_punch", "name": "Monster Punch Rio Punch", "price": "250 ₽"}
                ]
            }
        }
    }
}
# URL картинок: ключ = item['id']
PRODUCT_PHOTOS = {
    "m_ultra_red": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+red&pos=6&rpt=simage&img_url=https%3A%2F%2Factivsports.ru%2Fwa-data%2Fpublic%2Fshop%2Fproducts%2F93%2F95%2F9593%2Fimages%2F3477%2F3477.970.png&from=tabbar&lr=2",
    "m_ultra_white": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+white&pos=0&rpt=simage&img_url=https%3A%2F%2Fyummasia24.ru%2Fwp-content%2Fuploads%2F2024%2F11%2F78aae73e_1d3c_4c34_bd74_cfa94676d168-2048x2048.jpg&from=tabbar&lr=2",
    "m_ultra_black": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+black&pos=0&rpt=simage&img_url=https%3A%2F%2Fkraspanda.ru%2Fwp-content%2Fuploads%2F2025%2F08%2Fenergeticheskij-napitok-monster-energy-ultra-black-zero-bez-saharap-500ml.jpg&from=tabbar&lr=2",
    "m_ultra_gold": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+gold&pos=5&rpt=simage&img_url=https%3A%2F%2Fdamcdn.samokat.ru%2Fdam-storage-ext-env-prod%2F2026%2F05%2Ff29723ce-02fc-4393-953e-043eec8832b9&from=tabbar&lr=2",
    "m_ultra_strawberry_dreams": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+strawberry+dreams&pos=0&rpt=simage&img_url=https%3A%2F%2Fsc04.alicdn.com%2Fkf%2FA11e4fcaa0a614134ba02a0b359f52a3dg%2F1645420366%2FA11e4fcaa0a614134ba02a0b359f52a3dg.png&from=tabbar&lr=2",
    "m_ultra_rosa": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+rosa&pos=0&rpt=simage&img_url=https%3A%2F%2Fsc04.alicdn.com%2Fkf%2FA56f26a1439264b33b6c58be43e831237S%2F15000755128%2FA56f26a1439264b33b6c58be43e831237S.jpg&from=tabbar&lr=2",
    "m_ultra_vice_guava": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+vice+guava&pos=0&rpt=simage&img_url=https%3A%2F%2Fkraspanda.ru%2Fwp-content%2Fuploads%2F2025%2F11%2Fenergeticheskij-napitok-monster-ultra-vice-guava-473ml.jpg&from=tabbar&lr=2",
    "m_ultra_paradise": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+paradise&pos=0&rpt=simage&img_url=https%3A%2F%2Fgladiatorsportpit.ru%2Fimage%2Fcatalog%2Fenergetiki%2Fmonster-energy%2Fenergeticheskij-napitok-bez-sahara-monster-500-ml-ultra-paradise-zero.jpg&from=tabbar&lr=2",
    "m_ultra_fantasy_ruby_red": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+ultra+fantasy+ruby+red&pos=0&rpt=simage&img_url=https%3A%2F%2Fgladiatorsportpit.ru%2Fimage%2Fcatalog%2Fenergetiki%2Fmonster-energy%2Fenergeticheskij-napitok-monster-500-ml-ultra-fantasy-ruby-red.jpg&from=tabbar&lr=2",
    "m_orig_01": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+original&pos=5&rpt=simage&img_url=https%3A%2F%2Fir.ozone.ru%2Fs3%2Fmultimedia-1-o%2Fc1000%2F13191267012.jpg&from=tabbar&lr=2",
    "m_orig_02": "https://www.cicalia.com/it/img/imgproducts/76139/xl_76139.jpg",
    "m_orig_03": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+lando+norris+gold&pos=5&rpt=simage&img_url=https%3A%2F%2Fopt24.ru%2Fupload%2Fdev2fun.imagecompress%2Fwebp%2Fiblock%2Ff1a%2Fwslm605oaaf9ee2izljlvv6c8crjoifc.webp&from=tabbar&lr=2",
    "m_orig_04": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+full+throttle&pos=0&rpt=simage&img_url=https%3A%2F%2Fa.allegroimg.com%2Foriginal%2F0535b6%2F58c3b8c045daaa5594cc4ed69f26%2FMonster-THROTTLE-Lewis-Hamilton-DRS-500-ml-1-sztuka&from=tabbar&lr=2",
    "m_orig_05": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+vr46+the+doctor&pos=0&rpt=simage&img_url=https%3A%2F%2Fpng.pngtree.com%2Fpng-clipart%2F20240204%2Foriginal%2Fpngtree-monster-energy-drink-illustrative-photo-png-image_14233665.png&from=tabbar&lr=2",
    "m_juic_viking_berry": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+juiced+viking+berry&pos=0&rpt=simage&img_url=https%3A%2F%2Fkraspanda.ru%2Fwp-content%2Fuploads%2F2025%2F12%2Fenergeticheskij-napitok-juice-monster-viking-berry-473ml.jpg&from=tabbar&lr=2",
    "m_juic_aussie_lemonade": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+juiced+aussie+lemonade&pos=1&rpt=simage&img_url=https%3A%2F%2Frimibaltic-res.cloudinary.com%2Fimage%2Fupload%2Fb_white%2Cc_limit%2Cdpr_auto%2Cf_auto%2Cq_auto%3Alow%2Cw_auto%2Fd_ecommerce%3Abackend-fallback.png%2FMAT_1374661_PCE_LV&from=tabbar&lr=2",
    "m_juic_monarch": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+juiced+monarch&pos=0&rpt=simage&img_url=https%3A%2F%2Fgladiatorsportpit.ru%2Fimage%2Fcatalog%2Fenergetiki%2Fmonster-energy%2Fenergeticheskij-napitok-monster-500-ml-monarch.jpg&from=tabbar&lr=2",
    "m_pun_rio_punch": "https://yandex.ru/images/search?search_client=unknown&text=monster+energy+rio+punch&pos=0&rpt=simage&img_url=https%3A%2F%2Fi.ebayimg.com%2Fimages%2Fg%2F3eQAAeSwS11nznJk%2Fs-l1600.jpg&from=tabbar&lr=2"
}


# --- Клавиатуры ---
def get_brands_keyboard():
    buttons = [[InlineKeyboardButton(text="😈 Monster Energy", callback_data="brand_monster")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_lines_keyboard(brand_key: str):
    brand = catalog[brand_key]
    buttons = []
    for line_key, line_data in brand["lines"].items():
        count = len(line_data["items"])
        buttons.append([
            InlineKeyboardButton(
                text=f"{line_data['name']} ({count})",
                callback_data=f"line_{brand_key}_{line_key}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад к брендам", callback_data="back_brands")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_items_keyboard(brand_key: str, line_key: str):
    line = catalog[brand_key]["lines"][line_key]
    buttons = []
    for item in line["items"]:
        buttons.append([
            InlineKeyboardButton(
                text=item["name"],
                callback_data=f"item_{brand_key}_{line_key}_{item['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад к линейкам", callback_data=f"back_lines_{brand_key}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- Обработчики команд и кнопок ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! 👋 Выбери каталог, чтобы посмотреть энергетики:",
        reply_markup=get_brands_keyboard()
    )

@dp.message(Command("catalog"))
async def cmd_catalog(message: Message):
    await message.answer(
        "Выбери бренд энергетика:",
        reply_markup=get_brands_keyboard()
    )

@dp.callback_query(F.data.startswith("brand_"))
async def handle_brand(callback: CallbackQuery):
    brand_key = callback.data.split("_")[1]
    if brand_key not in catalog:
        await callback.answer("Бренд не найден", show_alert=True)
        return
    await callback.message.edit_text(
        f"Вы выбрали: {catalog[brand_key]['name']}. Теперь выбери линейку:",
        reply_markup=get_lines_keyboard(brand_key)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("line_"))
async def handle_line(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer("Ошибка формата", show_alert=True)
        return
    _, brand_key, line_key = parts

    brand = catalog.get(brand_key)
    if not brand or line_key not in brand["lines"]:
        await callback.answer("Линейка не найдена", show_alert=True)
        return

    await callback.message.edit_text(
        f"{brand['name']} — линейка: {brand['lines'][line_key]['name']}\nВыбери напиток:",
        reply_markup=get_items_keyboard(brand_key, line_key)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("item_"))
async def handle_item(callback: CallbackQuery):
    # Формат: item_brand_key_line_key_item_id
    parts = callback.data.split("_", 3)
    if len(parts) != 4:
        await callback.answer("Ошибка формата", show_alert=True)
        return
    _, brand_key, line_key, item_id = parts

    brand = catalog.get(brand_key)
    line = brand["lines"][line_key] if brand else None
    item = next((i for i in line["items"] if i["id"] == item_id), None) if line else None

    if not item:
        await callback.answer("Товар не найден", show_alert=True)
        return

    # Текст описания (защита, если desc нет)
    desc = item.get("desc", "Описание пока отсутствует.")
    text = (
        f"🥤 <b>{item['name']}</b>\n\n"
        f"{desc}\n\n"
        f"💰 Цена: <b>{item['price']}</b>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_{item_id}")],
        [InlineKeyboardButton(text="🔙 Назад к линейке", callback_data=f"back_lines_{brand_key}")]
    ])

    photo_url = PRODUCT_PHOTOS.get(item_id)

    if photo_url:
        # Отправляем фото + подпись
        await callback.message.answer_photo(
            photo=photo_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=kb
        )
        # Удаляем старое сообщение (чтобы не было дублей)
        await callback.message.delete()
    else:
        # Если фото нет — просто текст
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

    await callback.answer()

@dp.callback_query(F.data == "back_brands")
async def back_to_brands(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Выбери бренд энергетика:",
            reply_markup=get_brands_keyboard()
        )
        await callback.answer()
    except Exception as e:
        logger.exception("Ошибка при возврате к брендам")
        # Если редактировать нельзя — отправляем новое сообщение вместо этого
        await callback.message.answer(
            "Выбери бренд энергетика:",
            reply_markup=get_brands_keyboard()
        )
        await callback.answer()


@dp.callback_query(F.data.startswith("back_lines_"))
async def back_to_lines(callback: CallbackQuery):
    try:
        parts = callback.data.split("_")
        if len(parts) != 3:
            await callback.answer("Ошибка кнопки", show_alert=True)
            return
        _, _, brand_key = parts

        if brand_key not in catalog:
            logger.warning(f"Неизвестный бренд: {brand_key}")
            await callback.answer("Бренд не найден", show_alert=True)
            return

        await callback.message.edit_text(
            f"Выбери линейку для {catalog[brand_key]['name']}:",
            reply_markup=get_lines_keyboard(brand_key)
        )
        await callback.answer()
    except Exception as e:
        logger.exception("Ошибка при возврате к линейке")
        # Фолбэк: если edit_text не сработал, просто отвечаем новым сообщением
        await callback.message.answer(
            f"Выбери линейку для {catalog[brand_key]['name']} (возврат):",
            reply_markup=get_lines_keyboard(brand_key)
        )
        await callback.answer()
@dp.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: CallbackQuery):
    item_id = callback.data.replace("buy_", "")
    # Ищем товар, чтобы показать подтверждение
    found_item = None
    for brand in catalog.values():
        for line in brand["lines"].values():
            for item in line["items"]:
                if item["id"] == item_id:
                    found_item = item
                    break

    if not found_item:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await callback.message.answer(
        f"✅ Вы выбрали: <b>{found_item['name']}</b>\n"
        f"Цена: {found_item['price']}\n\n"
        "Для заказа напишите менеджеру: @umbraos\n"
        "(Скоро подключим корзину)",
        parse_mode="HTML"
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
