# KMP - O(n + m) cu failure function
from dataclasses import dataclass


@dataclass
class Match:
    line_number: int    # de la 1
    column: int         # de la 0
    line_text: str

    def __repr__(self) -> str:
        return f"Linia {self.line_number}, coloana {self.column}"


# failure[i] = cel mai lung prefix care e si sufix, ex: ababc -> [0,0,1,2,0]

def compute_failure(pattern: str) -> list[int]:
    m = len(pattern)
    failure = [0] * m
    k = 0

    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = failure[k - 1]

        if pattern[k] == pattern[i]:
            k += 1

        failure[i] = k

    return failure


def kmp_search(text: str, pattern: str) -> list[int]:

    n, m = len(text), len(pattern)

    if m == 0 or m > n:
        return []

    failure = compute_failure(pattern)
    positions: list[int] = []
    q = 0  # cate caractere se potrivesc

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = failure[q - 1]

        if pattern[q] == text[i]:
            q += 1

        if q == m:
            positions.append(i - m + 1)
            q = failure[q - 1]  # merge si cu suprapuneri

    return positions


# cauta in fiecare linie

def kmp_search_in_corpus(lines: list[str], pattern: str,
                          case_sensitive: bool = False) -> list[Match]:
    if not pattern:
        return []

    search_pattern = pattern if case_sensitive else pattern.lower()
    matches: list[Match] = []

    for line_idx, line in enumerate(lines):
        search_line = line if case_sensitive else line.lower()

        positions = kmp_search(search_line, search_pattern)

        for col in positions:
            matches.append(Match(
                line_number=line_idx + 1,
                column=col,
                line_text=line.rstrip()
            ))

    return matches


def highlight_match(line_text: str, column: int, pattern_len: int) -> str:
    return " " * column + "^" * pattern_len
