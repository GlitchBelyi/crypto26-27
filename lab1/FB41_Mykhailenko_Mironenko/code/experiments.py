import random

from entropy_calc import h1, h2


def experiment_3(
    natural_text,
    alphabet,
    length=200_000,
    seed=42
):
    length = min(length, len(natural_text))

    sequence_a = natural_text[:length]
    sequence_b = "а" * length

    rng = random.Random(seed)

    sequence_v = "".join(
        rng.choice(alphabet)
        for _ in range(length)
    )

    results = [
        {
            "name": "A",
            "H1": h1(sequence_a)
        },
        {
            "name": "Б",
            "H1": h1(sequence_b)
        },
        {
            "name": "В",
            "H1": h1(sequence_v)
        },
    ]

    sequences = {
        "A": sequence_a,
        "Б": sequence_b,
        "В": sequence_v,
    }

    return results, sequences


def experiment_4(length=200_000, seed=42):
    if length % 2:
        length -= 1

    sequence_d = "аб" * (length // 2)

    chars = list(sequence_d)

    rng = random.Random(seed)
    rng.shuffle(chars)

    sequence_g = "".join(chars)

    results = [
        {
            "name": "Г",
            "H1": h1(sequence_g),
            "H2_overlap": h2(sequence_g, 1),
            "H2_nonoverlap": h2(sequence_g, 2),
        },
        {
            "name": "Д",
            "H1": h1(sequence_d),
            "H2_overlap": h2(sequence_d, 1),
            "H2_nonoverlap": h2(sequence_d, 2),
        },
    ]

    sequences = {
        "Г": sequence_g,
        "Д": sequence_d,
    }

    return results, sequences