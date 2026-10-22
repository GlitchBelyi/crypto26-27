import csv

from entropy_calc import redundancy, top5


def visible(value):
    return value.replace(" ", "␠")


def save_frequency_table(path, counter):
    total = sum(counter.values())

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "symbol",
            "count",
            "probability"
        ])

        for symbol, count in counter.most_common():
            writer.writerow([
                visible(symbol),
                count,
                f"{count / total:.10f}"
            ])


def save_main_results(path, results):
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "text",
            "H0",
            "H1",
            "H2_overlap",
            "H2_nonoverlap"
        ])

        for name, result in results.items():
            writer.writerow([
                name,
                f"{result['H0']:.8f}",
                f"{result['H1']:.8f}",
                f"{result['H2_overlap']:.8f}",
                f"{result['H2_nonoverlap']:.8f}",
            ])


def save_experiment_3(path, results):
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "sequence",
            "H1"
        ])

        for row in results:
            writer.writerow([
                row["name"],
                f"{row['H1']:.8f}"
            ])


def save_experiment_4(path, results):
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "sequence",
            "H1",
            "H2_overlap",
            "H2_nonoverlap"
        ])

        for row in results:
            writer.writerow([
                row["name"],
                f"{row['H1']:.8f}",
                f"{row['H2_overlap']:.8f}",
                f"{row['H2_nonoverlap']:.8f}",
            ])


def save_redundancy(path, results):
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "text",
            "model",
            "entropy",
            "redundancy"
        ])

        for name, result in results.items():
            h0 = result["H0"]

            for model in (
                "H1",
                "H2_overlap",
                "H2_nonoverlap"
            ):
                value = result[model]

                writer.writerow([
                    name,
                    model,
                    f"{value:.8f}",
                    f"{redundancy(value, h0):.8f}",
                ])


def format_top5(counter):
    return ", ".join(
        f"{visible(symbol)} ({probability:.5f})"
        for symbol, _, probability in top5(counter)
    )


def save_summary(
    path,
    source_size,
    encoding,
    main_results,
    exp3,
    exp4
):
    lines = [
        f"Розмір вихідного файлу: "
        f"{source_size / 1024 / 1024:.3f} МБ",
        f"Кодування: {encoding}",
        "",
    ]

    for name, result in main_results.items():
        lines.extend([
            f"=== {name} ===",
            f"H0 = {result['H0']:.6f}",
            f"H1 = {result['H1']:.6f}",
            f"H2 overlap = "
            f"{result['H2_overlap']:.6f}",
            f"H2 non-overlap = "
            f"{result['H2_nonoverlap']:.6f}",
            "Top-5 символів: "
            + format_top5(result["characters"]),
            "Top-5 біграм overlap: "
            + format_top5(
                result["bigrams_overlap"]
            ),
            "Top-5 біграм non-overlap: "
            + format_top5(
                result["bigrams_nonoverlap"]
            ),
            "",
        ])

    lines.append("=== Експеримент А / Б / В ===")

    for row in exp3:
        lines.append(
            f"{row['name']}: H1 = {row['H1']:.6f}"
        )

    lines.append("")
    lines.append("=== Експеримент Г / Д ===")

    for row in exp4:
        lines.append(
            f"{row['name']}: "
            f"H1 = {row['H1']:.6f}; "
            f"H2 overlap = "
            f"{row['H2_overlap']:.6f}; "
            f"H2 non-overlap = "
            f"{row['H2_nonoverlap']:.6f}"
        )

    path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )