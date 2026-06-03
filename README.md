Motor de cautare in texte | Trie + KMP in Python
Built a text search engine from scratch in Python for my Advanced Data Structures course. No libraries, just raw implementations of two data structures that complement each other well.
What it does:

Indexes all words from a text corpus into a Trie for O(m) prefix search and autocomplete
Uses KMP to find every occurrence of a pattern across all lines, returning line number, column, and a visual highlight
CLI menu to run everything interactively

Why these two:
Trie handles anything prefix-related in O(m) regardless of corpus size. KMP guarantees O(n+m) pattern matching vs O(nm) for the naive approach — the difference comes from the failure function which avoids redundant comparisons by reusing already-matched prefixes.
