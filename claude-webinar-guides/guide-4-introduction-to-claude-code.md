# Guide 4: Introduction to Claude Code

*Claude, living in your terminal, with its sleeves rolled up.*

---

## Welcome!

This is the guide people expect to be scary. It isn't, and you're allowed to be curious about it even if you've never written a line of code.

Claude Code is Anthropic's **agentic coding tool**. Let's unpack that phrase, get it installed, and give you a handful of commands that make it genuinely useful.

---

## Part 1: What Is Claude Code?

### The Short Version

Claude Code is Claude running in your **terminal**, the plain text window where you type commands to your computer. Unlike the chat interface, Claude Code can see the files in a folder on your machine and actually change them, with your approval at each step.

### What "Agentic" Means

In the chat interface, Claude answers. Claude Code **acts**.

Give it a goal in ordinary English, and it will work out the steps, read the files it needs, make edits, run commands, check whether things worked, and fix what didn't. It's the difference between an advisor who tells you what to do and a collaborator who does it while you watch.

> **The analogy:** Chat Claude is a consultant on a phone call. Claude Code is a contractor standing in your house, who asks before knocking down any walls.

### Where It Fits

| | Claude.ai | Claude Code |
|---|---|---|
| Lives in | Browser or app | Terminal |
| Sees your files | Only what you upload | Every file in the folder you open |
| Changes your files | No | Yes, with permission |
| Runs commands | No | Yes, with permission |
| Best for | Thinking, writing, learning | Building, editing, and automating real work |

### The Honest Caveat

Claude Code is built for people working with code. If you never touch a project folder, the chat interface is probably your home. But plenty of non-developers get real value from it, and Part 4 is written for exactly those readers.

---

## Part 2: Installation and Setup

### What You Need First

* **A terminal.** Use **Terminal** on Mac (find it with Spotlight), or **PowerShell** or **Windows Terminal** on Windows.
* **Node.js version 18 or newer.** This is the runtime the npm installation method uses.

**Check whether you already have Node.js** by typing this and pressing Enter:

```bash
node --version
```

If you see something like `v20.11.0`, you're set. If you see "command not found," download the LTS version from **nodejs.org**, install it, then close and reopen your terminal.

### Step 1: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

The `-g` means "global," so the `claude` command works from any folder. Installation takes a minute or two.

> **On Mac or Linux,** if that command fails with a permissions error, do **not** rerun it with `sudo`. Installing global npm packages as an administrator causes more problems than it solves. Anthropic also publishes a native installer that sidesteps Node.js entirely:
>
> ```bash
> curl -fsSL https://claude.ai/install.sh | bash
> ```

**Confirm it worked:**

```bash
claude --version
```

### Step 2: Open a Project

Claude Code works inside whichever folder you're currently in, so navigate there first using `cd` ("change directory"):

```bash
cd ~/Documents/my-project
claude
```

That's it. Just `claude`, on its own.

> **A small but useful correction:** you'll sometimes see this written as `claude .` by analogy with editors like VS Code, where the dot means "this folder." Claude Code doesn't need it. Anything you type after `claude` is treated as your opening message, so `claude .` just sends Claude a lonely period. The pattern is: `cd` into the folder, then run `claude`.
>
> You *can* pass a real prompt this way, which is handy: `claude "explain what this project does"`.

### Step 3: Authenticate

The first time you run `claude`, it walks you through signing in. You'll pick one of two options:

1. **Your Claude subscription (Pro or Max).** Usage comes out of your existing plan. This is the simplest choice for most people, and often the most economical.
2. **An Anthropic Console account.** Usage is billed as API credits, using the key setup covered in Guide 3.

Your browser opens, you approve the login, and you return to the terminal ready to work. You only do this once. Later on, `/login` and `/logout` let you switch accounts.

---

## Part 3: Basic Commands

### Getting Around

| Type this | What happens |
|---|---|
| `claude` | Start Claude Code in the current folder |
| `claude "your question"` | Start with an opening prompt already asked |
| `claude -c` | Continue your most recent conversation |
| `claude -p "your question"` | Get one answer and exit, without the interactive session |
| `claude --version` | Check which version you have |

### Slash Commands (Inside a Session)

| Command | What it does |
|---|---|
| `/help` | List every available command |
| `/init` | Study the project and write a `CLAUDE.md` file describing it, so future sessions start informed |
| `/clear` | Wipe the conversation and start fresh, useful when changing topics |
| `/model` | Switch which Claude model you're using |
| `/cost` | See what the session has used so far |
| `/login`, `/logout` | Change accounts |
| `/exit` | Leave |

### Handy Keys and Symbols

* **Esc** interrupts Claude mid-task. Use it freely. Nothing breaks.
* **`@`** references a specific file, as in "explain @index.html to me."
* **`#`** saves a note to project memory, as in "# always use two-space indentation."
* **Ctrl + C**, pressed twice, force-quits.

### The Permission System

Claude Code asks before it edits a file or runs a command. Each prompt offers roughly:

* **Yes**, do it once.
* **Yes, and don't ask again** for this kind of action.
* **No**, and here's what to do instead.

Say yes deliberately while you're learning. The prompts are your steering wheel, and reading them is how you build an accurate sense of what the tool actually does.

---

## Part 4: For Non-Developers

You are allowed to be here. Some of the most useful things Claude Code does involve no programming at all.

### Try These First

**Understand something instead of changing it.** Open any project folder and ask:

> "Explain what this project does, in plain English, as if I have no technical background."

Nothing is modified. You just get a tour. This is the single best first exercise, and it works on a codebase you inherited, a repository a contractor handed over, or a template you downloaded.

**Ask the questions you're embarrassed to ask a person.**

> "What is this file for?"
> "Where does the contact form on our site send its submissions?"
> "Is there anything here that looks broken or out of date?"

Claude Code has infinite patience and no memory of you asking something basic yesterday.

**Make small, contained edits.**

> "Change the phone number on the contact page to 555-0142, everywhere it appears."

This is genuinely useful work, and it's the kind of task that used to require a whole email thread with somebody else.

### Four Habits That Keep You Safe

1. **Use version control.** If your project is a git repository, every change is reversible. If it isn't, copy the folder before you start. This one habit turns mistakes into non-events.
2. **Read the permission prompts.** They tell you precisely what's about to happen. Skimming them is the only real way to get into trouble.
3. **Start small.** "Fix the typo on the homepage" teaches you more than "redesign the site," and it teaches it faster.
4. **Ask it to explain first, act second.** "Tell me how you'd approach this before you change anything" is a completely valid instruction, and an excellent one.

### What This Teaches You About AI Assistants Generally

Watching Claude Code work is the clearest window into how AI agents actually operate. You see it read a file, form a plan, try something, notice the result, and adjust. There's no magic in there, just a fast, tireless, occasionally wrong collaborator that shows its work. Ten minutes of watching that loop will teach you more about AI than an hour of reading about it.

---

## Pro-Tip

**Run `/init` the first time you open any project.**

Claude Code explores the folder and writes a `CLAUDE.md` file summarizing what the project is, how it's organized, and how to work with it. Every future session reads that file automatically and starts up already oriented.

It takes about a minute, you only do it once per project, and it makes every conversation afterward noticeably sharper. Best of all, `CLAUDE.md` is a plain text file in plain English. Open it, read it, and edit it yourself. It's often the friendliest documentation your project has ever had.
