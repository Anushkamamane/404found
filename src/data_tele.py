from telethon import TelegramClient
import pandas as pd
import asyncio

api_id = 25115480
api_hash = 'b46f903b2da528d109ca0bd178ee291e'
phone_number = '+917447667365'

client = TelegramClient('session_name', api_id, api_hash)

async def fetch_chat_messages(channel, limit=1000):
    await client.start(phone=phone_number)
    messages = []
    async for message in client.iter_messages(channel, limit=5000):
        messages.append(message.text)
    return messages

async def main():
    channels = ['TataSafariOwnersClub', 'Harrier_EV', 'TATA_Harrier_SafariClub',]  # Add your channel usernames here
    all_messages = []
    for ch in channels:
        print(f"Fetching messages from {ch}...")
        msgs = await fetch_chat_messages(ch, limit=5000)
        all_messages.extend(msgs)
    print(f"Total messages fetched from all channels: {len(all_messages)}")

    df = pd.DataFrame(all_messages, columns=['message'])
    df.to_csv('notebooks/data/tatamotors_telegram_messages.csv', index=False)

with client:
    client.loop.run_until_complete(main())
