"""B4/A5 alternative - multinomial Naive Bayes (pure Python) vs the lexicon, leave-one-out on the 60 complaints."""
import math
import time
from collections import Counter, defaultdict

from ai_tools import tokens, label
from complaints_data import COMPLAINTS


def train(data):
    prior, wc, vocab = Counter(), defaultdict(Counter), set()
    for text, y, _ in data:
        prior[y] += 1
        for w in tokens(text):
            wc[y][w] += 1; vocab.add(w)
    return prior, wc, vocab


def predict(model, text):
    prior, wc, vocab = model
    n = sum(prior.values()); best, arg = -1e18, None
    for y in prior:
        tot = sum(wc[y].values())
        lp = math.log(prior[y] / n) + sum(math.log((wc[y][w] + 1) / (tot + len(vocab))) for w in tokens(text))
        if lp > best:
            best, arg = lp, y
    return arg


ok_nb = ok_lex = 0
t0 = time.perf_counter()
for i, (text, y, _) in enumerate(COMPLAINTS):
    model = train(COMPLAINTS[:i] + COMPLAINTS[i + 1:])
    ok_nb += predict(model, text) == y
dt = time.perf_counter() - t0
ok_lex = sum(label(t) == y for t, y, _ in COMPLAINTS)
print(f"Leave-one-out accuracy, Naive Bayes (59 training complaints each time): {ok_nb}/60 = {100 * ok_nb / 60:.1f}%")
print(f"Lexicon scorer (no training)                                          : {ok_lex}/60 = {100 * ok_lex / 60:.1f}%")
model = train(COMPLAINTS)
t0 = time.perf_counter()
for _ in range(500):
    for t, _, _ in COMPLAINTS:
        predict(model, t)
print(f"NB prediction time: {(time.perf_counter() - t0) / 30000 * 1e6:.1f} us per complaint")
print(f"NB model size: vocabulary {len(model[2])} words x 3 classes (~{len(model[2]) * 3 * 8 / 1024:.1f} KB of counts)")
