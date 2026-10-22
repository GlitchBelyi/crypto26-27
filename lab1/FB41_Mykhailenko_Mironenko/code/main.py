from pathlib import Path

from entropy_calc import analyze_text
from experiments import experiment_3, experiment_4
from results_io import (
    save_experiment_3,
    save_experiment_4,
    save_frequency_table,
    save_main_results,
    save_redundancy,
    save_summary,
)
from text_processing import (
    ALPHABET_WITH_SPACE,
    RUSSIAN_LETTERS,
    normalize_text,
    read_text_auto,
)


BASE_DIR = Path(__file__).resolve().parent

SOURCE_FILE = BASE_DIR / "text.txt"

DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"


def main():
    if not SOURCE_FILE.exists():
        print("Файл text.txt не знайдено.")
        return

    source_size = SOURCE_FILE.stat().st_size

    if source_size < 1_000_000:
        print("Увага: text.txt менший за 1 МБ.")

    DATA_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

    source_text, encoding = read_text_auto(
        SOURCE_FILE
    )

    text_with_spaces = normalize_text(
        source_text
    )

    text_without_spaces = (
        text_with_spaces.replace(" ", "")
    )

    (
        DATA_DIR / "text_with_spaces.txt"
    ).write_text(
        text_with_spaces,
        encoding="utf-8"
    )

    (
        DATA_DIR / "text_without_spaces.txt"
    ).write_text(
        text_without_spaces,
        encoding="utf-8"
    )

    with_spaces = analyze_text(
        text_with_spaces,
        len(ALPHABET_WITH_SPACE)
    )

    without_spaces = analyze_text(
        text_without_spaces,
        len(RUSSIAN_LETTERS)
    )

    main_results = {
        "with_spaces": with_spaces,
        "without_spaces": without_spaces,
    }

    save_frequency_table(
        RESULTS_DIR / "characters_with_spaces.csv",
        with_spaces["characters"]
    )

    save_frequency_table(
        RESULTS_DIR / "characters_without_spaces.csv",
        without_spaces["characters"]
    )

    save_frequency_table(
        RESULTS_DIR / "bigrams_overlap_with_spaces.csv",
        with_spaces["bigrams_overlap"]
    )

    save_frequency_table(
        RESULTS_DIR / "bigrams_nonoverlap_with_spaces.csv",
        with_spaces["bigrams_nonoverlap"]
    )

    save_frequency_table(
        RESULTS_DIR / "bigrams_overlap_without_spaces.csv",
        without_spaces["bigrams_overlap"]
    )

    save_frequency_table(
        RESULTS_DIR / "bigrams_nonoverlap_without_spaces.csv",
        without_spaces["bigrams_nonoverlap"]
    )

    save_main_results(
        RESULTS_DIR / "entropy.csv",
        main_results
    )

    exp3, sequences3 = experiment_3(
        text_with_spaces,
        ALPHABET_WITH_SPACE
    )

    for name, sequence in sequences3.items():
        (
            DATA_DIR / f"experiment_{name}.txt"
        ).write_text(
            sequence,
            encoding="utf-8"
        )

    save_experiment_3(
        RESULTS_DIR / "experiment_3.csv",
        exp3
    )

    exp4, sequences4 = experiment_4()

    for name, sequence in sequences4.items():
        (
            DATA_DIR / f"experiment_{name}.txt"
        ).write_text(
            sequence,
            encoding="utf-8"
        )

    save_experiment_4(
        RESULTS_DIR / "experiment_4.csv",
        exp4
    )

    save_redundancy(
        RESULTS_DIR / "redundancy.csv",
        main_results
    )

    save_summary(
        RESULTS_DIR / "summary.txt",
        source_size,
        encoding,
        main_results,
        exp3,
        exp4
    )

    print("Готово.")
    print(
        f"Результати: {RESULTS_DIR}"
    )


if __name__ == "__main__":
    main()