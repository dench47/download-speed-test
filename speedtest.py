#!/usr/bin/env python3
"""Замер скорости скачивания: N последовательных запросов к одному адресу."""

import argparse
import time
import urllib.request


def download_once(url: str) -> tuple[float, int]:
    """Скачивает url целиком, ждёт полного ответа. Возвращает (секунды, байты)."""
    start = time.perf_counter()
    with urllib.request.urlopen(url, timeout=120) as resp:
        body = resp.read()  # читаем тело до конца — это и есть полный ответ
    elapsed = time.perf_counter() - start
    return elapsed, len(body)


def fmt_bytes(n: float) -> str:
    """Человекочитаемый размер: байты -> КБ -> МБ."""
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or unit == "ГБ":
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} ГБ"


def main() -> None:
    parser = argparse.ArgumentParser(description="Замер скорости скачивания")
    parser.add_argument("url", help="адрес, к которому стучаться")
    parser.add_argument("-n", type=int, default=10, help="число запросов, по умолчанию 10")
    args = parser.parse_args()

    times = []
    total_bytes = 0
    for i in range(1, args.n + 1):
        elapsed, size = download_once(args.url)
        times.append(elapsed)
        total_bytes += size
        speed = size * 8 / elapsed / 1e6  # Мбит/с
        print(f"[{i:>2}/{args.n}] {fmt_bytes(size)} за {elapsed:.2f} c -> {speed:.1f} Мбит/с")

    total_time = sum(times)
    avg_time = total_time / len(times)
    mbits = total_bytes * 8 / total_time / 1e6        # Мбит/с
    mbytes = total_bytes / total_time / 1024 / 1024   # МБ/с

    print()
    print(f"Адрес: {args.url}, запросов: {len(times)}")
    print(f"Среднее время запроса: {avg_time:.2f} c")
    print(f"Общий объём: {fmt_bytes(total_bytes)} за {total_time:.2f} c")
    print(f"Скорость скачивания: {mbits:.1f} Мбит/с ({mbytes:.2f} МБ/с)")


if __name__ == "__main__":
    main()
