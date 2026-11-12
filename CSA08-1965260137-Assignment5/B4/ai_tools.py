"""B4 - lexicon sentiment scorer with negation, extractive summariser, keyword statistics."""
import re
from collections import Counter

POSITIVE = {"good", "clean", "cleaner", "fast", "helpful", "improved", "improvement", "better",
            "great", "excellent", "quick", "pleasant", "fresh", "happy", "nice", "polite",
            "resolved", "responsive", "satisfied", "thank", "thanks", "useful", "fine"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken", "worse", "terrible", "awful",
            "poor", "dust", "smell", "polluted", "pollution", "noise", "dangerous", "toxic",
            "choking", "burning", "foul", "unhealthy", "ignored", "delay", "fumes"}
NEGATORS = {"not", "never", "no", "cannot"}
STOP = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "of", "to", "in", "on", "at",
        "it", "its", "i", "we", "my", "our", "you", "your", "for", "with", "this", "that", "be",
        "has", "have", "had", "been", "from", "by", "as", "but", "so", "do", "does", "did",
        "please", "me", "us", "there", "they", "them", "very", "every", "any", "up", "out"}


def tokens(text):
    return re.findall(r"[a-z']+", text.lower())


def is_negator(word):
    return word in NEGATORS or word.endswith("n't")


def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = tokens(text)
    total = 0
    for i, w in enumerate(words):
        value = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if value and i > 0 and is_negator(words[i - 1]):
            value = -value
        total += value
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def summarise(text, k=1):
    """Extractive: pick the k sentences with the highest sum of frequencies of important words."""
    sents = sentences(text)
    if len(sents) <= k:
        return sents
    freq = Counter(w for w in tokens(text) if w not in STOP and len(w) > 2)
    scores = [sum(freq[w] for w in tokens(s) if w in freq) for s in sents]
    top = sorted(sorted(range(len(sents)), key=lambda i: (-scores[i], i))[:k])
    return [sents[i] for i in top]


def first_k(text, k=1):
    return sentences(text)[:k]


def top_words(texts, n=8):
    c = Counter(w for t in texts for w in tokens(t) if w not in STOP and len(w) > 2)
    return c.most_common(n)
