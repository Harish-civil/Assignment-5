"""B2.3 - adversarial sentences for the sentiment scorer (B4/ai_tools.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B4"))
from ai_tools import label, score

CASES = [  # (category, sentence, correct human label)
    ("sarcasm", "Oh great, the factory is burning plastic again.", "negative"),
    ("sarcasm", "Wonderful, another dirty day. Thanks a lot.", "negative"),
    ("sarcasm", "Yeah right, the air is really clean today.", "negative"),
    ("double negative", "I cannot say it is not good.", "positive"),
    ("double negative", "It is not that the service is not helpful.", "positive"),
    ("double negative", "Never again will I say the air is not bad.", "negative"),
    ("mixed opinion", "The staff were polite but the air is still terrible.", "negative"),
    ("mixed opinion", "Good app, bad data, slow support, clean design.", "neutral"),
    ("mixed opinion", "Air is cleaner now but smoke returns at night.", "neutral"),
    ("distance of negator", "The air is not very good.", "negative"),
    ("unknown words", "The stench is unbearable and I feel nauseous.", "negative"),
    ("spelling / slang", "Aiir is baad, super smokey!!", "negative"),
]
ok = 0
for cat, text, truth in CASES:
    pred = label(text)
    ok += pred == truth
    print(f"{cat:20} score {score(text):>3}  scorer={pred:8} human={truth:8} {'OK ' if pred == truth else 'FAIL'} | {text}")
print(f"\nCorrect on adversarial set: {ok}/{len(CASES)}")
