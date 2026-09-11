import math
import random
import string
from collections import Counter

RUSSIAN_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # 32 літери (ё -> е)
ALPHABET_WITH_SPACE = RUSSIAN_ALPHABET + " "


# 1. Попередня обробка тексту

def normalize_text(raw_text: str, alphabet: str = RUSSIAN_ALPHABET) -> str:
    """
    Правила обробки (згідно методички):
      - усі літери -> нижній регістр;
      - 'ё' зводимо до 'е' (щоб не роздувати алфавіт однією рідкісною літерою);
      - символи поза алфавітом (латиниця, цифри, пунктуація, лапки, тире...)
        вилучаються (тобто трактуються як роздільник -> замінюються пробілом);
      - послідовності пробілів/розділових символів -> один пробіл;
      - пробіли по краях прибираються.
    """
    text = raw_text.lower().replace("ё", "е")
    allowed = set(alphabet)
    out_chars = []
    for ch in text:
        out_chars.append(ch if ch in allowed else " ")
    collapsed = " ".join("".join(out_chars).split())
    return collapsed


def remove_spaces(text: str) -> str:
    return text.replace(" ", "")


# 2. Частоти символів і n-грам

def symbol_frequencies(text: str) -> Counter:
    return Counter(text)


def bigram_frequencies(text: str, overlapping: bool = True) -> Counter:
    step = 1 if overlapping else 2
    bigrams = (text[i:i + 2] for i in range(0, len(text) - 1, step))
    return Counter(b for b in bigrams if len(b) == 2)


def top_n(counter: Counter, n: int = 5):
    total = sum(counter.values())
    return [(item, cnt, cnt / total) for item, cnt in counter.most_common(n)]


# 3. Ентропія

def entropy_from_counts(counter: Counter) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    h = 0.0
    for cnt in counter.values():
        p = cnt / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def h1(text: str) -> float:
    return entropy_from_counts(symbol_frequencies(text))


def h2_per_symbol(text: str, overlapping: bool = True) -> float:
    """
    H2 у методичці визначена як 'питома ентропія на символ біграми', тобто
    H(X1,X2) / 2, а не сира сукупна ентропія біграми. Ділимо на 2, щоб
    порівнювати H1 і H2 в одних одиницях (біт/символ).
    """
    bigrams = bigram_frequencies(text, overlapping=overlapping)
    return entropy_from_counts(bigrams) / 2


# 4. Штучні послідовності для розділів 3 і 4 методички

def make_sequence_B(symbol: str, length: int) -> str:
    """Б — повторення одного символу."""
    return symbol * length


def make_sequence_V(alphabet: str, length: int, seed: int = 1) -> str:
    """В — рівноімовірна випадкова послідовність символів алфавіту."""
    rng = random.Random(seed)
    return "".join(rng.choice(alphabet) for _ in range(length))


def make_sequence_G(text_for_freqs: str, length: int, seed: int = 2) -> str:
    """
    Г — символи в випадковому порядку, але з частотами, близькими до
    частот природного тексту (перемішування символів природного фрагмента).
    """
    rng = random.Random(seed)
    pool = list(text_for_freqs[:length]) if len(text_for_freqs) >= length else \
        list((text_for_freqs * (length // len(text_for_freqs) + 1))[:length])
    rng.shuffle(pool)
    return "".join(pool)


def make_sequence_D(two_symbols: str, length: int) -> str:
    """Д — виражена періодична структура: abababab..."""
    a, b = two_symbols[0], two_symbols[1]
    pattern = a + b
    reps = length // 2 + 1
    return (pattern * reps)[:length]


# 5. Наближена оцінка умовної ентропії H^(n) методом вгадування
#    (замінник CoolPinkProgram.exe — та сама методика "вгадай наступну
#    букву за (n-1)-грамою", описана в методичці)

def guess_experiment(text: str, n: int, trials: int, alphabet: str, seed: int = 42):
    """
    Повертає (H_lower, H_upper, H_shannon_like) для контексту довжини n-1.
    Для кожного випробування:
      - випадково обираємо позицію i, беремо (n-1)-граму text[i:i+n-1]
        як контекст;
      - шукаємо ВСІ входження цього контексту в тексті (окрім самого i)
        і дивимось розподіл символу, що йде за контекстом;
      - "експериментатор" вгадує найімовірніший символ за цим розподілом
        спочатку 1-ю спробою, потім 2-ю (наступний за ймовірністю) і т.д.
    Накопичуємо q_1..q_m (частку вгадувань з 1-ї, 2-ї, ..., m-ї спроби)
    та обчислюємо межі нерівності з методички, а також H^(n) у "шенонівському"
    сенсі: середню умовну ентропію розподілу наступного символу.
    """
    rng = random.Random(seed)
    m = len(alphabet)
    context_len = n - 1
    N = len(text)
    if N <= context_len + 1:
        raise ValueError("Текст закороткий для такого n")

    # індекс: контекст => Counter наступних символів (будуємо один раз для n)
    context_index = {}
    for i in range(N - context_len):
        ctx = text[i:i + context_len]
        nxt = text[i + context_len] if i + context_len < N else None
        if nxt is None:
            continue
        context_index.setdefault(ctx, Counter())[nxt] += 1

    guess_success_rank = []  # ранг вгадування (1 = з першої спроби) для кожного випробування
    cond_entropies = []      # ентропія розподілу наступного символу в цьому контексті

    trial = 0
    attempts = 0
    max_attempts = trials * 50
    while trial < trials and attempts < max_attempts:
        attempts += 1
        i = rng.randrange(0, N - context_len - 1)
        ctx = text[i:i + context_len]
        actual_next = text[i + context_len]
        counter = context_index.get(ctx)
        if not counter or sum(counter.values()) < 2:
            # контекст трапляється надто рідко, щоб зробити статистично
            # обґрунтоване вгадування — пропускаємо, як і мав би зробити
            # реальний експериментатор, обираючи іншу n-граму
            continue
        # ранжуємо кандидатів за спаданням імовірності
        ranked = [sym for sym, _ in counter.most_common()]
        rank = ranked.index(actual_next) + 1 if actual_next in ranked else m
        guess_success_rank.append(rank)
        cond_entropies.append(entropy_from_counts(counter))
        trial += 1

    if trial == 0:
        return None

    # q_i^(n): частка випробувань, вгаданих НЕ пізніше i-ї спроби (кумулятивно)
    q = []
    cum = 0
    for i in range(1, m + 1):
        cum += sum(1 for r in guess_success_rank if r == i)
        q.append(cum / trial)

    # Верхня межа за Шенноном: ентропія розподілу "з якої спроби вгадано"
    upper = 0.0
    prev = 0.0
    for qi in q:
        p_i = qi - prev
        if p_i > 0:
            upper -= p_i * math.log2(p_i)
        prev = qi

    # Пряма (незалежна від нерівності) оцінка H^(n): середня ентропія
    # емпіричного розподілу наступного символу за випадково вибраними
    # контекстами довжини n-1. Це те саме H^(n) = H(x_n | x_1..x_{n-1}),
    # обчислене напряму за n-грамною статистикою, а не через ігрову
    # нерівність — використовуємо як надійний орієнтир поряд з CoolPinkProgram.
    h_direct = sum(cond_entropies) / len(cond_entropies)

    return {
        "n": n,
        "trials": trial,
        "q": q,
        "upper_bound_shannon": upper,
        "h_direct_estimate": h_direct,
    }


# ---------------------------------------------------------------------------
# 6. Надлишковість
# ---------------------------------------------------------------------------

def redundancy(h_inf: float, alphabet_size: int) -> float:
    h0 = math.log2(alphabet_size)
    return 1 - h_inf / h0
