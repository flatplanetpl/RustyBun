# Materiały referencyjne — zakres i pochodzenie

Ten katalog zawiera WYBÓR materiałów, nie kompletne checkouty trzech projektów. Nie wolno uruchamiać skopiowanego promptu, zakładając, że jego wszystkie zależności są tutaj dostępne. Pliki SOURCE.md wskazują deklarowane rewizje; przed badaniem dokładnej reprodukcji trzeba również sprawdzić identyczność bajtów z upstream.

| Źródło | Rola | Ograniczenie |
|---|---|---|
| oven-sh/bun, commit-46d3bc29 | PORTING.md i port-batch.ts, autentyczne materiały z historii Buna | nie pełny harness ani kompletny snapshot; port-batch odwołuje się do manifestu w /tmp |
| anthropics/code-migration-kit-with-claude-code | wybrane prompty i RULEBOOK, uogólniony zestaw migracyjny | nie zapis oryginalnych sesji; brak kompletnego runnera, wszystkich skryptów i przykładów |
| Lumafy/sumner-method | społecznościowe opisy ról i koncept orkiestracji | multi-agent-orchestration.ts ma stuby i validateFix=true; nie produkcyjny runner |

Istniejący README w katalogu Lumafy jest krótką lokalną notą, nie pełnym upstream README. Nie utożsamiaj wszystkich plików archiwum z niezmodyfikowanym mirrorem. Obecny etap nie wykonuje pełnego audytu bajtowej zgodności ani nie zmienia historycznych kopii.

Źródła pierwotne do późniejszego uzupełnienia: https://github.com/oven-sh/bun/commit/46d3bc29f270fa881dd5730ef1549e88407701a5 ; https://github.com/anthropics/code-migration-kit-with-claude-code/tree/cf91c9d5068d9aaf95a36164169f08c3e636c909 ; https://github.com/Lumafy/sumner-method/tree/323b94fbdbfbf9b445c4b9a881a5f8afc05c3f4e .

Nie podawaj tych materiałów do rund independent-design, design-review ani blind Architect. Ujawnienie następuje dopiero w comparative-review. Licencje i pochodzenie zachowujemy przy kopiowaniu; samo umieszczenie materiału tutaj nie oznacza poparcia dla jego zaleceń.
