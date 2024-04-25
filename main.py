import json
import spacy
import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


with open("./data/json/answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

nlp = spacy.load("./output/model-last")


async def send_long_message(message, chat_id, context, max_chunk_length=4000) -> None:
    chunks = [
        message[i : i + max_chunk_length]
        for i in range(0, len(message), max_chunk_length)
    ]
    for i, chunk in enumerate(chunks, start=1):
        await context.bot.send_message(chat_id=chat_id, text=f"{chunk}")


def get_results(user_input):
    doc = nlp(user_input)

    results = []

    for ent in doc.ents:
        for answer in answers:
            if "id" in answer and any(res.get("id") == answer["id"] for res in results):
                continue

            if (
                ent.text.lower() in answer["body"].lower()
                or ent.label_ in answer["label"]
            ):
                results.append(answer)
                break

    return results


async def handle_text(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    results = get_results(user_input=user_input)

    chat_id = update.effective_chat.id

    if len(results) > 1:
        response_text = "\n".join(
            f"Result {i + 1}: {result['body']} \n" for i, result in enumerate(results)
        )
        response_text = (
            f"Here are multiple results for your question:\n\n{response_text}"
        )

        await send_long_message(message=response_text, chat_id=chat_id, context=context)
    elif len(results) == 1:
        response_text = f"Here's what I've found:\n {results[0]['body']}"

        await context.bot.send_message(
            chat_id=chat_id,
            text=response_text,
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="I'm sorry, I didn't find an answer to your question.",
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
        Welcome to IT Network Support! You can ask me about various IT-related topics.
        I'm always happy to help!
        """,
    )


def main_telegram() -> None:
    application = (
        ApplicationBuilder()
        .token("6803422784:AAGe8z6lQB6y_muRfNIzofkq7-YE0Ig4HBw")
        .build()
    )

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == "__main__":
    main_telegram()
