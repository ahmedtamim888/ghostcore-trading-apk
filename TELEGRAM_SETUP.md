# 📱 TELEGRAM INTEGRATION SETUP GUIDE

## Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start chat and send `/newbot`
3. Choose a name: `COSMIC OMNI-BRAIN AI`
4. Choose username: `cosmic_omni_brain_bot` (or similar)
5. Copy the **Bot Token** (looks like: `123456789:ABCdefGhIJklmnoPQrstuvwxyz`)

## Step 2: Get Chat ID

1. Start chat with your new bot
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":123456789` - this is your Chat ID

## Step 3: Set Environment Variables

### For Local Development:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### For Docker:
```bash
docker run -e TELEGRAM_BOT_TOKEN="your_token" -e TELEGRAM_CHAT_ID="your_id" cosmic-ai
```

### For Cloud Platforms:
Add these as environment variables in your platform's settings:
- `TELEGRAM_BOT_TOKEN`: Your bot token
- `TELEGRAM_CHAT_ID`: Your chat ID

## Step 4: Test Integration

Once deployed, upload a chart image and you should receive signals like:

```
🔮 COSMIC OMNI-BRAIN SIGNAL
🕒 1M | 15:30 (UTC+6)
🎯 Signal: CALL
📖 Strategy: Trap Fade Reversal
📊 Confidence: 87%
🖼️ [Annotated Chart Attached]
```

## Troubleshooting

- **Bot not responding**: Check bot token
- **No messages received**: Verify chat ID
- **Permission errors**: Ensure bot can send messages to your chat

Happy Trading! 🚀
