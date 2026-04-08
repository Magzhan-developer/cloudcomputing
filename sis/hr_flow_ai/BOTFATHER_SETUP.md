# 🤖 BotFather Setup Guide — HR-Flow AI

Step-by-step instructions for configuring your bot's profile via [@BotFather](https://t.me/BotFather).

---

## 📸 Setting the Bot Avatar (Profile Picture)

### Prerequisites
- A square image (min. 512×512 px) representing your **HR-Flow AI Avatar**
- Access to your Telegram account that owns the bot

### Steps

1. **Open Telegram** and navigate to [@BotFather](https://t.me/BotFather)

2. **Send the command:**
   ```
   /mybots
   ```

3. **Select your bot** from the inline button list (e.g., `@hr_flow_ai_bot`)

4. **Tap** `Bot Settings` → `Edit Botpic`

5. **BotFather will ask:**
   > "OK. Send me a new profile photo for the bot."

6. **Send your image** — the one you prepared as your **HR-Flow AI Avatar**
   - Must be a square image
   - Minimum 512×512 pixels
   - Formats: JPG or PNG

7. **BotFather confirms:**
   > "Success! Profile photo updated."

8. ✅ **Done!** Your bot now displays the new avatar in all chats.

> 💡 **Tip:** To remove the avatar later, go to the same menu and tap `Delete Botpic`.

---

## 📝 Setting the Bot Description

These texts appear when users discover your bot.

### Short Description (shown in search results)

1. Open [@BotFather](https://t.me/BotFather)
2. Send:
   ```
   /setdescription
   ```
3. Select your bot
4. Send this description:
   ```
   HR-Flow AI — Smart resume screening for restaurants in Almaty.
   Upload a CV, get an instant AI evaluation. Powered by Gemini.
   ```

### About Text (shown on the bot's profile page)

1. Send:
   ```
   /setabouttext
   ```
2. Select your bot
3. Send:
   ```
   AI-powered HR assistant for the restaurant industry.
   Evaluates resumes against vacancy requirements.
   Built with ❤️ for Almaty's hospitality sector.
   ```

---

## 🗂️ Setting Bot Commands (manual method)

> **Preferred:** Use `python set_bot_commands.py` for automatic setup.
> Below is the manual BotFather method as a backup.

1. Open [@BotFather](https://t.me/BotFather)
2. Send:
   ```
   /setcommands
   ```
3. Select your bot
4. Send the following command list (paste **exactly** as shown):
   ```
   start - 🚀 Launch the bot & Welcome message
   vacancies - 🏢 View open vacancies
   upload - 📄 Upload a resume (PDF/TXT)
   admin_stats - 📊 FinOps Dashboard (Admin only)
   ```
5. BotFather confirms:
   > "Success! Command list updated."

---

## ✅ Verification Checklist

After completing the setup, verify everything:

| Check | How to verify |
|---|---|
| Avatar visible | Open the bot → profile picture is showing |
| Description set | Search for the bot → short text appears |
| Commands menu | Type `/` in the chat → 4 commands listed |
| `/start` works | Tap Start → welcome message appears |

---

## 🔧 Automated Command Setup

For the command menu, use the provided script instead of BotFather:

```bash
python set_bot_commands.py
```

Expected output:
```
┌──────────────────────────────────────────────┐
│  HR-Flow AI — Set Bot Commands               │
└──────────────────────────────────────────────┘

✅ Commands registered successfully!

   Users will now see this menu when they type /:

   /start          — 🚀 Launch the bot & Welcome message
   /vacancies      — 🏢 View open vacancies
   /upload         — 📄 Upload a resume (PDF/TXT)
   /admin_stats    — 📊 FinOps Dashboard (Admin only)

   📋 Verified: 4 command(s) active on Telegram.
```
