# RustyBun

Eksperyment migracji Bun z Zig do Rust: najpierw projekt procesu i kontraktów, następnie mierzalny pilotaż z Codexem w ramach abonamentu.

**Status: przygotowanie procesu.** Role, prompty i protokół przeglądu są kandydatem v0.1, nie zatwierdzonym ani uruchomionym systemem agentowym. Nie wykonano jeszcze analizy architektury pełnego Buna, kompilacji baseline ani migracji.

## Zacznij tutaj

- [START-HERE.md](START-HERE.md) — instrukcja dla kolejnego modelu i operatora.
- [Neutralny brief](docs/project-brief.md) — cel, ograniczenia i niewiadome, bez narzucania topologii agentów.
- [Plan wykonania](docs/experiment-plan.md) — etapy, produkty i bramki akceptacji.
- [Role](agents/roles.md) i [wspólny kontrakt](agents/contract.md) — odpowiedzialności i granice uprawnień.
- [Prompty](prompts/) — osobne zadania dla każdej roli i niezależnych recenzentów.
- [Weryfikacja w czystym kontekście](docs/clean-context-review.md) — co dokładnie przekazać recenzentowi.
- [Dziennik prezentacji](docs/presentation-journal.md) — decyzje z rozmowy, korekty, hipotezy i materiał narracyjny.

## Baseline i źródła

Kod do niezależnej analizy: `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.
Commit referencyjny z instrukcją migracji: `46d3bc29f270fa881dd5730ef1549e88407701a5`.
Drugi dodaje `docs/PORTING.md` i `scripts/port-batch.ts`, bez zmian implementacji Buna. To odtwarzalna granica Phase A, nie dowód dokładnego stanu pierwszej prywatnej sesji autora.

[Analiza wyboru](docs/upstream-baseline-analysis.md) · [konfiguracja SHA](upstream/bun-baseline.env) · [indeks materiałów](sources/README.md).

## Przygotowanie wejścia

```bash
# Uruchom z katalogu RustyBun. Wymagane: Python 3.10+ i Git.
python3 -m unittest discover -s tests -v
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
# Opcjonalnie: checkout samego kodu do dalszej analizy (Linux/macOS/WSL/Git Bash).
bash scripts/bootstrap-bun-baseline.sh
```

Pakiet zawiera `TASK.md`, `MANIFEST.json` oraz jawnie wybrane wejścia. Nie uruchamia modelu, nie loguje do usług i nie zużywa płatnego API. Rzeczywistą izolację zapewnia operator: osobna sesja i sandbox bez dostępu do głównego repo, historii rozmowy oraz dodatkowej pamięci.

`sources/` pozostaje archiwum; `agents/`, `prompts/`, `workflow/` i `templates/` opisują nasz proces; `results/` przechowuje jawnie oznaczone wyniki. Źródłowe licencje obowiązują w odpowiednich katalogach. Ten commit nie nadaje nowej licencji całemu repo.
