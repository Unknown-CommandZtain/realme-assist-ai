# 🤖 Realme Assist AI v2.0

**A community-powered Telegram assistant for Realme devices, Android, and everyday technology troubleshooting.**

Realme Assist AI combines Google Gemini-powered chat, Telegram photo analysis, RMX device-code lookups, and a collection of ready-made Realme support commands. Version 2.0 runs as a **JavaScript Cloudflare Worker**, receives updates through a **Telegram webhook**, and uses **Cloudflare D1 (SQLite)** to store settings, short-term conversations, job status, and moderation records.

> [!IMPORTANT]
> **Unofficial community project.** Realme Assist AI v2.0 is not developed, sponsored, or endorsed by Realme. AI can make mistakes, and legacy support templates may include information that has changed. Verify firmware, product, and safety-critical guidance with official sources.

**Status:** v2.0 release implementation  
**Source repository:** [Unknown-CommandZtain/realme-assist-ai](https://github.com/Unknown-CommandZtain/realme-assist-ai)  

## ✨ Features

- **🧠 Technology-focused AI:** Uses Google Gemini to answer questions about smartphones, Android, Realme UI, programming, and general IT troubleshooting. An instruction asks the model to decline unrelated requests; this is guidance, not a guaranteed topic filter.
- **📷 Photo troubleshooting:** Analyzes Telegram photo messages and their captions, subject to the Worker's photo-size and API limits. It does not process arbitrary document attachments as images.
- **💬 Public private-chat access:** Anyone can message the bot privately for supported public features.
- **🤫 Selective group responses:** In enabled groups, AI typically responds to a direct `@mention` or a reply to the bot. Supported slash commands and RMX codes are handled separately.
- **🔎 RMX model lookup:** `/lookup RMX1234`, or a recognized `RMX1234` code in a delivered message, searches for a Realme model using SerpApi. Results are cached for 24 hours.
- **🧵 Short-term AI memory:** Keeps up to six recent AI exchanges per conversation scope for up to 24 hours. Group memories are separated by chat, user, and topic; users can opt out or clear their history.
- **🌏 Language preferences:** Automatic language matching or a choice of English, Malay, Hindi, Indonesian, Chinese, Tamil, and Arabic.
- **👑 Owner-only controls:** The Telegram user ID configured as `ADMIN_ID` controls group activation, bot settings, moderation commands, custom command menus, a shared `/banana` image, and polls.
- **🛡️ Group moderation:** Owner commands to warn, remove warnings, inspect a user, ban, and unban. Warnings do not automatically trigger bans.
- **📊 Persistent quotas:** Daily AI and RMX-search caps, enforced globally, per user, and per chat, plus an eight-second per-user interval between attempts of the same API type.
- **📬 Reliable job handling:** Database-backed message processing with retry scheduling for temporary errors and a recurring maintenance process.
- **🧹 Optional group auto-deletion:** Configurable deletion of supported bot replies and their triggering messages, subject to Telegram permissions and scheduled processing.
- **📚 Legacy support library:** 27 instant-response commands covering troubleshooting, Android releases, optimization, community rules, and other commonly asked questions.

## 🧰 Technology stack

| Component | Implementation |
| --- | --- |
| Runtime / programming language | JavaScript ES module on Cloudflare Workers |
| Telegram integration | Telegram Bot API over HTTPS using a webhook |
| AI | Google Gemini REST API (`generateContent`) |
| Default AI model | `gemini-3.5-flash-lite`, configurable with `GEMINI_MODEL` |
| Image analysis | Telegram photo download and Gemini inline image input |
| Model-code search | SerpApi Google Search results |
| Database | Cloudflare D1 (SQLite) |
| Background execution | Cloudflare Worker `ctx.waitUntil()` and Cron Triggers |
| Configuration | Worker secrets, text variables, and D1 binding |

**No Python runtime, `python-telegram-bot`, PostgreSQL, APScheduler, or Railway service is required for this version.** Those belong to the original implementation.

## 🚀 Deployment on Cloudflare Workers

(BELOW IS THE STEPS IF YOU WANT TO SET UP A BOT SIMILARLY LIKE WHAT I DO)

The supplied v2.0 implementation is a single JavaScript Worker module, represented in the uploaded `worker.txt`. Add the script to a Cloudflare Worker (or save it as your project's Worker entry file, such as `src/index.js`). The filename in your repository can differ, but it must be deployed as JavaScript.

### 1. Prepare your Telegram bot

1. Create or manage a bot with [@BotFather](https://t.me/BotFather).
2. Obtain its bot token and your **numeric** personal Telegram user ID.
3. **Stop the previous host such as Railway bot** before switching to the webhook. Do not run the old long-polling implementation against the same Telegram bot at the same time.
4. If credentials were ever exposed, rotate them before deployment.

### 2. Create the Worker and D1 database

1. In the [Cloudflare dashboard](https://dash.cloudflare.com/), create a Worker and deploy the v2.0 JavaScript source.
2. Create a **D1 database** for Realme Assist AI as example.
3. Bind the D1 database to the Worker using the exact variable name **`DB`** (uppercase).
4. Confirm the deployment has a public HTTPS Worker URL.
5. In the source code, set `ORIGIN` to that exact deployed origin, **without a trailing slash**, and deploy again if it differs from the URL already in the code.

If you use a different Worker URL or custom domain, update this constant. The `/setup` route and Telegram webhook registration depend on it.

### 3. Configure secrets and variables

Configure the following in your Worker's settings. Treat credentials as secrets, not source-code constants.

| Name | Type | Required? | Purpose |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Secret | Yes | Telegram Bot API authentication |
| `WEBHOOK_SECRET` | Secret | Yes | Protects the webhook and authorizes setup actions |
| `GEMINI_API_KEY` | Secret | For AI features | Authenticates Google Gemini requests |
| `SERPAPI_KEY` | Secret | For RMX searches | Enables online Realme model-code lookup |
| `ADMIN_ID` | Text variable | Yes | Numeric Telegram user ID of the sole bot owner |
| `ALLOWED_GROUP_IDS` | Text variable | No | Comma- or whitespace-separated initial group IDs, usually negative numbers |
| `GEMINI_MODEL` | Text variable | No | Overrides the default model name |


`WEBHOOK_SECRET` must be **32–256 characters**, using only letters, numbers, `_`, or `-`. Use a randomly generated value. `ADMIN_ID` must contain the owner's numeric personal Telegram ID, with no extra quotation marks.

The Worker validates the bot token's presence, webhook secret format, owner ID format, and D1 binding at setup. If the Gemini or SerpApi keys are missing, the Worker can still initialize, but those corresponding features will be unavailable.

> [!CAUTION]
> Never publish tokens, API keys, or your webhook secret in GitHub, screenshots, or shared setup logs. Rotate exposed credentials and redeploy. The bot does **not** ask users to type an admin key in Telegram: ownership is checked against `ADMIN_ID` on every owner-only command.

The once-per-minute schedule runs maintenance for delayed job retries, scheduled message deletion, and periodic cleanup. The Worker may process only a limited number of queued items per invocation; actual deletion and retry times can be later than their requested due times.

### 5. Initialize and connect Telegram

Open the setup page at:

**<https://your.workers.dev/setup>**

For a deployment at another origin, use `https://YOUR-WORKER-ORIGIN/setup` instead.

1. Enter the **`WEBHOOK_SECRET`**, **not** the Telegram bot token.
2. Select **Initialize and connect**.
3. The Worker creates its D1 tables and registers `/webhook` with Telegram.
4. Use **Check status** to review the webhook URL, pending updates, delivery error timestamp, and latest maintenance run.
5. Test `/start` and `/help` in a private chat. From the account matching `ADMIN_ID`, test `/admin` and `/settings`.

The setup page registers Telegram's `message` update type, not all Telegram update types. Setup is designed to be run again, but it does **not** import existing host (e.g Railway) data.

### 6. Enable a group

Groups are **disabled by default** unless their IDs have been preloaded through `ALLOWED_GROUP_IDS` during initialization or an owner has enabled them.

1. Add the bot to the group.
2. From the Telegram account matching `ADMIN_ID`, send `/chatid` to identify the group.
3. Send `/enablegroup` inside that group.
4. Try `/help`, mention the bot in a tech question, or reply to one of its messages.
5. For bans and automated deletions, grant the necessary Telegram administrator permissions to the bot.

`/disablegroup` turns off processing for that group. Commands from an anonymous group administrator or messages sent on behalf of a chat do not authenticate as the configured owner. Telegram's group privacy mode can also affect which ordinary group messages, including unmentioned RMX codes, are delivered to the bot.

## 💬 How the bot responds

**Private chats:** Anyone may use `/start`, `/help`, tech-related AI questions, photo questions, RMX lookups, personal memory/language settings, and other public commands. Owner commands remain restricted.

**Enabled group chats:** The bot responds to supported slash commands, direct mentions, or replies to its own messages. It can also detect an RMX code in messages Telegram delivers to it, without requiring a mention. AI conversation memory is isolated per **group + user + topic**, preventing a member's saved chat history from being included in another member's prompt.

**Disabled group chats:** Ordinary activity is ignored. The configured owner can still use the supported management commands needed to inspect or enable the group.

The bot's AI is instructed to focus on technology and keep responses concise. It has **no general live-browsing capability**; RMX code lookup is a separate search feature.

## 📖 Public commands

| Command | Description |
| --- | --- |
| `/start` | Welcome message and quick instructions |
| `/help` | Show available bot commands |
| `/lookup RMX1234` | Search for a Realme device by RMX code |
| `/forget` or `/new` | Clear the current conversation's saved AI history |
| `/memory on` / `/memory off` | Enable or disable your personal AI memory; disabling also clears your saved history |
| `/set language auto` | Match the user's language automatically |
| `/set language en\|ms\|hi\|id\|zh\|ta\|ar` | Set a supported language preference |
| `/usage` | View your API attempt counts for the current Malaysia-time day |
| `/privacy` | Read a description of data sent to providers and stored in D1 |
| `/banana` | Send the saved community banana image, or a fallback message |
| `/whatsapp` | Show the original bot's support contact |
| `/polls` | Explain how owner-created Telegram polls work |

For `/language`, use **one** value, such as `/language ms` or `/language en`.

### 📚 Built-in Realme support commands

These 27 legacy commands return predefined support text. They do **not** request a new Gemini response.

| Category | Commands | Topics |
| --- | --- | --- |
| Getting started and community | `/about`, `/ask`, `/rules`, `/form` | Bot information, asking for help, group rules, bug reports |
| Android releases and software | `/android16`, `/eol`, `/miss`, `/push`, `/stable`, `/manual` | Realme UI/Android information, update phases, end-of-life guidance, system app updates |
| Troubleshooting and maintenance | `/apk`, `/bug`, `/fooview`, `/debloat`, `/cleaners` | Installation issues, bug reports, broken system apps, removing unwanted apps, storage cleaning |
| Battery, hardware, and performance | `/aod`, `/battery`, `/charge`, `/benchmark`, `/fps`, `/ram`, `/swap` | Display, batteries, charging, benchmarks, gaming, memory |
| Apps and photography | `/cool`, `/gcam` | Useful applications and Google Camera ports |
| Updates and community commentary | `/rant`, `/realistic`, `/rumor` | Update expectations, rumors, developer commentary |

**Content notice:** These are legacy templates carried into v2.0. Some include changing update timelines, device-specific assumptions, external links, or third-party app suggestions. They have **not** been independently re-verified for this release.

## 🚦 AI and RMX-search limits

The following limits are defined in the uploaded v2.0 Worker source. They are **application-level settings**, not published quotas from Google or Cloudflare.

| Limit | Gemini AI attempts | RMX search attempts |
| --- | ---: | ---: |
| Global, all chats combined, per day | 100 | 30 |
| Per user, per day | 20 | 5 |
| Per chat, per day | 40 | 15 |
| Minimum interval per user and service | 8 seconds | 8 seconds |

- Limits reset at **midnight Malaysia time (UTC+8)**.
- A failed **admitted** API attempt can still count toward a limit.
- A cached RMX result is returned without starting a fresh SerpApi search.
- Users can run `/usage`; the owner receives aggregate counts for the day.
- Values can be changed in the Worker's `LIMITS` object and redeployed.

## 🧠 Privacy, memory, and data retention

The Worker stores only the data needed for its supported operations, although temporary processing records may include the text or Telegram photo metadata supplied with a message.

| Data | How it is used / retained |
| --- | --- |
| Current AI question and optional photo bytes | Sent to Google Gemini to answer the request; photo bytes are not saved in D1 as images |
| AI conversation history | Up to six exchanges per conversation scope, eligible for reuse for up to 24 hours |
| Preferences and chat settings | Saved in D1 until changed or removed |
| Queued messages and jobs | Held for processing; completed job payload and answer are cleared; old completed/dead job records are periodically removed after seven days |
| API usage records | Used for quotas; records older than two days are periodically deleted |
| RMX lookup cache | Saved for 24 hours before expiration |
| Warning records | Stored in D1 for group moderation |
| Auto-delete schedule | Stores pending Telegram message IDs and due times |

The Worker may send **up to six recent exchanges from the same conversation scope** to Gemini with a new prompt. `/forget` clears that scope. `/memory off` disables your saved AI memory and attempts to clear your saved history across scopes. The `/privacy` command explains this in the bot.

Expired history is filtered out of prompts even before scheduled cleanup executes. Physical database cleanup depends on the Cron Trigger running. **External providers' own retention and privacy policies also apply.**

## 🗃️ D1 database structure

The setup routine creates these tables automatically:

| Table | Purpose |
| --- | --- |
| `ra_meta` | Schema version, maintenance timestamp, and shared banana photo reference |
| `ra_chats` | Per-chat enablement and feature settings |
| `ra_prefs` | Per-user memory and language preferences |
| `ra_jobs` | Persistent processing queue, retry state, and results awaiting delivery |
| `ra_history` | Recent per-conversation AI questions and responses |
| `ra_usage` | AI/search attempt counts and cooldown tracking |
| `ra_warnings` | Group warning adjustments |
| `ra_cache` | Cached RMX search results |
| `ra_deletes` | Scheduled Telegram message deletions |

The current schema version is recorded as `2.0`. D1 is an entirely separate SQLite database from the original Railway PostgreSQL database.

## 🔁 Processing and maintenance

1. Telegram sends a `message` update to `/webhook` over HTTPS.
2. The Worker checks the `X-Telegram-Bot-Api-Secret-Token` header, validates the update, and applies chat filters.
3. Accepted updates are written to `ra_jobs`, keyed by Telegram `update_id` to avoid duplicate queue entries.
4. The Worker tries processing promptly using `ctx.waitUntil()`.
5. Temporary processing or delivery failures can be retried from the persistent queue with increasing delays. Jobs stop retrying after the configured attempt cap.
6. The minute-level Cron Trigger processes due work, handles a small batch of scheduled deletions, and periodically removes expired records.

This design reduces the risk of losing accepted work during transient errors, but **does not guarantee delivery** during prolonged outages, quota exhaustion, or configuration failures.

## 🧭 Changes from the original bot

| Earlier implementation | Version 2.0 |
| --- | --- |
| Python / `python-telegram-bot` v13 | JavaScript Cloudflare Worker |
| Railway service | Cloudflare Workers |
| Long-polling Telegram updates | Telegram webhook with secret-token check |
| PostgreSQL persistence | D1 SQLite persistence |
| Original Python modules (`main.py`, `messages/`, etc.) | Worker script containing routing, AI, commands, D1 schema, and maintenance |
| Previous retry approach | D1-backed processing jobs, bounded retries, and Cron recovery |
| Restricted initial bot testing | Public private chats, with numeric-ID-restricted owner controls |

## 🤝 Contributing and support

Bug reports, corrections to legacy support templates, and suggestions are welcome through the [project repository](https://github.com/Unknown-CommandZtain/realme-assist-ai). The bot also exposes `/about`, `/form`, and `/whatsapp` for existing community information and contact paths.

For device update eligibility, software rollout dates, and repair advice, consult official Realme sources as appropriate.

---
