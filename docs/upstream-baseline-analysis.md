# Baseline Buna — dowody i sposób użycia

## Decyzja po przygotowaniu procesu v0.1

**Domyślne wejście do niezależnej analizy to surowy kod `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.** Commit `46d3bc29f270fa881dd5730ef1549e88407701a5` pozostaje referencją z instrukcją Phase A, a nie wejściem blind Architecta. To zmiana sposobu udostępniania wiedzy, nie zmiana implementacji wybranej do eksperymentu.

## Ustalona granica historyczna

W analizie zapisanej wcześniej w RustyBun (stan repo `a1527be0274985ba0e48144dbdd26b2340cd9440`) porównanie commitów wykazało:

- `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`, 2026-05-04 10:20:16 UTC — rodzic commita instrukcji.
- `46d3bc29f270fa881dd5730ef1549e88407701a5`, 2026-05-04 13:20:04 UTC — `docs: add Phase-A porting guide`.
- Różnica: dodane tylko `docs/PORTING.md` (576 linii) i `scripts/port-batch.ts` (46 linii), bez zmian implementacji Buna.
- Referencja należy do historii późniejszej gałęzi rewrite; porównanie z `6033d71077a2be04405e6c443bf9a30ccf34d293` wskazało ją jako merge-base.

Dowody możliwe do odtworzenia:

https://github.com/oven-sh/bun/compare/0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f...46d3bc29f270fa881dd5730ef1549e88407701a5

https://github.com/oven-sh/bun/commit/46d3bc29f270fa881dd5730ef1549e88407701a5

https://github.com/oven-sh/bun/pull/30412

## Dlaczego nie nowszy base PR-a

`0d9b296af33f2b851fcbf4df3e9ec89751734ba4` był według porównania 25 commitów dalej niż surowy snapshot. Zmieniał m.in. runtime, HTTP, sys, build i testy. Dla pierwszego kontrolowanego eksperymentu utrzymujemy wcześniejszy kod. Kolejny snapshot może być późniejszą próbą odporności, nie cichą podmianą baseline.

## Granice pewności

To mocno uzasadniona, publicznie odtwarzalna granica Phase A. Historia nie dowodzi dokładnego stanu dysku, lokalnych niezatwierdzonych plików ani kontekstu pierwszej sesji autora. Nie twierdzimy też, że wcześniej nie wykonywano analizy lub reorganizacji.

## Dwa rodzaje wejścia

- **Analiza niezależna:** surowy source SHA, eksport bez historii Git i znanych plików instrukcji. Brak materiałów poprzedniej migracji.
- **Porównanie/reprodukcja reguł:** ten sam kod implementacji, osobno udostępniony `PORTING.md` z referencyjnego SHA, jawny manifest wiedzy dodatkowej.

Nazwy Run A/Run B w wcześniejszych notatkach nie oznaczają wykonanych prób. Faktyczne run_id, wersję procesu, model, zakres i wyniki zapisujemy dopiero w results/. Żaden baseline nie został w ramach przygotowania v0.1 zbudowany ani przetestowany.
