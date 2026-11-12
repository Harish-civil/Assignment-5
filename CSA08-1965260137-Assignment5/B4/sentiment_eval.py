"""B4.1 - run scorer + summariser on 60 complaints, compare with my own labels."""
import time
from collections import Counter

from ai_tools import label, score, summarise, first_k, top_words
from complaints_data import COMPLAINTS

print(f"{'#':>2} {'mine':8} {'scorer':8} {'ok':3} score  text")
agree, wrong, conf = 0, [], Counter()
for i, (text, mine, key) in enumerate(COMPLAINTS, 1):
    pred = label(text)
    ok = pred == mine
    agree += ok
    conf[(mine, pred)] += 1
    if not ok:
        wrong.append((i, mine, pred, text))
    print(f"{i:>2} {mine:8} {pred:8} {'Y' if ok else 'N':3} {score(text):>4}   {text[:60]}...")
n = len(COMPLAINTS)
print(f"\nAGREEMENT: {agree}/{n} = {100 * agree / n:.1f}%")
print("Confusion (mine -> scorer):")
for (m, p), c in sorted(conf.items()):
    print(f"   {m:8} -> {p:8} {c}")
print("\nDISAGREEMENTS:")
for i, m, p, t in wrong:
    print(f" #{i}: mine={m}, scorer={p} | {t}")

# ---- summariser quality: does a 1-sentence summary contain the key issue word? -----------
hit_ext = hit_first = 0
for text, _, key in COMPLAINTS:
    hit_ext += key.lower() in " ".join(summarise(text, 1)).lower()
    hit_first += key.lower() in " ".join(first_k(text, 1)).lower()
print(f"\nSUMMARY key-issue coverage (1 sentence): extractive {hit_ext}/{n} = {100 * hit_ext / n:.1f}% ; "
      f"first-sentence {hit_first}/{n} = {100 * hit_first / n:.1f}%")
for idx in (0, 9, 53):
    t = COMPLAINTS[idx][0]
    print(f"\nExample #{idx + 1}\n  full      : {t}\n  extractive: {summarise(t)[0]}\n  first-k   : {first_k(t)[0]}")

neg_texts = [t for t, m, _ in COMPLAINTS if m == "negative"]
print("\nTop words in negative complaints:", top_words(neg_texts))

# ---- timing --------------------------------------------------------------------------
texts = [t for t, _, _ in COMPLAINTS] * 800        # 48,000 ~ one month at the new scale
for name, fn in (("score", score), ("extractive summary", summarise), ("first-k summary", first_k)):
    t0 = time.perf_counter()
    for t in texts:
        fn(t)
    dt = time.perf_counter() - t0
    print(f"{name:20}: {len(texts):,} complaints in {dt:.3f} s  ({dt / len(texts) * 1e6:.1f} us each)")
