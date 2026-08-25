# Day 14 — Planning the Smart Notes Summarizer

---

## Step 1 — Write the one sentence

> Paste long lecture notes, get back the 5 most important sentences, the
> key terms, and how long the notes take to read.

Rules for the sentence:

- It says what the **user gets**, not what the code does. "Uses TF-IDF"
  is not a promise, it is a technique.
- No "and also". If you need two sentences, you have two apps, and you
  are going to finish neither today.
- If you cannot write it, you do not have an idea yet. You have a mood.

**Ask the room:** what is the one sentence for your group project?

---

## Step 2 — Write the contract

Before anything in the middle, pin down the two ends.

| | |
|---|---|
| **IN** | one blob of text — pasted, or read from a `.txt` file |
| | one number — how many sentences the summary should be |
| **OUT** | a summary — N sentences, in the order they were written |
| | key terms — the 10 words the notes lean on hardest |
| | stats — word count, reading time, sentence count |
| | a chart — those 10 words, drawn by weight |

Why this comes second: once both ends are nailed down, you can build the
middle in any order, and **you can tell when a piece is finished.**
Without a contract, "done" is a feeling.

---

## Step 3 — Draw the pipeline, with the shape of the data at every arrow

```
text (str)
   │
   ├─ split_into_sentences()  ──▶  list[str]           Day 11  regex
   ├─ score_sentences()       ──▶  array of floats     Day 13  TF-IDF
   ├─ pick_summary()          ──▶  list[str]           Day 2   sort + slice
   ├─ extract_key_terms()     ──▶  DataFrame           Day 13 + Day 6
   ├─ compute_stats()         ──▶  three ints          Day 2
   └─ Streamlit renders it    ──▶  pixels              Days 4-5, Day 7
```

Two things to notice:

1. **Write the type on every arrow.** `list[str]`, not "the sentences".
   Most bugs in a small app are one function handing the next the wrong
   shape — a string where a list was expected, a numpy array where a
   float was expected. Naming the shape here means you catch it in a
   diagram instead of in a traceback.

2. **Five arrows became five functions**, with the same names. That is
   not a coincidence. The pipeline drawn on the board *is* the function
   list. If you cannot name the arrow, the function does not have one
   job — split it.

---

## Step 4 — Argue the decisions now, so you do not argue them at line 200

Every one of these could have gone the other way. What matters is that
the argument happened **before** the code, and that the reason is written
down where the next person can read it.

| Decision | We chose | Why | Cost of changing later |
|---|---|---|---|
| Sentence score | **Sum** of word weights | Rewards sentences carrying more loaded words. On lecture notes those really are the important ones. | One line — `.sum(axis=1)` → `.mean(axis=1)` |
| Summary order | **Original**, not ranked | Ranked order reads like five unrelated facts. Original order still reads like an argument. | One line — but everybody notices |
| A "Summarize" button | **No button** | The whole computation is milliseconds. A button adds a click and a `session_state` variable to keep results alive across reruns. | Touches every section |
| Caching (Day 12) | **No** | `st.cache_data` earns its place on network calls and big files. TF-IDF over 20 sentences is not slow. | Cheap to add, so do not add it early |
| Input | Paste **and** `.txt` upload | Both are in the target on slide 3. PDF is Day 11 work and is not today's point. | Cheap |

The mockup on slide 3 has a **Summarize** button. We are not building it.
That is what a plan is for — you find the contradiction on paper, decide,
and write down which one won.

---

## Step 5 — List what will go wrong, *before* it goes wrong

This is the step people skip, and it is the one that saves the demo.

| What happens | What the app does |
|---|---|
| Nothing pasted yet | `st.info` — and computes nothing |
| One sentence pasted | Say there is nothing to summarise. A **warning**, not an error — the user did nothing wrong |
| `"the and a is of"` | TF-IDF raises `empty vocabulary`. Catch it, say it in English |
| Notes about **Dr.** Ambedkar | The naive regex splits on `Dr.` — see below |
| Accuracy rose to **98.6** percent | Same problem, different cause |
| `.txt` file saved on a Windows laptop | Not UTF-8. `.decode("utf-8")` raises on the first curly quote |

### The one worth stopping on

Slide 5 gives the sentence splitter as one line:

```python
re.split(r'(?<=[.!?])\s+', text)
```

and the checkpoint on that same slide says *"sentences are split correctly
(not on 'Mr.' or 'Dr.')"*.

**Both cannot be true.** That one line splits `"Dr. Ambedkar"` straight
down the middle.

Planning is what makes you notice. The checkpoint is the thing worth
keeping, so the function grew from one line to fifteen, using
**protect → split → restore**:

1. Hide the full stops that do not end a sentence (`Dr.` → `Dr␀`).
2. Split on the ones left over — now every one of them is real.
3. Put the hidden ones back.

Fifteen lines instead of one, decided in the plan, not at 11:40 in front
of a class.

---

## Step 6 — Choose the build order, smallest runnable slice first

| Section | Does | Minutes | You can run it? |
|---|---|---|---|
| 1 | text in → sentences out | 15 | yes |
| 2 | sentences in → summary out | 15 | yes |
| 3 | key terms, stats, chart | 15 | yes |
| 4 | polish — sidebar, empty state, footer | 15 | yes |

The only rule: **each section runs before the next one is written.** Not
compiles — runs, in a browser, with real notes pasted in.

If a section cannot run on its own, it is too big. Cut it in half.

Every section in `smart_notes_app.py` carries its checkpoint as a comment
block, so you can tick them off on the projector as we go.

---

## Step 7 — Write down what you are NOT building

- PDF upload. Day 11 can already do it. It is not today's point.
- Sentences rewritten in the model's own words. TF-IDF **selects**
  sentences; it cannot **write** one. That is a different kind of model
  entirely.
- Saving summaries to a database. Day 10 can do it. Out of scope.

A plan with no out-of-scope list is not a plan, it is a wish. The list is
what you point at when someone says *"could it also just…"* at minute
sixty-five.

---

## What the plan missed

Honest postscript, and the most useful slide of the day.

The first real test run put **`98`** on the key-terms cards, ranked above
real words. TF-IDF's tokenizer had split `98.6` into `98`, and nothing in
step 5 said *"the vocabulary will contain things that are not words."*
Stop words were planned for. Digits were not.

The fix was four lines in `extract_key_terms()`. It cost nothing because
the pipeline had one function that owned key terms — that is step 3 paying
for itself.

**The lesson is not "plan harder."** It is:

- A plan is not a prophecy. It will miss things.
- A good plan makes the miss **cheap** — one function, four lines, no
  other section touched.
- When it misses, add the miss to step 5 of your *next* plan.

---

## Template — copy this for the Day 16 group project

```
1. THE ONE SENTENCE
   A user can ______ so that ______.

2. THE CONTRACT
   IN:   ______
   OUT:  ______

3. THE PIPELINE          (write the data shape on every arrow)
   ______ ──▶ ______ ──▶ ______ ──▶ ______

4. DECISIONS             (the ones that could have gone either way)
   We chose ______ over ______ because ______.

5. WHAT WILL GO WRONG    (at least five; empty input is always one)
   When ______ , the app ______.

6. BUILD ORDER           (each step must RUN before the next is written)
   Step 1 ______ (runs? ___)   Step 2 ______ (runs? ___)

7. NOT BUILDING
   ______ , ______ , ______
```

Fifteen minutes on this. Then open the editor.
