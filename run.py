from telethon import TelegramClient
import json
import os
import msvcrt  # For "press any key to exit" on Windows

# === Load credentials from info.json ===
if not os.path.exists("info.json"):
    print("❌ info.json not found! Please create it with your API credentials.")
    print("""
Example content:
{
  "api_id": 12345678,
  "api_hash": "your_api_hash",
  "phone": "your_phone_number"
}
    """)
    input("\nPress any key to exit...")
    exit()

with open("info.json", "r") as f:
    config = json.load(f)

api_id = config.get("api_id")
api_hash = config.get("api_hash")
phone = config.get("phone")

if not all([api_id, api_hash, phone]):
    print("❌ Missing api_id, api_hash, or phone number in info.json.")
    input("\nPress any key to exit...")
    exit()

# === Session file in current folder with short name ===
SESSION_FILE = "session.chatid"
client = TelegramClient(SESSION_FILE, api_id, api_hash)

async def list_and_save_chat_ids():
    await client.start(phone=phone)
    dialogs = await client.get_dialogs()

    print("\n📋 Your Joined Groups & Channels:\n")
    output_lines = []

    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            title = dialog.name or "(No Title)"
            chat_id = dialog.id
            line = f"{title} → Chat ID: {chat_id}"
            print(f"🔹 {line}")
            output_lines.append(line)

    # Save to file
    with open("chat_ids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print("\n✅ All Chat IDs saved to chat_ids.txt.")
    print("\nPress any key to exit...", end="", flush=True)
    msvcrt.getch()

# === Run the client ===
with client:
    client.loop.run_until_complete(list_and_save_chat_ids())