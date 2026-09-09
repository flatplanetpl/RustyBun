# Przygotowanie procesu RustyBun v0.2

Status: **PROCESS_PREPARED_NOT_APPROVED; przegląd Damiana PENDING; G1–G5 PENDING**.

Podstawa: zaakceptowany plan po D01–D08 i polecenie „Implement the plan”. Baza: `b1ba7a9f946cd0de6c1c79869faeaa110ac96782`, czysty Git przed zmianami. To jeden lokalny commit przygotowawczy, bez push. Hash commita jest podany w końcowym raporcie wykonawcy; poniższy manifest wiąże testowane pliki z ich treścią bez samoodnoszącego się hasha commita.

## Wynik i granice

**FACT:** aktywne dokumenty, prompty i konfiguracja opisują jeden wycinek, jedną główną sesję, zadania kolejno i jednego aktywnego writera. Operator odpowiada za baseline/verifier przed G3. Review jest obowiązkowe, jego rodzaj nie został wybrany za operatora; samoprzegląd pozostaje jawny. Szablony zawierają budżet z rezerwą, interwencje i checkpoint. Liczbowe wartości budżetu pozostają null; usunięto domyślne dwa review i dwie rundy poprawek.

Nie zmieniano skryptów, CLI, profili ani formatu 0.1 manifestu eksportera. Nowa konfiguracja i szablony mają wersję 0.2. Wykorzystano istniejące generyczne kopiowanie rekordów, bez adaptera, fallbacka czy nowego runnera. Pipeline opisuje warunki; operator egzekwuje je na podstawie dowodów. Wszystkie bramki zachowują brak zatwierdzenia.

**SELF_REVIEW:** zmiany przygotował i sprawdził koordynator w tej samej sesji; nie jest to niezależna runda review ani odbiór przez Damiana. Nowych agentów nie uruchomiono. Mniejszy koszt uproszczonego procesu pozostaje hipotezą.

## D01–D08 → zmiany → sprawdzenia

| Decyzja | Zastosowanie w aktywnych artefaktach | Dowód przygotowania |
|---|---|---|
| D01 | plan, Architect/Planner i raport ograniczają analizę do potrzeb jednego wycinka; pipeline max_units=1 | test jednej sekwencji i kontrola treści; brak wyboru kodu Buna |
| D02 | role są odpowiedzialnościami, review bez domyślnego A/B; rodzaj, wykonawca i niezależność w szablonach | test domyślnej ścieżki, rozdzielenia opcjonalnych zadań i pustego planu review |
| D03 | operator Damian jako właściciel; etap baseline-verifier przed Planner/G3; wymagania także przed Implementerem | test zależności przed G3 i implementacją; verification.status=NOT_RUN |
| D04 | wymagania wrong_result, empty_test_set, missing_output, timeout, wrong_implementation; manifest i hashe protokołu | test kompletności wymaganych kontroli i niezapisanych wyników; brak rzeczywistych kontroli Buna |
| D05 | limit/rezerwa dla czasu, uwagi i zasobu modelu; przygotowanie w budżecie; warunek dostępnej rezerwy; brak domyślnej liczby poprawek | test niezatwierdzonych limitów/rezerw i zależności rozpoczęcia zmiany |
| D06 | opis wpisów interwencji; checkpoint i poprzedni rekord; nowy hash wymaga review/parity; skumulowane zużycie | test pól checkpointu i zachowania metadanych przez helpery; praktyczne wznowienie nie było wykonywane |
| D07 | ograniczona analiza; blind-architect/architecture-review wyłącznie w optional_tasks; executable_runner=false | test domyślnej ścieżki, referencji i granic wejść |
| D08 | aktualne README/START-HERE, jawna adnotacja do decyzji, journal dopisany z zachowaniem historii; osobne comparative review | kontrola linków i niezmienności dawnych artefaktów; pending gate tests |

## Wykonane sprawdzenia

- **104/104 testy OK**, czas raportowany przez unittest: **8.141 s**. Polecenie: `python3 -m unittest discover -s tests -v`. [Pełny log](test-output.txt), [czas, środowisko i exit code](test-run.json).
- Dodano 12 testów do wcześniejszych 92. Pierwsze uruchomienie 11 testów nowego modułu na starych kontraktach zakończyło się `FAILED (failures=6, errors=8)` (liczby uwzględniają subtesty); ujawniło stare wersje, brak pól i zależności. Po zmianach nowy moduł przeszedł, następnie cała suite wraz z dodatkowym testem helpera design-review.
- Testy korzystają z kopii bieżących wejść w tymczasowym repo Git, rzeczywistego eksportera i helperów. Eksportują design-review i comparative-review, sprawdzają hashe oraz zachowanie metadanych v0.2. Nie tworzą operacyjnego pakietu porównawczego z zatwierdzonymi wejściami poprzednich rund. Wywołania klienta i logowania w istniejącej suite są symulowane.
- Kontrola manifestów: **40 plików archiwizacji + 34 wejścia**, zero rozbieżności. Dodatkowo **87/87 dawnych plików results/, sources/, upstream/** zgodnych z bazowymi blobami Git. [Pełny wykaz hashy](integrity.json).
- JSON, lokalne odnośniki w zmienionych dokumentach i odwołania pipeline/pakietów sprawdzono; `git diff --check` bez błędów. [Zakres kontroli spójności](consistency.json). Wyszukiwanie pozostałości v0.1/A/B rozróżnia zakazy domyślnych wymagań i jawnie historyczny zapis od aktywnej reguły; nie przepisuje archiwów.
- Ograniczony przegląd publikacyjny nowego raportu, metadanych i logu testów nie wykazał wartości credentiali ani prywatnych zapisów sesji. Nie odczytywano cache logowania. To przegląd wskazanego zestawu, nie gwarancja wykrycia każdego rodzaju danych wrażliwych.

## Niewykonane etapy i otwarte decyzje

Nie wykonano nowego independent/design/comparative review, analizy Buna, wyboru wycinka, przygotowania oryginału, implementacji verifiera, jego realnych kontroli negatywnych, portu, parity, runtime sandbox testu ani praktycznego wznowienia pilota. Testy narzędzi i kontrola danych nie dowodzą gotowości G3 ani skuteczności procesu. Nie użyto płatnego API, nowych agentów ani push.

Następny krok: przegląd przygotowanego diffu z Damianem, następnie osobne przygotowanie wymaganej rundy comparative review przed G1. Trzeba wskazać i zamrozić jej wcześniejsze raporty/propozycję, wejścia, zakres, rekord i warunki wykonania. Sam eksport konfiguracji nie spełnia tego warunku.

Do ustalenia pozostają: wycinek i środowisko; model/ustawienia; jednostka pomiaru, budżet, rezerwa i liczba poprawek; rodzaj, wykonawca i zakres review zależny od ryzyka. Żadnej z tych decyzji nie wpisano za operatora. Historyczne COMPLETE, LAUNCH_ERROR i EXPLORATORY; INDEPENDENCE UNVERIFIED pozostają niezmienione.

## Pełna lista plików w commicie

- [AGENTS.md](../../AGENTS.md)
- [README.md](../../README.md)
- [START-HERE.md](../../START-HERE.md)
- [agents/contract.md](../../agents/contract.md)
- [agents/roles.md](../../agents/roles.md)
- [docs/clean-context-review.md](../../docs/clean-context-review.md)
- [docs/decisions/2026-09-09-pilot-v0.2.md](../../docs/decisions/2026-09-09-pilot-v0.2.md)
- [docs/design-review-command.md](../../docs/design-review-command.md)
- [docs/experiment-plan.md](../../docs/experiment-plan.md)
- [docs/independent-review-command.md](../../docs/independent-review-command.md)
- [docs/preflight-start.md](../../docs/preflight-start.md)
- [docs/presentation-journal.md](../../docs/presentation-journal.md)
- [prompts/01-architect.md](../../prompts/01-architect.md)
- [prompts/02-planner.md](../../prompts/02-planner.md)
- [prompts/03-implementer.md](../../prompts/03-implementer.md)
- [prompts/04-reviewer.md](../../prompts/04-reviewer.md)
- [prompts/05-fixer.md](../../prompts/05-fixer.md)
- [prompts/06-referee-operator.md](../../prompts/06-referee-operator.md)
- [prompts/08-design-review.md](../../prompts/08-design-review.md)
- [prompts/09-comparative-review.md](../../prompts/09-comparative-review.md)
- [prompts/10-architecture-review.md](../../prompts/10-architecture-review.md)
- [results/tooling-process-v02-20260909T174417Z/MANIFEST.json](../../results/tooling-process-v02-20260909T174417Z/MANIFEST.json)
- [results/tooling-process-v02-20260909T174417Z/consistency.json](../../results/tooling-process-v02-20260909T174417Z/consistency.json)
- [results/tooling-process-v02-20260909T174417Z/integrity.json](../../results/tooling-process-v02-20260909T174417Z/integrity.json)
- [results/tooling-process-v02-20260909T174417Z/report.md](../../results/tooling-process-v02-20260909T174417Z/report.md)
- [results/tooling-process-v02-20260909T174417Z/test-output.txt](../../results/tooling-process-v02-20260909T174417Z/test-output.txt)
- [results/tooling-process-v02-20260909T174417Z/test-run.json](../../results/tooling-process-v02-20260909T174417Z/test-run.json)
- [templates/architecture-report.md](../../templates/architecture-report.md)
- [templates/migration-unit.json](../../templates/migration-unit.json)
- [templates/review-report.md](../../templates/review-report.md)
- [templates/run-record.json](../../templates/run-record.json)
- [tests/test_design_review.py](../../tests/test_design_review.py)
- [tests/test_workflow_contract.py](../../tests/test_workflow_contract.py)
- [workflow/bundles.json](../../workflow/bundles.json)
- [workflow/pipeline.json](../../workflow/pipeline.json)
