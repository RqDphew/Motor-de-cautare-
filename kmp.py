"""
kmp.py - Implementare algoritmul Knuth-Morris-Pratt (KMP)

KMP caută toate aparițiile unui pattern într-un text în timp O(n + m),
evitând comparațiile redundante prin funcția de eșec (failure function / prefix function).
"""

from dataclasses import dataclass


@dataclass
class Match:
    """Reprezintă o apariție a pattern-ului în text."""
    line_number: int    # linia (1-based) în care s-a găsit
    column: int         # coloana (0-based) de start în linia respectivă
    line_text: str      # textul complet al liniei (pentru afișare context)

    def __repr__(self) -> str:
        return f"Linia {self.line_number}, coloana {self.column}"



# Funcția de eșec (prefix function)

def compute_failure(pattern: str) -> list[int]:
    """
    Construiește funcția de eșec (prefix function) pentru `pattern`.

    failure[i] = lungimea celui mai lung prefix propriu al pattern[0..i]
                 care este și sufix al aceluiași subșir.

    Exemplu: pattern = "ababc"
      failure = [0, 0, 1, 2, 0]

    """
    m = len(pattern)
    failure = [0] * m
    k = 0  # lungimea prefixului curent potrivit

    # Parcurgem de la poziția 1 (failure[0] este mereu 0)
    for i in range(1, m):
        # Dacă nu se potrivesc, folosim failure pentru a retrage
        while k > 0 and pattern[k] != pattern[i]:
            k = failure[k - 1]

        if pattern[k] == pattern[i]:
            k += 1  # am extins prefixul potrivit

        failure[i] = k

    return failure


# Căutare KMP în șir unic

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Găsește toate pozițiile (0-based) la care `pattern` apare în `text`.
    """

    n, m = len(text), len(pattern)

    if m == 0 or m > n:
        return []

    failure = compute_failure(pattern)
    positions: list[int] = []
    q = 0  # numărul de caractere ale pattern-ului potrivite până acum

    for i in range(n):
        # Retragere prin failure function cât timp nu se potrivesc
        while q > 0 and pattern[q] != text[i]:
            q = failure[q - 1]

        if pattern[q] == text[i]:
            q += 1  # potrivire parțială extinsă

        if q == m:
            # Pattern complet găsit: poziția de start este i - m + 1
            positions.append(i - m + 1)
            q = failure[q - 1]  # continuăm căutarea (permite suprapuneri)

    return positions


# Căutare KMP în corpus

def kmp_search_in_corpus(lines: list[str], pattern: str,
                          case_sensitive: bool = False) -> list[Match]:
    """
    Caută `pattern` în toate liniile unui corpus text.
    Returnează lista de obiecte Match cu linia, coloana și contextul.
    """
    if not pattern:
        return []

    search_pattern = pattern if case_sensitive else pattern.lower()
    matches: list[Match] = []

    for line_idx, line in enumerate(lines):
        search_line = line if case_sensitive else line.lower()

        positions = kmp_search(search_line, search_pattern)

        for col in positions:
            matches.append(Match(
                line_number=line_idx + 1,   # 1-based pentru afișare
                column=col,
                line_text=line.rstrip()     # fără newline trailing
            ))

    return matches


# Utilitar: afișare vizuală a potrivirii


def highlight_match(line_text: str, column: int, pattern_len: int) -> str:
    """
    Construiește un string care evidențiază poziția pattern-ului în linie.

    """
    return " " * column + "^" * pattern_len
