"""
trie.py — Implementare Trie
Motor de căutare în texte 

Structura Trie stochează cuvinte caracter cu caracter, permițând:
  - inserție eficientă de cuvinte
  - căutare exactă
  - căutare după prefix (autocomplete)
  - listarea tuturor cuvintelor indexate
"""


class TrieNode:
    """
    Nodul unui Trie.
    Fiecare nod reține:
      - children: dicționar {caracter -> TrieNode}
      - is_end:   True dacă nodul marchează sfârșitul unui cuvânt valid
      - count:    de câte ori apare cuvântul în corpus (incrementat la inserție)
    """

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.count: int = 0  # frecvența cuvântului în corpus


class Trie:

    def __init__(self):
        self.root = TrieNode()
        self._word_count = 0  # numărul total de cuvinte distincte

    # Inserție

    def insert(self, word: str) -> None:
        """
        Inserează un cuvânt în Trie.
        Parcurge (sau creează) noduri pentru fiecare caracter.
        La final marchează nodul ca end-of-word și incrementează count.

        Complexitate timp: O(|word|)
        Complexitate spațiu: O(|word|)  în cel mai rău caz (cuvânt complet nou)
        """
        word = word.lower()
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # creăm nod nou dacă lipsește
            node = node.children[char]

        if not node.is_end:
            # cuvânt nou distinct
            self._word_count += 1

        node.is_end = True
        node.count += 1  # cuvântul mai apare o dată în corpus

    
    # Căutare exactă


    def search(self, word: str) -> int:
        """
        Caută un cuvânt exact în Trie.
        Returnează frecvența cuvântului (0 dacă nu există).

        Complexitate timp: O(|word|)
        """
        word = word.lower()
        node = self._traverse(word)

        if node is None or not node.is_end:
            return 0
        return node.count


    # Căutare prefix (autocomplete)
    

    def starts_with(self, prefix: str) -> list[str]:
        """
        Returnează lista tuturor cuvintelor din Trie care încep cu `prefix`.
        Utilizat pentru funcționalitatea de autocomplete.

        Complexitate timp: O(|prefix| + k)
          unde k = numărul total de caractere ale cuvintelor găsite
        """
        prefix = prefix.lower()
        node = self._traverse(prefix)

        if node is None:
            return []  # prefixul nu există în Trie

        results: list[str] = []
        self._collect_words(node, prefix, results)
        return sorted(results)  # sortăm alfabetic pentru output curat


    # Toate cuvintele
    

    def get_all_words(self) -> list[str]:
        """
        Returnează toate cuvintele indexate în Trie (ordine alfabetică).

        Complexitate timp: O(N) unde N = numărul total de caractere stocate
        """
        results: list[str] = []
        self._collect_words(self.root, "", results)
        return sorted(results)


    # Ștergere
    

    def delete(self, word: str) -> bool:
        """
        Șterge un cuvânt din Trie.
        Returnează True dacă cuvântul a existat și a fost șters.

        Complexitate timp: O(|word|)
        """
        word = word.lower()
        return self._delete_helper(self.root, word, 0)

    def _delete_helper(self, node: TrieNode, word: str, depth: int) -> bool:
        """Recursiv: șterge cuvântul și curăță nodurile orfane."""
        if depth == len(word):
            if not node.is_end:
                return False  # cuvântul nu există
            node.is_end = False
            node.count = 0
            self._word_count -= 1
            return len(node.children) == 0  # semnalăm că nodul poate fi eliminat

        char = word[depth]
        if char not in node.children:
            return False  # cuvântul nu există

        should_delete_child = self._delete_helper(node.children[char], word, depth + 1)

        if should_delete_child:
            del node.children[char]
            # putem șterge și nodul curent dacă nu are alt scop
            return len(node.children) == 0 and not node.is_end

        return False


    # Utilități interne
    

    def _traverse(self, prefix: str) -> TrieNode | None:
        """
        Traversează Trie-ul urmând caracterele din `prefix`.
        Returnează nodul de la finalul prefixului, sau None dacă nu există.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, current: str, results: list[str]) -> None:
        """
        DFS recursiv — colectează toate cuvintele complete din subarborele `node`.
        `current` acumulează calea curentă de caractere.
        """
        if node.is_end:
            results.append(current)  # am găsit un cuvânt complet

        for char, child in node.children.items():
            self._collect_words(child, current + char, results)


    # Proprietăți
    

    @property
    def word_count(self) -> int:
        """Numărul de cuvinte distincte stocate în Trie."""
        return self._word_count

    def __repr__(self) -> str:
        return f"Trie(cuvinte_distincte={self._word_count})"
