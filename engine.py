# motor de cautare: trie pt cuvinte/prefix, kmp pt pattern in text
import re
from trie import Trie
from kmp import kmp_search_in_corpus, highlight_match, compute_failure


class TextSearchEngine:

    def __init__(self, name: str = "corpus"):
        self.trie = Trie()
        self.lines: list[str] = []
        self._name = name

    # Încărcare text

    def load_text(self, text: str) -> None:
        self.lines = text.splitlines()

        for line in self.lines:
            # Extrage cuvintele: secvențe de litere și cifre, ignoră punctuația
            words = re.findall(r"[a-zA-ZăâîșțĂÂÎȘȚ]+", line)
            for word in words:
                self.trie.insert(word.lower())

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self.load_text(f.read())


    def search_pattern(self, pattern: str,
                        case_sensitive: bool = False,
                        show_highlight: bool = True) -> None:
        if not self.lines:
            print("  [!] Corpusul este gol. Încarcă mai întâi un text.")
            return

        if not pattern:
            print("  [!] Pattern-ul nu poate fi gol.")
            return

        # afisam si failure function
        pat_lower = pattern if case_sensitive else pattern.lower()
        failure = compute_failure(pat_lower)
        print(f"\n  Failure function pentru '{pat_lower}': {failure}")

        matches = kmp_search_in_corpus(self.lines, pattern, case_sensitive)

        if not matches:
            print(f"\n  Nicio apariție găsită pentru '{pattern}'.")
            return

        print(f"\n  {len(matches)} apariție/aparitii pentru '{pattern}':\n")
        for match in matches:
            print(f"  → Linia {match.line_number:>3}, coloana {match.column:>3}:")
            print(f"     {match.line_text}")
            if show_highlight:
                print(f"     {highlight_match(match.line_text, match.column, len(pattern))}")




    def search_word(self, word: str) -> None:
        freq = self.trie.search(word)
        if freq > 0:
            print(f"\n  Cuvântul '{word}' există în index. Frecvență: {freq}.")
        else:
            print(f"\n  Cuvântul '{word}' NU există în index.")




    def autocomplete(self, prefix: str) -> None:
        results = self.trie.starts_with(prefix)
        if results:
            print(f"\n  {len(results)} cuvinte cu prefixul '{prefix}':")
            for word in results:
                print(f"    • {word}")
        else:
            print(f"\n  Niciun cuvânt cu prefixul '{prefix}'.")




    def show_all_words(self) -> None:
        words = self.trie.get_all_words()
        if not words:
            print("\n  Indexul este gol.")
            return

        print(f"\n  {len(words)} cuvinte indexate (ordine alfabetică):\n")
        col_width = max(len(w) for w in words) + 4
        cols = max(1, 60 // col_width)
        for i, word in enumerate(words):
            end = "\n" if (i + 1) % cols == 0 else ""
            print(f"  {word:<{col_width}}", end=end)
        print()


    def show_stats(self) -> None:
        total_words = sum(
            len(re.findall(r"[a-zA-ZăâîșțĂÂÎȘȚ]+", line))
            for line in self.lines
        )
        print(f"\n  ── Statistici corpus ──────────────────")
        print(f"  Linii:              {len(self.lines)}")
        print(f"  Cuvinte totale:     {total_words}")
        print(f"  Cuvinte distincte:  {self.trie.word_count}")
        print(f"  ───────────────────────────────────────")


# texte pt demo


SAMPLE_CORPUS_1 = """Algoritmii de căutare sunt fundamentali în informatică.
Algoritmul KMP (Knuth-Morris-Pratt) caută un pattern într-un text în timp liniar.
Structura de date Trie permite căutarea rapidă a cuvintelor după prefix.
Motorul de căutare combină Trie și KMP pentru indexare și regăsire eficientă.
Complexitatea algoritmului KMP este O(n + m), unde n este lungimea textului.
Trie-ul are complexitate O(m) pentru inserție și căutare, unde m este lungimea cuvântului.
Funcția de eșec din KMP evită comparațiile redundante în timpul căutării.
Structurile de date avansate sunt esențiale pentru motoarele de căutare moderne."""

SAMPLE_CORPUS_2 = """Python este un limbaj de programare de nivel înalt.
Structurile de date sunt componente esențiale ale oricărui program.
Arborele binar de căutare permite operații de inserție și căutare eficiente.
Tabela de dispersie oferă acces în timp mediu O(1) pentru operații de bază.
Programarea dinamică rezolvă probleme prin descompunere în subprobleme.
Algoritmii de sortare includ QuickSort, MergeSort și HeapSort.
Graful este o structură de date folosită pentru modelarea relațiilor.
Parcurgerea în adâncime (DFS) și în lățime (BFS) sunt tehnici fundamentale."""
