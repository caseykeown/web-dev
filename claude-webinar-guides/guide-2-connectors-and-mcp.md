# Guide 2: Connecting Claude to Your World

*Connectors, MCP, and how to stop copying and pasting forever.*

---

## Welcome!

Out of the box, Claude is brilliant but sealed off. It knows an enormous amount about the world in general, and nothing at all about *your* world: your files, your calendar, your team's messages.

**Connectors** fix that. This guide explains what they are, how to turn them on, and what they'll save you. You will not need to write a single line of code.

---

## Part 1: What Are Connectors and MCP?

### The Simple Version

A **Connector** is a secure bridge between Claude and an app you already use, such as Google Drive, Slack, or GitHub. Once connected, you can ask Claude to look things up in that app and act on what it finds, right inside your normal conversation.

Before a connector:

> "Here, let me find that spreadsheet, download it, and upload it to you. Hang on."

After a connector:

> "Claude, pull up the Q3 budget from my Drive and tell me where we overspent."

### So What Is MCP?

**MCP** stands for **Model Context Protocol**. It's the open standard, created by Anthropic, that makes connectors possible.

Here's the analogy that makes it click:

> **MCP is the USB-C port of AI.**
>
> Before USB-C, every device needed its own weird proprietary cable. Before MCP, every AI tool needed custom one-off code to talk to every app. MCP created one standard shape that everybody can build to. Any app that speaks MCP can plug into Claude, and any AI that speaks MCP can use those apps.

**Three things beginners should know about MCP:**

1. **It's a standard, not a product.** You don't "buy MCP" or install it by itself. You just benefit from it every time you add a connector.
2. **It's open.** Anthropic published it for anyone to use, so the library of available connectors keeps growing, built by both companies and independent developers.
3. **You stay in control.** Connecting an app requires you to sign in and approve access. Claude only sees what you allow, and you can disconnect at any time.

### A Note on Vocabulary

You'll hear a few overlapping terms. Don't let them trip you up:

| Term | What it means for you |
|---|---|
| **Connector** | The friendly, click-to-add integration in the Claude interface |
| **MCP server** | The technical name for the thing a connector talks to |
| **Remote connector** | Lives in the cloud, connects with a sign-in, and works on web and mobile |
| **Local connector** | Runs on your own computer through the desktop app, useful for local files and tools |

For everyday use, "connector" is the only word you need.

---

## Part 2: How to Add a Connector, Step by Step

*Interfaces evolve, so menu labels may shift slightly. The flow stays the same.*

### Adding a Connector

1. **Open your settings.** In Claude (web or desktop), click your name or profile icon, then go to **Settings**.
2. **Find the Connectors section.** Look for **Connectors** in the settings menu.
3. **Browse what's available.** You'll see a directory of ready-made connectors, including Google Drive, Slack, GitHub, Canva, Notion, Asana, and many more.
4. **Click Connect** next to the one you want.
5. **Sign in to that app.** A window opens asking you to log in to your Google, Slack, or GitHub account. This happens on *their* site, not Claude's, so your password is never shared with Anthropic.
6. **Review the permissions.** The screen tells you exactly what Claude will be able to see or do. Read it, then approve it.
7. **You're done.** The connector now shows as connected in your settings.

### Turning It On in a Conversation

Once connected, look for the **tools or attachment icon** near the chat box. Your connected apps appear there, and you can toggle which ones are active for the conversation you're in.

### A Few Practical Notes

* **Some connectors need an admin.** In a workplace Google Workspace or Slack, your IT administrator may have to approve the integration before you can connect. If a connection fails, that's usually why. It is not something you broke.
* **Availability varies by plan.** Certain connectors are limited to specific Claude plans, and organization-wide connectors are typically set up by an admin for everyone at once.
* **Disconnecting is easy.** Return to **Settings**, then **Connectors**, and remove any connector at any time. For extra peace of mind, you can also revoke Claude's access from inside the other app's own security settings.

---

## Part 3: How Claude Suggests Connected Apps

Here's the part that delights new users: **you usually don't have to tell Claude which app to use.**

Once a connector is active, Claude reads your request, notices that answering it requires outside information, and offers to reach for the right app.

**What this looks like in practice:**

You type:

> "What did the team decide about the truck maintenance schedule?"

Claude recognizes that the answer lives in your messages, not in its own knowledge, and responds along the lines of:

> "I can search your Slack for that. Would you like me to?"

You approve, Claude searches, and you get a real answer with sources.

**How to make suggestions better:**

* **Mention the app by name when you want certainty.** "Search my Google Drive for the insurance policy" removes all ambiguity.
* **Keep only relevant connectors switched on.** If ten apps are active, Claude has more to sift through. Toggle off what you're not using today.
* **Expect a permission prompt.** Claude asks before taking meaningful actions, especially anything that writes, sends, or changes data. Approving each time is a feature, not a nuisance.

---

## Part 4: Three Ways Connectors Save Beginners Real Time

### Example 1: The Document You Can't Find (Google Drive)

**Before:** You search Drive by half-remembered filename, open four wrong documents, finally find the right one, skim eleven pages for the number you need.

**After:** You ask, "Find the vendor contract with Ridgeline in my Drive and tell me the payment terms and the renewal date."

**Time saved:** Roughly fifteen minutes of hunting, every single time. Claude searches, reads, and answers in one step.

---

### Example 2: The Meeting You Missed (Slack)

**Before:** You scroll back through three days of messages across five channels, trying to reconstruct what was decided and what's now yours to do.

**After:** You ask, "Summarize what happened in the #operations channel this week and list anything assigned to me."

**Time saved:** A half hour of scrolling, plus the anxiety of wondering what you missed. This is the single best Monday-morning habit you can build.

---

### Example 3: The Code You Don't Speak (GitHub)

**Before:** As a non-developer, you open a GitHub page, see a wall of technical changes, and have to interrupt an engineer to ask what it means.

**After:** You ask, "Look at the open pull requests in our website repository and explain in plain English what each one changes."

**Time saved:** An entire back-and-forth with your technical team. You show up to the meeting already understanding what's happening.

---

## Pro-Tip

**Start with exactly one connector and use it for a full week.**

The temptation is to connect everything on day one, which usually ends with ten integrations you forgot you turned on. Instead, pick the app where your information actually lives (for most people that's Google Drive or Slack), connect only that, and get into the habit of asking Claude first before you go searching yourself.

Once reaching for Claude becomes automatic, add the next one. Your connector list should grow because you needed it to, not because the directory looked exciting.
