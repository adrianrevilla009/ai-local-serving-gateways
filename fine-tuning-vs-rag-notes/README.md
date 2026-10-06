# fine-tuning-vs-rag-notes

`decide.py` holds a decision note as code: one `choose()` function that picks prompting, RAG or fine-tuning, and three test cases.

## Goal

Make the "fine-tuning vs RAG vs prompting" choice explicit and testable by asking the questions in order and returning the cheapest technique that fits.

## Run it

```
python3 decide.py
```

Expected: `ok: 3 decision cases`.

Everything here was run. It is a rule of thumb in code, not measured on a real model.

## What it proves

- If knowledge changes often or answers need citations, `choose()` returns `rag`, because facts then live in an index that can be updated.
- With a new style or format needed and at least 500 labeled examples, it returns `fine-tuning`; with 20 examples it returns `prompting`.
- When nothing else applies, a prompt that fits in context gives `prompting`, otherwise `rag`. The order of the checks in `decide.py` is the decision.

## Trade-offs

- The 500-example threshold is an assumption; the right number depends on the task and the model.
- Booleans hide shades: "knowledge changes often" has no cutoff.
- Three cases cover the main branches but not every combination.

## When not to use it

- When you can measure the options on your own evaluation set, trust those results over this rule.
- When fine-tuning is needed for cost or latency (a smaller model), which `choose()` does not consider.
