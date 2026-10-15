# trie - insert, cautare, prefix (autocomplete), stergere
class TrieNode:

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.count: int = 0  # de cate ori apare


class Trie:

    def __init__(self):
        self.root = TrieNode()
        self._word_count = 0  # cuvinte distincte

    # O(len(word))

    def insert(self, word: str) -> None:
        word = word.lower()
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end:
            self._word_count += 1

        node.is_end = True
        node.count += 1


    # returneaza frecventa, 0 daca nu e


    def search(self, word: str) -> int:
        word = word.lower()
        node = self._traverse(word)

        if node is None or not node.is_end:
            return 0
        return node.count


    # autocomplete


    def starts_with(self, prefix: str) -> list[str]:
        prefix = prefix.lower()
        node = self._traverse(prefix)

        if node is None:
            return []

        results: list[str] = []
        self._collect_words(node, prefix, results)
        return sorted(results)




    def get_all_words(self) -> list[str]:
        results: list[str] = []
        self._collect_words(self.root, "", results)
        return sorted(results)




    def delete(self, word: str) -> bool:
        word = word.lower()
        return self._delete_helper(self.root, word, 0)

    def _delete_helper(self, node: TrieNode, word: str, depth: int) -> bool:
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            node.count = 0
            self._word_count -= 1
            return len(node.children) == 0  # nodul poate fi sters

        char = word[depth]
        if char not in node.children:
            return False

        should_delete_child = self._delete_helper(node.children[char], word, depth + 1)

        if should_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end

        return False




    def _traverse(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, current: str, results: list[str]) -> None:
        if node.is_end:
            results.append(current)

        for char, child in node.children.items():
            self._collect_words(child, current + char, results)




    @property
    def word_count(self) -> int:
        return self._word_count

    def __repr__(self) -> str:
        return f"Trie(cuvinte_distincte={self._word_count})"
