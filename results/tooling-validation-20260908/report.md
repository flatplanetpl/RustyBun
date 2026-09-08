# Weryfikacja narzędzi przygotowawczych — 2026-09-08

Zakres: eksporter pakietów i składnia bootstrapu. To NIE jest wynik niezależnej oceny LLM, builda Buna ani migracji.

## Wykonane sprawdzenia

- `python3 -m unittest discover -s tests -v` — 8/8 PASS. Testy offline na małych lokalnych repo Git: allowlista, SHA-256, brak niezatwierdzonych zmian w eksporcie, odmowa nadpisania, wymaganie kodu dla Architekta, wykluczenie instrukcji/historii/symlinków, błędne ścieżki/ref, brakujące wejście i powtarzalność manifestu. Nie wymagają połączenia z modelem.
- `bash -n scripts/bootstrap-bun-baseline.sh` — PASS (tylko składnia).
- Parsowanie nowych JSON i kontrola wszystkich odwołań pipeline → prompt — PASS. Bramki G1–G5 pozostają PENDING.

Pełny wynik testów: [test-output.txt](test-output.txt). Python: 3.13.5. Git: git version 2.47.3. Środowisko: Linux. Nie wykonano testów na Windows/macOS ani Pythonie 3.10.

Pierwsza lokalna próba startu testów wykryła brak utworzonego katalogu scripts/ w środowisku przygotowania. Katalog i pliki uzupełniono, następnie pełny zestaw uruchomiono ponownie z powyższym wynikiem.

## Hashe sprawdzonych plików

- `scripts/build-context-pack.py`: `de8b632148cbcee11092a3fa89578f58198067bee24ed302df8adcafbdcae73e`
- `scripts/bootstrap-bun-baseline.sh`: `da58f66beccd7bcfa3ab85e4dac49ef2a23fc3efacdd7adfa8437652bc5a5a6d`
- `tests/test_context_pack.py`: `ff06d1bb0f4b31ba03e2d9f2dcb330c305659de3e050c7fd53c1e6cc4070e4f8`

## Ograniczenia

Pełnego checkoutu Buna nie pobrano: bezpośredni Git w tym środowisku nie rozwiązywał DNS github.com. Eksport rzeczywistego Buna i pobranie historycznych zależności nie były testowane. Konektor GitHub pozwolił odczytać repo i przygotować zapis. Wynik testów fixture'ów nie jest dowodem pełnej izolacji środowiska agenta.

Pełny runner agentów nie jest zaimplementowany; workflow/pipeline.json to opis procesu. Eksporter nie uruchamia modelu i nie egzekwuje sandboxa. Brak wyników quota, kosztu, czasu builda i parity.
