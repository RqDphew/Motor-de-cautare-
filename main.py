"""
 Motor de căutare în texte
"""

from engine import TextSearchEngine, SAMPLE_CORPUS_1, SAMPLE_CORPUS_2


# Constante vizuale

LINE  = "─" * 50
DLINE = "═" * 50


def print_header():
    print(f"\n{DLINE}")
    print("   Motor de Căutare în Texte")
    print("   Trie + KMP  |  SDA — UVT")
    print(f"{DLINE}")


def print_menu():
    print(f"\n{LINE}")
    print("  MENIU PRINCIPAL")
    print(LINE)
    print("  1. Încarcă corpus demo (texte predefinite)")
    print("  2. Introdu propriul text")
    print("  3. Caută pattern în text (KMP)")
    print("  4. Caută cuvânt exact (Trie)")
    print("  5. Autocomplete după prefix (Trie)")
    print("  6. Afișează toate cuvintele indexate (Trie)")
    print("  7. Statistici corpus")
    print("  8. Demo complet automat")
    print("  0. Ieșire")
    print(LINE)


def load_demo_corpus(engine: TextSearchEngine):
    """Meniu secundar: alege unul din corpusurile predefinite."""
    print(f"\n{LINE}")
    print("  Corpusuri disponibile:")
    print("  1. Algoritmi și structuri de date")
    print("  2. Python și programare generală")
    print(LINE)
    choice = input("  Alege corpus [1/2]: ").strip()

    if choice == "1":
        engine.load_text(SAMPLE_CORPUS_1)
        print("\n  ✓ Corpus 1 încărcat cu succes.")
    elif choice == "2":
        engine.load_text(SAMPLE_CORPUS_2)
        print("\n  ✓ Corpus 2 încărcat cu succes.")
    else:
        print("  [!] Opțiune invalidă.")
        return

    engine.show_stats()


def load_custom_text(engine: TextSearchEngine):
    """Permite utilizatorului să introducă text de la tastatură."""
    print("\n  Introdu textul (termină cu o linie goală):")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break

    if lines:
        engine.load_text("\n".join(lines))
        print(f"\n  ✓ Text încărcat: {len(lines)} linii.")
        engine.show_stats()
    else:
        print("  [!] Niciun text introdus.")


def run_full_demo(engine: TextSearchEngine):
    """Demo automat: încarcă corpus și rulează toate operațiile."""
    print(f"\n{DLINE}")
    print("  DEMO AUTOMAT COMPLET")
    print(DLINE)

    # 1. Încarcă corpus
    print("\n[1] Încărcare corpus demo...")
    engine.load_text(SAMPLE_CORPUS_1)
    engine.show_stats()

    # 2. KMP search
    print(f"\n{LINE}")
    print("[2] Căutare KMP: pattern = 'kmp'")
    engine.search_pattern("kmp")

    print(f"\n{LINE}")
    print("[3] Căutare KMP: pattern = 'căutare'")
    engine.search_pattern("căutare")

    # 3. Trie exact search
    print(f"\n{LINE}")
    print("[4] Căutare cuvânt exact în Trie: 'algoritm'")
    engine.search_word("algoritm")

    print("[5] Căutare cuvânt exact în Trie: 'python'")
    engine.search_word("python")

    # 4. Autocomplete
    print(f"\n{LINE}")
    print("[6] Autocomplete prefix 'căut':")
    engine.autocomplete("căut")

    print("\n[7] Autocomplete prefix 'alg':")
    engine.autocomplete("alg")

    # 5. Toate cuvintele
    print(f"\n{LINE}")
    print("[8] Toate cuvintele indexate:")
    engine.show_all_words()

    print(f"\n{DLINE}")
    print("  Demo complet finalizat.")
    print(DLINE)



def main():
    print_header()
    engine = TextSearchEngine()

    while True:
        print_menu()
        choice = input("  Alege opțiunea: ").strip()

        if choice == "0":
            print("\n  La revedere!\n")
            break

        elif choice == "1":
            load_demo_corpus(engine)

        elif choice == "2":
            load_custom_text(engine)

        elif choice == "3":
            if not engine.lines:
                print("\n  [!] Încarcă mai întâi un corpus (opțiunile 1 sau 2).")
            else:
                pattern = input("\n  Introdu pattern-ul: ").strip()
                cs = input("  Case-sensitive? [d/N]: ").strip().lower() == "d"
                engine.search_pattern(pattern, case_sensitive=cs)

        elif choice == "4":
            if not engine.lines:
                print("\n  [!] Încarcă mai întâi un corpus.")
            else:
                word = input("\n  Introdu cuvântul: ").strip()
                engine.search_word(word)

        elif choice == "5":
            if not engine.lines:
                print("\n  [!] Încarcă mai întâi un corpus.")
            else:
                prefix = input("\n  Introdu prefixul: ").strip()
                engine.autocomplete(prefix)

        elif choice == "6":
            engine.show_all_words()

        elif choice == "7":
            engine.show_stats()

        elif choice == "8":
            run_full_demo(engine)

        else:
            print("\n  [!] Opțiune invalidă. Alege un număr între 0 și 8.")

        input("\n  [Apasă Enter pentru a continua...]")


if __name__ == "__main__":
    main()
