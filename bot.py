
import asyncio
import logging
import os
import replicate
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

# Railway Environment Variables'dan kalitlarni olish (agar yo'q bo'lsa zaxira kalitlar ishlaydi)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8723145433:AAH_GreWnfPp0nLcFQnC28B85K0eqspn_4M")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "R8_CVkIHOPcJlSTkrs9jWLd9qs9v5rph6O13glxO")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Nano Banana 2 uchun mahsulotni brend darajasiga keltiruvchi prompt
SYSTEM_PROMPT = (
    "High-end professional product photo, cinematic studio lighting, "
    "ultra-detailed texture, 8k resolution, clean commercial background"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Salom! **BrendFoto AI** botiga xush kelibsiz! 📸\n\n"
        "Mahsulotingiz rasmini yuboring, men uni Google Nano Banana 2 orqali brend darajasiga keltirib beraman."
    )

@dp.message(F.photo)
async def process_photo(message: types.Message):
    status_msg = await message.answer("📸 Rasm qabul qilindi. Nano Banana 2 ishlov bermoqda, biroz kuting...")

    try:
        # Telegram serveridan rasm manzilini olish
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

        # Google Nano Banana 2 modelini ishga tushirish
        output = await asyncio.to_thread(
            replicate.run,
            "google/nano-banana-2",
            input={
                "prompt": SYSTEM_PROMPT,
                "image_input": [image_url],  # Nano Banana 2 rasm linkini massiv usulida qabul qiladi
                "aspect_ratio": "match_input_image",  # Asl rasm proporsiyasini saqlab qoladi
                "output_format": "jpg"
            }
        )

        # Natijani olish va yuborish
        if output:
            result_url = str(output[0]) if isinstance(output, list) else str(output)
            await message.answer_photo(
                photo=result_url,
                caption="✨ **BrendFoto AI (Nano Banana 2)** natijasi tayyor!"
            )
        else:
            await message.answer("Rasm ishlanmadi, qaytadan urinib ko'ring.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
    
    finally:
        await status_msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
