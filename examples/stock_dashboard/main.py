import csv
from pathlib import Path


def load_prices(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize(rows: list[dict[str, str]]) -> str:
    lines = ["Symbol | Price | Daily change"]
    for row in rows:
        lines.append(
            f"{row['symbol']} | ${float(row['price']):.2f} | "
            f"{float(row['change_percent']):+.2f}%"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(summarize(load_prices(Path(__file__).with_name("prices.csv"))))

