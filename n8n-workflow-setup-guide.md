# n8n Electricity Meter Workflow Setup Guide

This guide will help you set up the comprehensive n8n workflow that monitors your electricity meter and provides both automated daily reports and real-time Telegram bot interactions.

## Overview

The workflow provides:
- **Daily Automated Reports**: Sent at 9:00 AM every day
- **Interactive Telegram Bot**: Real-time usage queries with menu interface
- **Multiple Data Views**: Current usage, monthly reports, projections
- **Error Handling**: Comprehensive error management and user feedback

## Prerequisites

1. **n8n Instance**: Running n8n installation (cloud or self-hosted)
2. **Telegram Bot**: Created via BotFather on Telegram
3. **Python Script**: Your existing `auto_login_fetch_env.py` script
4. **Credentials**: RUVIE username and password

## Step 1: Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow instructions
3. Save the **Bot Token** for later use
4. Get your **Chat ID** by:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your `chat.id` in the response

## Step 2: Set Up n8n Credentials

### Telegram Bot Credentials
1. Go to n8n Settings → Credentials
2. Create new credential: **Telegram API**
3. Enter:
   - **Access Token**: Your bot token from BotFather
   - **Name**: `telegram-bot-credentials`

### RUVIE Credentials
1. Create new credential: **Generic Credential**
2. Enter:
   - **Name**: `ruvie`
   - **Username**: Your RUVIE username
   - **Password**: Your RUVIE password

### Telegram Chat Configuration
1. Create another credential: **Generic Credential**
2. Enter:
   - **Name**: `telegram`
   - **chatId**: Your Telegram chat ID (for daily reports)

## Step 3: Import the Workflow

1. Copy the content from `electricity-meter-workflow.json`
2. In n8n, go to **Workflows** → **Import from file**
3. Paste the JSON content and import

## Step 4: Configure Webhook URL

1. Find the **Telegram Webhook** node in the workflow
2. Copy the webhook URL (format: `https://your-n8n-domain/webhook/telegram-webhook`)
3. Set the webhook for your Telegram bot:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-n8n-domain/webhook/telegram-webhook"}'
   ```

## Step 5: Update File Paths

Update the Python script paths in these nodes if different:
- **Fetch Monthly Data**
- **Fetch Current Data** 
- **Fetch Monthly On-Demand**

Current path: `/Volumes/EXTSSD/Workspace/remote-check-meter/auto_login_fetch_env.py`

## Step 6: Test the Workflow

### Test Daily Report
1. Manually execute the **Daily 9AM Trigger** node
2. Check if you receive a Telegram message with usage data

### Test Bot Interactions
1. Message your bot with `/start`
2. Try the interactive buttons:
   - ⚡ Current Usage
   - 📊 Monthly Report
   - ℹ️ Help

## Bot Commands and Features

### Available Commands
- `/start` - Show welcome menu with interactive buttons
- `/usage` - Get current electricity usage
- `/help` - Show help information

### Interactive Buttons
- **⚡ Current Usage** - Real-time usage with today's data
- **📊 Monthly Report** - Complete monthly usage statistics
- **🔄 Refresh** - Update current data
- **🏠 Main Menu** - Return to main menu
- **ℹ️ Help** - Show help information

### Daily Report Features
- **Automated Timing**: Runs at 9:00 AM daily
- **Comprehensive Data**: Today's usage, monthly summary, trends
- **Error Handling**: Notifications if script fails

## Data Processing

The workflow handles both JSON and text output from your Python script:

### Expected JSON Format
```json
{
  "year": 2025,
  "month": 8,
  "data": [
    {
      "date": "2025-08-01",
      "daily_usage_kwh": 25.5,
      "cumulative_usage_kwh": 1234.5
    }
  ]
}
```

### Fallback Text Processing
If JSON parsing fails, the workflow looks for text patterns:
- `Total Usage: X kWh`
- `Daily Average: X kWh`
- `Cost: $X`

## Customization Options

### Modify Daily Report Time
Edit the **Daily 9AM Trigger** node:
- Change `cronExpression`: `"0 9 * * *"` (current: 9 AM)
- Format: `"minute hour day month day-of-week"`
- Example: `"0 8 * * *"` for 8 AM

### Customize Messages
Edit the text in any **Send** nodes to modify:
- Welcome messages
- Report formatting
- Error messages
- Help content

### Add New Bot Commands
1. Add new condition in **Check** nodes
2. Create corresponding processing logic
3. Add new response nodes

## Troubleshooting

### Bot Not Responding
1. Check webhook URL is correctly set
2. Verify bot token in credentials
3. Ensure workflow is active

### Daily Reports Not Sending
1. Check cron trigger is active
2. Verify Python script path is correct
3. Check RUVIE credentials
4. Review execution logs

### Python Script Errors
1. Ensure script has execution permissions
2. Check environment variables are set
3. Verify Python dependencies are installed
4. Test script manually with year/month parameters

### Data Processing Issues
1. Check Python script output format
2. Verify JSON structure matches expected format
3. Review data processing nodes for errors

## Security Considerations

1. **Credential Security**: Store all credentials securely in n8n
2. **Webhook Security**: Use HTTPS for webhook URLs
3. **Access Control**: Limit bot access to your chat ID only
4. **Script Security**: Ensure Python script is secure and up-to-date

## Advanced Features

### Error Recovery
- Automatic retry logic for failed script executions
- Fallback text parsing if JSON fails
- User-friendly error messages with retry options

### Performance Optimization
- `continueOnFail: true` for script execution nodes
- Efficient data processing with minimal API calls
- Responsive button interactions

### Monitoring
- Enable workflow execution logging
- Set up notifications for critical failures
- Monitor daily report delivery

## Support

If you encounter issues:

1. Check n8n execution logs for detailed error information
2. Test Python script independently
3. Verify all credentials are correctly configured
4. Ensure webhook URL is accessible from Telegram servers

## File Structure

```
/Volumes/EXTSSD/Workspace/remote-check-meter/
├── electricity-meter-workflow.json     # Main n8n workflow
├── n8n-workflow-setup-guide.md        # This setup guide
├── auto_login_fetch_env.py            # Your Python script
└── ... (other project files)
```

This comprehensive workflow provides a robust electricity monitoring solution with both automated reporting and interactive bot capabilities.