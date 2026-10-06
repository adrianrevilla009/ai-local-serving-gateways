"""Encodes the decision note as code so the rules are explicit and testable. Order of questions matters."""


def choose(knowledge_changes_often, needs_citations, needs_new_style_or_format, prompt_fits_in_context, labeled_examples):
    """Return the cheapest technique that fits; escalate only when the cheaper one cannot work."""
    if knowledge_changes_often or needs_citations:
        return "rag"  # facts live in an index you can update and cite, not in weights
    if needs_new_style_or_format and labeled_examples >= 500:
        return "fine-tuning"  # behaviour/format is learned from examples
    if prompt_fits_in_context:
        return "prompting"  # instructions plus a few examples in the prompt
    return "rag"


CASES = [
    (dict(knowledge_changes_often=True, needs_citations=False, needs_new_style_or_format=False,
          prompt_fits_in_context=False, labeled_examples=0), "rag"),
    (dict(knowledge_changes_often=False, needs_citations=False, needs_new_style_or_format=True,
          prompt_fits_in_context=True, labeled_examples=2000), "fine-tuning"),
    (dict(knowledge_changes_often=False, needs_citations=False, needs_new_style_or_format=True,
          prompt_fits_in_context=True, labeled_examples=20), "prompting"),
]

if __name__ == "__main__":
    for args, expected in CASES:
        got = choose(**args)
        assert got == expected, (args, got, expected)
    print(f"ok: {len(CASES)} decision cases")
