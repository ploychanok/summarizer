# Summarizer - Slack App Configuration Guide

**App Name:** Summarizer  
**Description:** Automatically summarize Slack conversations with AI-powered decision and action tracking

## Quick Setup Checklist

### 1. Create Slack App
- Go to [https://api.slack.com/apps](https://api.slack.com/apps)
- Click "Create New App" → "From scratch"
- **App Name:** `Summarizer`
- **Development Slack Workspace:** Choose your workspace
- Click "Create App"

### 2. Basic Information
- **App Name:** Summarizer
- **Short Description:** Automatically summarize Slack conversations with AI-powered decision and action tracking
- **Long Description:** Summarizer uses advanced AI to analyze your Slack discussions and generate structured summaries highlighting key decisions made, action items assigned, and questions that need follow-up - helping teams stay organized and accountable.
- **App Icon:** Upload your generated icon (512x512px PNG)
- **Background Color:** #4A154B (Slack purple) or your brand color

### 3. OAuth & Permissions
Navigate to "OAuth & Permissions" and add these **Bot Token Scopes**:

**Required Scopes:**
- `channels:history` - View messages in public channels
- `groups:history` - View messages in private channels  
- `chat:write` - Send messages as the bot
- `users:read` - View people in the workspace
- `channels:read` - View basic information about public channels
- `commands` - Add shortcuts and/or slash commands

**Optional (for enhanced features):**
- `im:history` - View messages in direct messages
- `mpim:history` - View messages in group direct messages

### 4. Slash Commands
Navigate to "Slash Commands" and create:

- **Command:** `/summarize`
- **Request URL:** *(Leave blank - using Socket Mode)*
- **Short Description:** Summarize Slack conversations
- **Usage Hint:** `thread <timestamp> | channel [N] | help`

### 5. Socket Mode (Recommended)
Navigate to "Socket Mode":
- **Enable Socket Mode:** Toggle ON
- Click "Generate Token" for app-level token
- **Token Name:** `summarizer-socket`
- **Scopes:** Select `connections:write`
- Copy the **App-Level Token** (starts with `xapp-`)

### 6. Event Subscriptions (Optional)
If you want to enable automatic triggers:
- **Enable Events:** Toggle ON
- **Subscribe to bot events:**
  - `message.channels` - Message posted to channel
  - `message.groups` - Message posted to private channel

### 7. Install App to Workspace
- Go to "Install App"
- Click "Install to Workspace"
- Authorize the permissions
- Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 8. App Home (Optional Customization)
- **App Display Name:** Summarizer
- **Default Username:** @summarizer
- **Always Show My Bot as Online:** Toggle ON

## Environment Variables Setup

Copy these tokens to your `.env` file:

```env
# From "OAuth & Permissions" → "Bot User OAuth Token"
SLACK_BOT_TOKEN=xoxb-your-bot-token-here

# From "Basic Information" → "Signing Secret"  
SLACK_SIGNING_SECRET=your-signing-secret-here

# From "Socket Mode" → App-level token
SLACK_APP_TOKEN=xapp-your-app-token-here

# Your OpenAI API key
OPENAI_API_KEY=your-openai-api-key-here
```

## Testing the Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Run the bot: `python src/main.py`
4. In Slack, try: `/summarize help`

## App Distribution (Optional)

If you want to distribute your app:

1. **App Directory Listing:**
   - Complete all required fields
   - Add screenshots of the bot in action
   - Submit for review

2. **Public Distribution:**
   - Set up proper hosting (Heroku, AWS, etc.)
   - Configure webhook URLs instead of Socket Mode
   - Add privacy policy and terms of service

## Icon Requirements

- **Size:** 512x512 pixels minimum
- **Format:** PNG with transparent background
- **Style:** Simple, recognizable at small sizes
- **Colors:** Professional, matches your brand

## Recommended App Store Assets

- **App Icon:** 512x512px
- **Screenshots:** Show the bot summarizing conversations
- **App Description:** Focus on time-saving and team productivity
- **Keywords:** summarize, productivity, AI, decisions, action items

## Support & Maintenance

- Monitor app usage in Slack App dashboard
- Update scopes if adding new features  
- Keep dependencies updated for security
- Monitor OpenAI API usage and costs