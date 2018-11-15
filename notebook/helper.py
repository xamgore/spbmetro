from collections import defaultdict

from IPython.display import display
from ipymarkup import BoxLabelMarkup, LineMarkup, show_markup
from typing import Dict, List, Union
from yargy import Parser
from yargy.rule import NamedRule


def find(text: str, substr: str):
    pos = text.find(substr)
    return (pos, pos + len(substr)) if pos != -1 else (-1, -1)


def test(rule, *lines, tree=False, facts=False):
    is_at = lambda span, set: any((span == s) for s in set)
    parser = Parser(rule)

    for line in lines:
        if isinstance(line, str):
            text, expected = line, []
        else:
            text = line[0]
            expected = [find(text, substr) for substr in line[1:]]

        matches = list(sorted(parser.findall(text), key=lambda _: _.span))
        # display(matches)
        matched_spans = [_.span for _ in matches]
        spans = [(s[0], s[1], '#aec7e8' if is_at(s, expected) else '#ff9896') for s in matched_spans] \
                + [(s[0], s[1], '#ccc') for s in expected if not is_at((s[0], s[1]), matched_spans)]

        show_markup(text, [s for s in spans if s[0] < s[1]], LineMarkup)

        if matches:
            for _ in matches:
                if tree:
                    display(matches[0].tree.as_dot)
                if facts:
                    display(_.fact)


def test_samples(rules: Union[NamedRule, List[NamedRule]], texts: List[str], num: int = 20, seed: int = None,
                 markup=None):
    from random import seed as sed, sample

    sed(seed)
    texts = sample(texts, num)
    results: Dict[int, Dict[int, List]] = defaultdict(dict)

    if not (isinstance(rules, list) or isinstance(rules, tuple)):
        rules = [rules]

    for rule_idx, rule in enumerate(rules):
        parser = Parser(rule)

        for text_idx in range(num):
            matches = parser.findall(texts[text_idx])
            results[text_idx][rule_idx] = matches

    for text_idx, rule_spans in results.items():
        spans = [(s.span[0], s.span[1], str(rules[rule_idx].name)) for rule_idx, spans in rule_spans.items() for s in
                 spans]
        show_markup(texts[text_idx], spans, markup or BoxLabelMarkup)
        for rule_idx, spans in rule_spans.items():
            for s in spans:
                display(s.fact)
