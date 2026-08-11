# Claude for REALTORS®

*Using AI in your real estate business without breaking the rules that protect it.*

---

## Welcome!

You already know that AI can write a listing description in nine seconds. That's the easy part, and frankly it's the least interesting thing about this.

The hard part is that real estate is a regulated profession with a trademark you are licensed to use, a Code of Ethics you agreed to follow, and fair housing law that does not care one bit whether a human or a machine wrote the sentence. An AI tool that doesn't know those rules will cheerfully write you into a violation.

This guide fixes that. You'll learn how to set Claude up so it respects the REALTOR® marks by default, keeps your marketing fair housing compliant, and turns real NAR data into content your clients actually want.

> **Please read this first.** This document is educational, not legal advice. Trademark and fair housing rules change, and your state, your MLS, and your brokerage may impose stricter requirements than anything here. Verify trademark questions with NAR Legal Affairs at **trademark@nar.realtor**, and take compliance questions to your broker or your own counsel.

---

## Part 1: The Trademark Rules Claude Doesn't Know

### Why This Section Comes First

REALTOR® is not a synonym for "real estate agent." It's a federally registered collective membership mark owned by the National Association of REALTORS®, and you are licensed to use it because you're a member. That license comes with rules.

Here's the problem: a general-purpose AI has read the entire internet, and the internet is full of people using the mark incorrectly. Ask for a bio and you may well get back "experienced realtor" in lowercase, which is exactly the kind of usage the rules exist to prevent. **Claude will follow these rules beautifully once you tell it to, and it will not follow them if you don't.**

### The Core Rules

**Use it in all capital letters with the registration symbol.** The preferred format is REALTOR® or REALTORS®. When all caps isn't feasible, an initial capital R is the fallback. Lowercase is prohibited, with one exception covered below.

**It identifies a member, not a profession.** The term should be used only in reference to real estate professionals who are members of NAR, and never as a generic label for brokers or agents in general. "Contact a REALTOR® today" is fine when you mean a member. "The realtor showed us three houses" is a misuse, and so is applying it to non-member agents.

**Separate it from your name with punctuation.** Write **Jane Smith, REALTOR®**, not "Jane Smith REALTOR®". The comma or dash is required whenever possible, even when the two appear on separate lines of a signature or a sign. Helpfully, separating punctuation is not needed when the mark appears *before* your name.

**Pair it with a name, not a description.** The marks must be used with a member's name or with the legal name of a member's real estate business. Using them with descriptive words or phrases is prohibited. That means constructions like "Luxury REALTOR®," "Your Neighborhood REALTOR® Team," or "Top-Producing REALTOR® of the Year" are the kind of phrasing to avoid, because the mark is being attached to a description instead of to a name.

**Mind plurals and possessives.** REALTORS® is the correct plural form. Avoid possessive constructions where you can, and never invent forms like "Realtor's" in lowercase or "REALTOR®s" with the symbol in the wrong place.

**Never imply NAR endorsement.** Your membership permits you to identify yourself as a member. It does not permit you to suggest that NAR endorses you, your listings, your brokerage, or your services.

### The Internet Exception

Because the whole world types web addresses in lowercase, the rules relax online. For **domain names, email addresses, and social media usernames**:

* Lowercase is acceptable.
* The ® symbol is not required.
* Separating punctuation between your name and the mark is not required.

So `janesmithrealtor.com` and `@janesmithrealtor` are acceptable, while the *visible text* of your website, your bio, and your profile description still follow the full capitalization and punctuation rules. Note also that non-members may not use the marks in domain names or usernames at all.

### Your Copy-and-Paste Compliance Instructions

This is the single most valuable thing in this guide. Paste this into the **custom instructions** of a Claude Project (see Part 5) and every piece of writing Claude produces for you will follow the rules automatically.

```
TRADEMARK RULES (always follow, in every draft):

1. Write REALTOR® and REALTORS® in all capital letters with the ®
   registration symbol. Never lowercase, never "Realtor."
2. Use the term only for members of the National Association of
   REALTORS®. When referring to real estate professionals generally,
   write "real estate agent," "broker," or "real estate professional"
   instead.
3. Always place separating punctuation between my name and the mark:
   "Jane Smith, REALTOR®". No punctuation is needed when the mark comes
   before my name.
4. Attach the mark only to my name or my firm's legal name. Never attach
   it to a descriptive phrase such as "luxury REALTOR®" or "top REALTOR®."
5. Never imply that NAR endorses me, my firm, or my listings.
6. Exception: in domain names, email addresses, and social media
   usernames, lowercase is fine and the ® and punctuation are not needed.
7. If a draft would require an improper use, rewrite the sentence rather
   than bending the rule, and tell me why you changed it.
```

> **Try this right now.** Ask Claude: *"Rewrite my agent bio to follow these trademark rules, and show me a short list of every correction you made and why."* You'll often learn more from the correction list than from the bio.

---

## Part 2: Fair Housing and AI, the Part That Actually Carries Risk

### One Sentence to Remember

> **Describe the property. Never describe the kind of person who should live there.**

Fair housing law regulates a message, not a vocabulary. That's why memorizing a list of banned words is not enough on its own. Plenty of violations are built entirely from words no list has ever mentioned.

### The Liability Rule Nobody Told You

**An AI draft is legally yours the moment you publish it.** If Claude writes "perfect for a young family" and you post it, you have made a familial status statement. "The AI wrote it" is not a defense, because publishing is the act the law cares about.

This is not a reason to avoid AI. It's a reason to always do a human compliance read before anything goes live.

### Language Patterns That Get Agents in Trouble

| Risky phrasing | Why it's a problem | Safer version |
|---|---|---|
| "Perfect for a young family" | Familial status and age | "Three bedrooms and a fenced yard" |
| "Walking distance to shops" | May imply an ability requirement | "0.4 miles from the town square" |
| "Bachelor pad" | Gender-coded | "Open one-bedroom layout" |
| "Safe neighborhood" | Invites steering, and it's a claim you can't verify | Describe verifiable features only |
| "Great schools nearby" | A steering proxy in many contexts | "Located in the Jefferson County school district" |
| "Ideal for empty nesters" | Familial status and age | "Low-maintenance single-level living" |
| "Exclusive community" | Can read as an exclusionary signal | "Homeowners association with 40 units" |

A useful note on history: the widely circulated "forbidden words" list traces back to a 1989 HUD memorandum that HUD later withdrew, with nothing formally replacing it. Treat any list as a prompt for thinking, never as a substitute for it.

### Your Fair Housing Prompt

Add this to the same Project instructions:

```
FAIR HOUSING RULES (always follow):

- Describe the property, never the type of person who should live there.
- Never reference or imply race, color, religion, sex, disability,
  familial status, national origin, or any protected class under federal,
  state, or local law.
- Do not use "family," "families," "kid-friendly," "bachelor," "empty
  nester," "safe," "exclusive," or "walking distance."
- Describe schools by district name and factual distances only. Never
  characterize school or neighborhood quality.
- Use measured distances instead of implied physical ability.
- After every listing description, add a short section titled
  "Compliance check" that flags any phrase a fair housing reviewer might
  question, and explain why.
```

That last line is the one that makes this genuinely useful. You get the draft *and* a second opinion on it in the same response.

### An Honest Warning

Claude is a strong compliance reviewer and a poor compliance guarantee. It will catch the obvious problems and most of the subtle ones. It will not catch a state-specific rule it wasn't told about, and it can be talked out of a correct objection if you push. **Your broker's review process still applies to every word.**

---

## Part 3: Marketing That Uses Your Actual Expertise

NAR's marketing resources center on a consistent theme: your value is the local knowledge and judgment a consumer cannot get anywhere else. That's a helpful frame for AI, because it tells you exactly which half of the job to delegate.

**Give Claude the drafting. Keep the judgment.**

### Listing Descriptions

Bad prompt: "Write a listing description for a 3 bedroom house."

You'll get generic filler, because you gave it nothing to work with.

Good prompt:

```
Write an MLS listing description, 150 words maximum.

Property: 1247 Maple Street, 3 bed, 2 bath, 1,850 sq ft, built 1962,
renovated 2023.
Standout features: original oak floors refinished, new 30-year roof,
south-facing sunroom, detached two-car garage with 220v wiring.
The tradeoff to work around: the kitchen is small and has not been updated.
Buyer profile in this price band locally: mostly repeat buyers trading
down from larger homes.
Tone: warm and specific, not salesy. No exclamation points.

Then give me a "Compliance check" section per my fair housing rules.
```

The difference is that the second prompt contains information only you have. That's the whole trick.

### Other High-Value Marketing Tasks

* **Turn one listing into ten pieces of content.** "Take this description and give me an Instagram caption, a Facebook post, a 30-second video script, an email to my sphere, and a text for my buyer's agent list. Match my voice in each."
* **Write the follow-up you keep putting off.** "Draft a check-in email to a seller whose home has been listed 45 days with 12 showings and no offers. Honest about the price conversation, not defensive, and end with a specific recommendation."
* **Prepare for the listing appointment.** "I'm presenting tomorrow. Give me the eight hardest questions a seller might ask about my commission and my marketing plan, and help me practice clear answers."
* **Explain the hard things simply.** "Explain escalation clauses to a first-time buyer at an eighth-grade reading level, in under 200 words."
* **Build your farming calendar.** "Create a 12-month content calendar for a neighborhood farm of 400 homes, one mailer and two social posts per month, seasonally relevant to Kentucky."

### Keeping Your Voice

Paste three or four things you actually wrote and liked into your Project knowledge, then instruct: *"Match the voice in these samples. I would rather sound like myself with a typo than sound like a brochure."*

Claude imitates a supplied voice far better than it invents one. Most AI real estate content sounds identical because nobody bothers with this step.

---

## Part 4: Turning NAR Research Into Client Conversations

### The Rule That Keeps You Credible

**Never ask Claude to recall a housing statistic from memory. Paste the real number in, then ask Claude to explain it.**

AI models can produce confident, wrong figures, and a wrong statistic in a listing presentation costs you more credibility than having no statistic at all. NAR's Research and Statistics group publishes the authoritative numbers. Your job is to bring the data. Claude's job is to make it land.

### What NAR Publishes

* **Existing-Home Sales**, monthly, the industry's most-cited sales measure.
* **Profile of Home Buyers and Sellers**, annual, now in its 44th year, and the deepest look at consumer behavior available.
* **REALTORS® Confidence Index**, monthly, drawn from member survey responses on traffic, cash sales, and conditions.
* **Housing Affordability Index**, measuring whether a typical family earns enough to qualify for a mortgage on a typical home.
* **Local and metro market statistics**, where available, which are usually the most persuasive of all in a listing appointment.

### Worked Example, Using Real 2025 Profile Data

Here are figures from NAR's 2025 Profile of Home Buyers and Sellers:

* Median buyer age reached a record **59**.
* First-time buyers fell to a record low **21%** of the market, with a median age of **40**.
* Repeat buyers made up **79%** of purchases, with a median down payment of **23%**, the highest since 2003.
* First-time buyer median down payment rose to **10%**, the highest since 1989.
* **88%** of buyers and **91%** of sellers used a real estate professional.
* FSBO fell to **5%**, the lowest share ever recorded.
* The typical seller had owned the home **11 years** before selling, another record.

Now the prompt:

```
Here are statistics from NAR's 2025 Profile of Home Buyers and Sellers:
[paste the figures above]

I present to sellers in the $250k to $400k range in Louisville.

1. Which two of these numbers matter most to that seller, and why?
2. Write me three sentences I can say out loud in a listing
   appointment that use those numbers without sounding like a
   statistics lecture.
3. What is the strongest honest objection a seller could raise
   against my interpretation?
```

Question 3 is the one most people skip, and it's the one that keeps you from walking into a room overconfident.

### A Second Use: Explaining the Market to Nervous Clients

```
My buyer client is frustrated that they have been outbid three times.
Using the NAR data above, write a short, honest email that explains
what they are up against without being discouraging, and gives them
two concrete strategy changes to consider.
```

Note what the data does here. It reframes a personal failure as a market condition, which is both kinder and more accurate.

---

## Part 5: Setting Up Your REALTOR® Project

If you read Guide 1, this is where Projects prove their worth. Do this once and every future chat inherits it.

1. In the claude.ai sidebar, click **Projects**, then **New Project**.
2. Name it something like "My Real Estate Practice."
3. In **custom instructions**, paste both rule blocks from Part 1 and Part 2, plus a few lines about who you are: your market, your typical client, your brokerage, and how you like to sound.
4. In **Project knowledge**, upload:
   * Three or four writing samples in your own voice.
   * Your brokerage's advertising and compliance policy.
   * Your listing presentation.
   * Current market statistics you trust, refreshed monthly.
5. Start every work chat inside this Project.

That fifth step is the one people forget. A Project you never open is just a folder.

### Connectors Worth Adding

From Guide 2, the integrations that pay off fastest in this business:

* **Google Drive**, so Claude can pull from your listing files, disclosures, and market reports without you hunting for them.
* **Google Calendar**, for showing schedules and follow-up planning.
* **Gmail**, for drafting replies in context rather than from scratch.

A representative ask once connected: *"Find the seller net sheet for 1247 Maple in my Drive and draft an email walking the seller through it in plain English."*

---

## Quick Reference Card

**Trademark, at a glance**

| Do | Don't |
|---|---|
| Jane Smith, REALTOR® | Jane Smith Realtor |
| REALTORS® | Realtors |
| janesmithrealtor.com | Lowercase in your visible bio text |
| Use it for NAR members | Use it for agents in general |
| Attach it to a name | Attach it to a description |

**Fair housing, at a glance**

| Do | Don't |
|---|---|
| Describe rooms, materials, measurements | Describe who belongs there |
| "0.4 miles from downtown" | "Walking distance" |
| "Jefferson County school district" | "Great schools" |
| Human review before publishing | Publish an AI draft unread |

---

## Pro-Tip

**Make Claude argue with you before a big listing appointment.**

Everyone uses AI to produce things. Almost nobody uses it to pressure-test things, which is where the real advantage sits. The night before a presentation, try this:

```
You are a skeptical seller interviewing three agents tomorrow. I am
one of them. My pitch is: [paste your pitch]. Ask me the six hardest
questions you have, one at a time. Push back on weak answers. Do not
be polite about it.
```

Ten minutes of that will do more for your close rate than another hundred social posts. You'll find the soft spot in your pitch in your kitchen, where it costs you nothing, instead of at a stranger's dining room table, where it costs you the listing.

---

## Sources and Further Reading

* [NAR Membership Marks Manual](https://www.nar.realtor/membership-marks-manual) and [Limitations on License to Use the MARKS](https://www.nar.realtor/membership-marks-manual/limitations-on-license-to-use-the-marks)
* [NAR Logos and Trademark Rules](https://www.nar.realtor/logos-and-trademark-rules), including [Using NAR Trademarks in Usernames](https://www.nar.realtor/logos-and-trademark-rules/using-nar-trademarks-in-usernames), [Trademark Use on Social Media](https://www.nar.realtor/logos-and-trademark-rules/trademark-use-on-social-media), and the [Logo and Trademark FAQ](https://www.nar.realtor/logos-and-trademark-rules/logo-trademark-faq)
* [On Your Mark: A Trademark Pocket Reference for Members](https://www.yorkcountycouncil.com/wp-content/uploads/2021/12/OnYourMark-ATrademarkPocketReferenceforMembers.pdf)
* [The REALTOR® Trademark and Logo in Member Marketing, Boise Regional REALTORS®](https://www.boirealtors.com/realtor-trademark-logo-member-marketing/)
* [NAR Marketing resources](https://www.nar.realtor/marketing)
* [NAR Research and Statistics](https://www.nar.realtor/research-and-statistics) and [Housing Statistics and Market Trends](https://www.nar.realtor/research-and-statistics/housing-statistics)
* [2025 Profile of Home Buyers and Sellers highlights](https://www.nar.realtor/sites/default/files/2025-11/2025-profile-of-home-buyers-and-sellers-highlights-11-04-2025.pdf) and [Top 10 Takeaways](https://www.nar.realtor/blogs/economists-outlook/top-10-takeaways-from-nars-2025-profile-of-home-buyers-and-sellers)
* [REALTORS® Confidence Index](https://www.nar.realtor/research-and-statistics/research-reports/realtors-confidence-index) and [Housing Affordability Index](https://www.nar.realtor/research-and-statistics/housing-statistics/housing-affordability-index)

*REALTOR® and REALTORS® are registered collective membership marks owned by the National Association of REALTORS®. This guide is an independent educational resource and is not affiliated with, endorsed by, or approved by NAR.*
