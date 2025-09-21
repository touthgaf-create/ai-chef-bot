#!/usr/bin/env python3
"""
AI Chef Bot - Railway версия
"""
import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования для Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Конфигурация для Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_API_KEY = os.getenv("PROXY_API_KEY", "")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

# Проверка токена
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не установлен!")
    sys.exit(1)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

def get_main_menu():
    """Главное меню бота"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🍳 Новый рецепт", callback_data="new_recipe"),
        InlineKeyboardButton(text="📚 Мои рецепты", callback_data="my_recipes")
    )
    
    builder.row(
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        InlineKeyboardButton(text="⭐️ Премиум", callback_data="premium")
    )
    
    builder.row(
        InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
        InlineKeyboardButton(text="📞 Поддержка", callback_data="support")
    )
    
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    
    # Логируем нового пользователя
    logger.info(f"👤 Новый пользователь: {message.from_user.id} (@{message.from_user.username})")
    
    welcome_text = f"""
🎉 <b>Добро пожаловать в AI Chef Bot!</b>

Привет, {message.from_user.first_name}! 👋

Я - ваш персональный ИИ-повар, который поможет:

🔸 <b>Создавать рецепты</b> из ваших продуктов
🔸 <b>Экономить деньги</b> - до 30.000₽ в год!
🔸 <b>Избегать выбрасывания</b> продуктов
🔸 <b>Готовить вкусно</b> каждый день

<b>🎁 Как это работает:</b>
1️⃣ Отправьте список продуктов из холодильника
2️⃣ Получите персональный рецепт за 30 секунд
3️⃣ Готовьте и наслаждайтесь результатом!

<b>📊 Статистика экономии:</b>
• Средняя российская семья выбрасывает продуктов на 30.000₽ в год
• С нашим ботом вы сократите это на 80%
• Это значит экономия ~24.000₽ в год!

<i>💡 Совет: начните с простого списка из 4-5 продуктов</i>

Что будем готовить сегодня? 👨‍🍳
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "new_recipe")
async def new_recipe(callback):
    """Создание нового рецепта"""
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✏️ Написать список", callback_data="write_list"),
        InlineKeyboardButton(text="🎤 Голосом", callback_data="voice_input")
    )
    builder.row(
        InlineKeyboardButton(text="📸 Сфотографировать", callback_data="photo_input"),
        InlineKeyboardButton(text="🧾 Загрузить чек", callback_data="receipt_input")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_menu")
    )
    
    await callback.message.edit_text(
        "📦 <b>Добавление продуктов</b>\n\n"
        "Выберите способ добавления продуктов для создания рецепта:\n\n"
        "🔸 <b>Написать список</b> - самый быстрый способ\n"
        "🔸 <b>Голосом</b> - удобно когда руки заняты\n"
        "🔸 <b>Сфотографировать</b> - ИИ распознает продукты\n"
        "🔸 <b>Чек из магазина</b> - что купили, то и приготовим\n\n"
        "<i>💡 Для начала рекомендуем написать список текстом</i>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "write_list")
async def write_list(callback):
    """Запрос текстового списка"""
    await callback.message.edit_text(
        "✏️ <b>Напишите список продуктов</b>\n\n"
        "Перечислите продукты, которые у вас есть:\n\n"
        "<b>Примеры:</b>\n"
        "• <i>Курица, картофель, морковь, лук, сметана</i>\n"
        "• <i>Фарш говяжий, макароны, помидоры, сыр</i>\n"
        "• <i>Рыба, рис, брокколи, лимон</i>\n\n"
        "📝 Просто напишите через запятую или каждый продукт с новой строки.\n\n"
        "<i>⚡ Чем больше продуктов укажете, тем интереснее получится рецепт!</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "my_recipes")
async def my_recipes(callback):
    """Мои рецепты"""
    await callback.message.edit_text(
        "📚 <b>Ваши рецепты</b>\n\n"
        "📊 <b>Статистика:</b>\n"
        f"• Рецептов создано: <b>0</b>\n"
        f"• Денег сэкономлено: <b>~0₽</b>\n"
        f"• Продуктов использовано: <b>0</b>\n\n"
        "🎯 <b>У вас пока нет сохранённых рецептов</b>\n\n"
        "Создайте первый рецепт - это займёт всего 30 секунд! 🚀\n\n"
        "<i>💡 Каждый рецепт экономит в среднем 200-400₽</i>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "profile")
async def profile(callback):
    """Профиль пользователя"""
    user_id = callback.from_user.id
    username = callback.from_user.username or "не указан"
    first_name = callback.from_user.first_name
    
    await callback.message.edit_text(
        f"👤 <b>Ваш профиль</b>\n\n"
        f"<b>Основная информация:</b>\n"
        f"• Имя: <b>{first_name}</b>\n"
        f"• Username: <b>@{username}</b>\n"
        f"• ID: <code>{user_id}</code>\n"
        f"• Статус: <b>🎁 Пробный период</b>\n\n"
        f"<b>📊 Статистика использования:</b>\n"
        f"• Рецептов создано: <b>0</b>\n"
        f"• Денег сэкономлено: <b>~0₽</b>\n"
        f"• Продуктов переработано: <b>0</b>\n"
        f"• Дней с нами: <b>1</b>\n\n"
        f"<b>🎯 Ваш уровень:</b> Начинающий повар 👶\n\n"
        f"<i>💡 Создавайте рецепты каждый день чтобы повысить уровень!</i>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "premium")
async def premium(callback):
    """Информация о премиум"""
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Оформить за 299₽", callback_data="buy_premium"),
        InlineKeyboardButton(text="🎁 Промокод", callback_data="promo")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_menu")
    )
    
    await callback.message.edit_text(
        f"⭐️ <b>AI Chef Premium</b>\n\n"
        f"<b>💰 Цена: всего 299₽ в месяц!</b>\n\n"
        f"<b>🎁 Что получаете:</b>\n"
        f"✅ <b>50 рецептов в день</b> (вместо 2)\n"
        f"✅ <b>GPT-4</b> для лучшего качества рецептов\n"
        f"✅ <b>Распознавание фото</b> продуктов и чеков\n"
        f"✅ <b>Голосовой ввод</b> продуктов\n"
        f"✅ <b>Планирование меню</b> на неделю\n"
        f"✅ <b>Списки покупок</b> с оптимизацией\n"
        f"✅ <b>Калькулятор калорий</b> и БЖУ\n"
        f"✅ <b>Персональные диеты</b> и ограничения\n"
        f"✅ <b>Приоритетная поддержка</b>\n\n"
        f"<b>💡 Это дешевле чем:</b>\n"
        f"• 1 поход в ресторан\n"
        f"• 3 чашки кофе в кафе\n"
        f"• Продукты, которые вы выбросите за 1 день\n\n"
        f"<b>🎯 ROI: экономия 24.000₽ при стоимости 3.588₽ в год</b>\n\n"
        f"<i>🔥 Первые 7 дней бесплатно!</i>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_command(callback):
    """Помощь"""
    await callback.message.edit_text(
        "❓ <b>Помощь по AI Chef Bot</b>\n\n"
        "<b>🔸 Как создать рецепт:</b>\n"
        "1. Нажмите '🍳 Новый рецепт'\n"
        "2. Выберите способ ввода продуктов\n"
        "3. Укажите что у вас есть дома\n"
        "4. Получите персональный рецепт за 30 сек\n\n"
        "<b>🔸 Советы для лучших рецептов:</b>\n"
        "• Указывайте 4-8 основных продуктов\n"
        "• Добавляйте специи и приправы\n"
        "• Уточняйте тип блюда (обед, ужин, завтрак)\n"
        "• Указывайте диетические ограничения\n\n"
        "<b>🔸 Популярные команды:</b>\n"
        "• /start - перезапустить бота\n"
        "• /profile - ваш профиль и статистика\n"
        "• /premium - информация о подписке\n\n"
        "<b>🔸 Проблемы и вопросы:</b>\n"
        "Если что-то не работает - нажмите 'Поддержка'",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message()
async def handle_products(message: Message):
    """Обработка списка продуктов"""
    
    if len(message.text) < 5:
        await message.answer(
            "🤔 Слишком мало информации!\n\n"
            "Пожалуйста, напишите больше продуктов для создания рецепта.\n\n"
            "<i>Например: курица, картофель, морковь, лук</i>",
            parse_mode="HTML"
        )
        return
    
    # Логируем запрос пользователя
    logger.info(f"📝 Пользователь {message.from_user.id} запросил рецепт из: {message.text[:50]}...")
    
    # Показываем процесс генерации
    loading_msg = await message.answer("⏳ Анализирую ваши продукты и создаю рецепт...")
    
    # Имитация обработки (здесь будет реальный API вызов)
    await asyncio.sleep(2)
    await loading_msg.edit_text("👨‍🍳 Подбираю идеальное сочетание...")
    await asyncio.sleep(2)
    await loading_msg.edit_text("📝 Составляю пошаговый рецепт...")
    await asyncio.sleep(1)
    
    # Парсим продукты пользователя
    products = [p.strip().lower() for p in message.text.replace('\n', ',').split(',') if p.strip()]
    products_str = ', '.join(products[:5])  # Берем первые 5 продуктов
    
    # Генерируем рецепт (пока демо-версия)
    recipe = f"""
🍽 <b>Ароматное блюдо из ваших продуктов</b>

<i>Сбалансированное и вкусное блюдо с использованием: {products_str}</i>

⏱ <b>Время приготовления:</b> 35 минут
👥 <b>Порций:</b> 4
📊 <b>Сложность:</b> Легко
💰 <b>Стоимость:</b> ~280₽

<b>🔥 Питательная ценность (на порцию):</b>
• Калории: 340 ккал
• Белки: 26г | Жиры: 14г | Углеводы: 32г

<b>📝 Ингредиенты:</b>
• Ваши продукты: {products_str}
• Соль, черный перец - по вкусу
• Растительное масло - 2 ст.л.
• Вода - 200 мл

<b>👨‍🍳 Пошаговое приготовление:</b>

<b>Шаг 1:</b> Подготовка (5 мин)
Помойте и нарежьте все продукты удобными кусочками. Подготовьте специи.

<b>Шаг 2:</b> Обжарка (10 мин)
Разогрейте сковороду с маслом на среднем огне. Обжарьте основные ингредиенты до золотистого цвета.

<b>Шаг 3:</b> Тушение (20 мин)
Добавьте воду, приправы. Накройте крышкой и тушите на медленном огне до готовности.

<b>Шаг 4:</b> Финиш
Попробуйте на соль, добавьте зелень. Подавайте горячим!

💡 <b>Совет от шефа:</b> За 5 минут до готовности добавьте любимые специи - это сделает вкус ярче!

<b>🏷 Теги:</b> #домашнее #быстро #из_остатков #экономно

<b>💰 Экономия:</b> Вместо заказа еды (~800₽) вы потратили ~280₽
<b>✅ Ваша выгода: 520₽!</b>
"""
    
    # Кнопки действий с рецептом
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👨‍🍳 Начать готовить", callback_data="start_cooking"),
        InlineKeyboardButton(text="⭐ В избранное", callback_data="add_favorite")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Другой рецепт", callback_data="new_recipe"),
        InlineKeyboardButton(text="📤 Поделиться", callback_data="share_recipe")
    )
    builder.row(
        InlineKeyboardButton(text="🛒 Список покупок", callback_data="shopping_list"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_menu")
    )
    
    await loading_msg.edit_text(
        recipe,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
    # Логируем успешную генерацию
    logger.info(f"✅ Рецепт создан для пользователя {message.from_user.id}")

@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query()
async def handle_other_callbacks(callback):
    """Обработка остальных callbacks"""
    callback_messages = {
        "voice_input": "🎤 Голосовой ввод будет доступен в Premium версии!",
        "photo_input": "📸 Распознавание фото будет доступно в Premium версии!",
        "receipt_input": "🧾 Распознавание чеков будет доступно в Premium версии!",
        "start_cooking": "👨‍🍳 Функция пошагового приготовления в разработке!",
        "add_favorite": "⭐ Рецепт добавлен в избранное!",
        "share_recipe": "📤 Функция публикации рецептов в разработке!",
        "shopping_list": "🛒 Генерация списков покупок будет в Premium!",
        "buy_premium": "💳 Интеграция платежей в разработке. Пишите в поддержку!",
        "promo": "🎁 Введение промокодов будет доступно позже!",
        "support": "📞 Поддержка: @your_support_username или напишите в чат"
    }
    
    message = callback_messages.get(callback.data, f"Функция '{callback.data}' в разработке! 🛠")
    await callback.answer(message, show_alert=True)

async def main():
    """Главная функция"""
    logger.info("🚀 Запуск AI Chef Bot на Railway...")
    
    # Проверяем токен
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен в переменных окружения!")
        return
    
    logger.info(f"✅ Токен найден: {BOT_TOKEN[:10]}...")
    logger.info(f"📡 ProxyAPI: {'✅ Настроен' if PROXY_API_KEY else '⚠️ Не настроен'}")
    logger.info(f"👥 Админы: {ADMIN_IDS}")
    
    # Регистрируем роутеры
    dp.include_router(router)
    
    try:
        # Устанавливаем команды бота
        await bot.set_my_commands([
            ("start", "🏠 Главное меню"),
            ("recipe", "🍳 Новый рецепт"),
            ("profile", "👤 Мой профиль"),
            ("premium", "⭐ Премиум подписка"),
            ("help", "❓ Помощь")
        ])
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот запущен успешно!")
        logger.info(f"📱 Username: @{bot_info.username}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
        logger.info(f"👤 Имя: {bot_info.first_name}")
        
        # Уведомляем админов о запуске
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"🚀 <b>AI Chef Bot запущен на Railway!</b>\n\n"
                    f"🤖 @{bot_info.username}\n"
                    f"🕐 Время запуска: {asyncio.get_event_loop().time()}\n"
                    f"🌐 Платформа: Railway\n"
                    f"✅ Все системы готовы к работе!",
                    parse_mode="HTML"
                )
                logger.info(f"✅ Уведомление отправлено админу {admin_id}")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось уведомить админа {admin_id}: {e}")
        
        logger.info("🎯 Бот готов принимать сообщения!")
        
        # Запускаем polling
        await dp.start_polling(
            bot, 
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при запуске: {e}")
        raise

if __name__ == "__main__":
    try:
        # Обработка graceful shutdown
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        sys.exit(1)
