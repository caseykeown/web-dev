# Guide 3: The Beginner's Guide to the Claude API

*What an API key is, how to get one, and how to keep it safe.*

---

## Welcome!

The word "API" makes a lot of people freeze up. It shouldn't. You do not need to be a programmer to understand this guide, and you may already need an API key without realizing it.

By the end of this page you'll know what a key is, how to create one, and the handful of security habits that keep you out of trouble.

---

## Part 1: What Is an API Key, Really?

### The Analogy

Imagine Claude has two entrances.

**The front door** is claude.ai. You walk up, log in with your email and password, and talk to Claude yourself. Friendly, visual, human.

**The service entrance** is the API. This is the door that *other software* uses to talk to Claude on your behalf. No login screen, no chat window, just one program handing a request to another program.

An **API key** is the badge that opens the service entrance. It's a long string of characters that says, "the software carrying this badge is authorized, and whoever owns it pays for what it uses."

### API in Plain English

API stands for **Application Programming Interface**. It's simply an agreed-upon way for two pieces of software to talk to each other. Your weather app uses an API to fetch a forecast. A checkout page uses one to charge your card. Nothing mystical.

### Why Would a Beginner Need One?

You're not writing software, so why does this matter? Because a growing number of tools are "bring your own key." They give you the interface and ask you to supply the Claude access. Common situations:

* **A writing, research, or note-taking app** that offers AI features and asks you to paste in a Claude API key.
* **An automation platform** such as Zapier or Make, where you build a workflow that sends text to Claude and does something with the reply.
* **A spreadsheet plugin or browser extension** that adds AI capability to a tool you already use.
* **A developer you hired** building something custom for your business, who needs a key billed to your account rather than theirs.

### Two Things That Surprise People

1. **The API is billed separately from your Claude.ai subscription.** A Pro or Max plan covers the chat interface. API usage is its own account with its own prepaid credits. Having one does not give you the other.
2. **You pay per use, not per month.** API pricing is based on the amount of text processed, measured in units called tokens. Light experimentation costs very little, often just a few dollars, but the meter is genuinely running, which is exactly why key security matters so much.

---

## Part 2: How to Generate an API Key

### Before You Start

You'll need an Anthropic Console account, which is separate from your Claude.ai login even if you use the same email address.

### Step by Step

1. **Go to the Console.** Visit **console.anthropic.com** in your browser.
2. **Sign in or sign up.** Create an account if this is your first visit, then verify your email.
3. **Add billing.** Find **Billing** or **Plans & Billing** in the settings menu and purchase credits. The API requires prepaid credits before it will process any requests, so a brand-new key with no credits behind it will simply return an error.
4. **Open the API Keys page.** In **Settings**, click **API Keys**.
5. **Click "Create Key."**
6. **Name it descriptively.** Use something you'll recognize in six months, such as "Zapier automation" or "Sarah's writing app." Vague names like "test" become a real problem once you have five keys and can't remember which app depends on which.
7. **Copy the key immediately.** It begins with `sk-ant-` followed by a long string of characters.

> ### Read This Before You Close the Window
>
> **You will only see the full key once.** The moment you close that dialog, Anthropic will never show it to you again. This is deliberate, and it is a security feature, not an inconvenience.
>
> Paste it somewhere safe *right now*: a password manager is ideal, or paste it directly into the app that needs it.
>
> Lost it? Nothing is broken. Delete that key and create a new one. It takes twenty seconds.

### Helpful Extras in the Console

* **Spend limits.** Set a monthly cap so an accident or a runaway script can never produce a shocking bill. Do this on day one.
* **Usage dashboard.** See exactly what you're spending and which key is spending it.
* **Workspaces.** Separate keys and budgets by project or client, so one experiment can't drain another project's funds.

---

## Part 3: Keeping Your Key Safe

Treat your API key exactly like a credit card number. Anyone who has it can spend your money, and the charges are entirely legitimate from Anthropic's point of view, because the request carried your valid badge.

### The Golden Rules

**Never post it publicly.** Not in a screenshot, not in a support forum, not in a Slack message to a coworker, not in a YouTube tutorial. Automated bots continuously scan public places for exposed keys, and they find them within minutes.

**Never put it directly in your code.** Writing `api_key = "sk-ant-abc123..."` inside a file is the single most common way keys leak, because that file eventually gets shared, backed up, or uploaded to GitHub.

**Never put it in anything a browser downloads.** Any key inside a website's front-end code is visible to every visitor who opens developer tools. Requests to Claude belong on a server you control, not in the browser.

**Never share one key across people.** If a contractor needs access, create a key just for them. When the project ends, delete that key and nothing else is disrupted.

### The Right Way: Environment Variables

An **environment variable** is a value stored in your computer's or server's settings rather than inside your files. Your program reads it at run time. The key exists on the machine, but never in the code.

**On Mac or Linux,** in the Terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**On Windows,** in PowerShell:

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

To make it permanent rather than lasting only for that terminal session, add it to your shell profile (`~/.zshrc` or `~/.bashrc` on Mac and Linux) or set it through System Properties on Windows.

**Using a `.env` file?** Many tools support a small file named `.env` holding lines like `ANTHROPIC_API_KEY=sk-ant-...`. This is fine, with one non-negotiable condition:

```
# Add this line to your .gitignore file
.env
```

Without that, your key travels to GitHub with your next commit. Add `.env` to `.gitignore` *before* you create the `.env` file, not after.

### If You're Just Pasting It Into an App

Most beginners never touch a terminal. If a trusted app asks for your key in a settings field, pasting it there is fine. Just check three things first:

1. **The app is reputable.** You're handing over spending power. Research unfamiliar tools before trusting them.
2. **The connection is secure.** The address starts with `https://`.
3. **You can revoke it.** Which you always can, from the Console.

### If a Key Is Ever Exposed

Don't panic, and don't wait. Go to **console.anthropic.com**, open **API Keys**, and **delete the exposed key immediately**. It stops working instantly. Then create a new one and update whichever app was using it. The whole recovery takes about a minute, and acting fast is what keeps a scare from becoming a bill.

---

## Pro-Tip

**Set a spend limit before you create your first key.**

New API users often skip this and then lie awake wondering what a misconfigured automation might be doing at 3 a.m. A monthly cap of ten or twenty dollars is plenty for learning, and it turns the worst realistic outcome from "an alarming invoice" into "an error message and a lesson."

You can raise the limit anytime. You cannot un-spend money.
