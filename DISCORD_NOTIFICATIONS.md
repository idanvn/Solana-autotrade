# Discord Notifications Setup 🔔

Get instant notifications in Discord when your bot executes trades!

## Features

- 🟢 **Buy Notifications**: Get alerts when SOL is purchased
- 🔴 **Sell Notifications**: Get alerts when SOL is sold
- 📊 **Trade Details**: See amount, price, profit/loss, and more
- 🎨 **Rich Embeds**: Beautiful formatted messages with colors

## Setup Instructions

### Step 1: Create Discord Webhook

1. Open your Discord server
2. Right-click on the channel where you want notifications
3. Select **Edit Channel** → **Integrations** → **Webhooks**
4. Click **New Webhook**
5. Give it a name (e.g., "SOL Trading Bot")
6. Copy the **Webhook URL**

### Step 2: Add Webhook to .env

Open your `.env` file and add:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

Replace with your actual webhook URL from Step 1.

### Step 3: Test the Connection

Run the test script to verify it works:

```bash
python scripts/test_discord_webhook.py
```

You should see "✅ Test notification sent successfully!" and a message in your Discord channel.

### Step 4: Run the Bot

Now when you run the trading bot, it will automatically send notifications:

```bash
python scripts/run_live_bot.py
```

## Notification Examples

### Buy Notification (Green)
```
🟢 BUY SIGNAL EXECUTED
Amount: 0.026809 SOL
Price: $186.50
Total Value: $5.00
Details: Price dropped 2.15% from $190.60
         Entry: $186.50
         Position size: $5.00 USDC
```

### Sell Notification (Red)
```
🔴 SELL SIGNAL EXECUTED
Amount: 0.026809 SOL
Price: $190.23
Total Value: $5.10
Details: Entry: $186.50
         Exit: $190.23
         Profit: +$0.10 (+2.00%)
         Received: $5.10 USDC
         Total P&L today: +$0.10
```

## Disable Notifications

To disable Discord notifications:

1. Remove or comment out the `DISCORD_WEBHOOK_URL` line in `.env`
2. Or set it to an empty value: `DISCORD_WEBHOOK_URL=`

The bot will continue to work normally without sending notifications.

## Security Notes

⚠️ **Keep your webhook URL private!**
- Don't commit `.env` to Git (it's in `.gitignore`)
- Don't share your webhook URL publicly
- Anyone with the URL can send messages to your channel

## Troubleshooting

### "No webhook URL configured"
- Make sure `DISCORD_WEBHOOK_URL` is set in your `.env` file
- Check that the URL starts with `https://discord.com/api/webhooks/`

### "Failed to send notification"
- Verify the webhook URL is correct
- Check your internet connection
- Make sure the webhook hasn't been deleted in Discord

### Notifications not appearing
- Check you're looking at the correct Discord channel
- Verify the webhook is enabled in Discord settings
- Run `test_discord_webhook.py` to test the connection

## Advanced Configuration

The notifications are sent from these functions in `scripts/run_live_bot.py`:
- `execute_buy()` - Called when buying SOL
- `execute_sell()` - Called when selling SOL

You can customize the notification format by editing the `send_discord_notification()` function.

## Next Steps

- ✅ Test the webhook connection
- ✅ Run the bot and wait for trade signals
- 📱 Keep Discord open to see real-time notifications
- 📊 Monitor your trading performance

Happy trading! 🚀
