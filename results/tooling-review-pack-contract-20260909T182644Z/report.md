# Korekta kontroli procesu w pakietach review

Status: **TOOLING_VERIFIED; SELF_REVIEW; odbiór Damiana i G1–G5 PENDING**.

Podstawa: [zaakceptowany plan 001](../../docs/plans/001-review-pack-process-contract.md)
i polecenie użytkownika wdrożenia wraz z jednym lokalnym commitem. Baza:
`874c55a8f85a0c080bd50bcf69aafca850988c6b`, czysty Git przed zmianami. Hash commita korekcyjnego jest w końcowym
raporcie wykonawcy; [manifest](MANIFEST.json) wiąże zmienione pliki z treścią,
bez samoodnoszącego się hasha commita. Commit bazy i wcześniejsze wyniki zachowano.

## Luka i korekta

**FACT:** przed zmianą rzeczywisty eksport każdego pakietu i wykonanie
`python3 -I -B -m unittest discover -s tests -p test_workflow_contract.py -v`
z katalogu `<export>/input` dawały `FAILED (failures=1, errors=2)`, exit 1.
[Design-review przed zmianą](before-design-review.txt),
[comparative-review przed zmianą](before-comparative-review.txt),
[metadane reprodukcji](reproduction.json). Kontrola całego repo wymagała materiałów
historycznych niedostarczanych design-review; fixture integracyjna wymagała także
narzędzi drugiej rundy niedostarczanych comparative-review. Dawny wynik 104/104
w repo jest prawdziwy, ale nie dowodził uruchamialności modułu po eksporcie.

`tests/test_process_contract.py` zawiera osiem niezmienionych testów kontraktu
(identyczne AST) i wydzieloną kontrolę referencji promptów/zadań. Używa biblioteki
standardowej oraz dostarczonych konfiguracji, szablonów i promptów.
`tests/test_workflow_contract.py` zachowuje kompletność repo, granice wejść,
kontrole hashy eksportu i zachowania metadanych preflight. Dodano sześć regresji
wykonujących kontrole w osobnym procesie na rzeczywistych eksportach i ich kopiach.
Nowy test uruchomienia napisano przed podziałem; nie przechodził dla obu pakietów.

W `workflow/bundles.json` zmieniają się wyłącznie dwa wpisy nazwy modułu. Pozostała
konfiguracja, granice wejść, skrypty, CLI, schematy JSON i bramki są niezmienione.
Nie dodano runnera ani fallbacków. Przenośna kontrola nie próbuje odczytywać plików
innych pakietów na podstawie pełnej konfiguracji allowlist.

## Wykonane polecenia i wyniki

| Kontrola | Wynik i dowód |
|---|---|
| `python3 -m unittest discover -s tests -p 'test_*contract.py' -v` | 18/18 OK po podziale, 11.359 s; zapis terminala sesji. Następnie doprecyzowano asercję przyczyny brakującego pliku i sprawdzono pełną suite. |
| `python3 -m unittest discover -s tests -v` | **111/111 OK**, 22.116 s, exit 0; [pełny log](test-output.txt), [środowisko/czas](test-run.json). |
| `python3 -I -B -m unittest discover -s tests -p test_process_contract.py -v` w `<export>/input` | **9/9 OK w każdym pakiecie**, exit 0, brak zmian wejść; [design-review](design-review-checks.txt), [comparative-review](comparative-review-checks.txt). |
| To samo polecenie na kopiach z kontrolowanymi mutacjami | **26/26 odrzuceń**, każde exit 1 i oczekiwany błąd/asercja; [lista uruchomień](package-runs.json), [odbiór sześciu testów integracji](package-acceptance.txt). |
| Kontrola SHA-256 i bajtów względem bazy/manifestów | **93/93** wcześniejsze pliki results/sources/upstream, **40/40** pliki archiwum, **34/34** wejścia; zero rozbieżności. [Integralność](integrity.json). |
| JSON, lokalne odnośniki, `git diff --check` | Dokładny zakres, liczby i wyniki w [kontroli spójności](consistency.json). |

104 → 111 oznacza sześć nowych regresji oraz rozdzielenie jednego testu referencji
na dwa. Asercje poprzedniego kontraktu są zachowane. Osobny zapis odbioru korzysta
z tej samej klasy integracji i zapisuje stdout/stderr wszystkich 28 procesów:
dwa poprawne pakiety i 26 mutacji. Nie podmienia zachowania eksportera ani Pythona.

Pierwszy `git diff --cached --check` obejmujący nowe pliki wykrył 12 końcowych
spacji emitowanych przez unittest przy subtestach. Z czytelnych kopii `.txt`
usunięto tylko końcowe spacje/tabulatory. Dokładne pierwotne logi z etykietami
przypadków zachowano bez zmiany bajtów po dekompresji:
[design-review raw](design-review-checks.raw.txt.gz),
[comparative-review raw](comparative-review-checks.raw.txt.gz).
Końcowa kontrola diffu obejmuje wszystkie nowe pliki. Wyniki testów nie zmieniły się.

| Mutacja na kopii każdego pakietu | Liczba odrzuceń łącznie |
|---|---:|
| Usunięcie pipeline, bundles, migration-unit lub run-record | 8 |
| `review_policy.required=false` lub `review.required=false` w szablonie jednostki | 4 |
| `max_active_writers=2` | 2 |
| Usunięcie `baseline:validated` osobno z planner/implementer/referee | 6 |
| Usunięcie `verifier:validated` osobno z planner/implementer/referee | 6 |

Eksporty pochodzą z tymczasowych repo Git zawierających kopię bieżących wejść;
[manifest design-review](design-review-MANIFEST.json) i
[manifest comparative-review](comparative-review-MANIFEST.json) zapisują ich hashe.
`process_sha` tych fixture nie jest hashem commita RustyBun ani rundy operacyjnej.
Nie zachowujemy tymczasowych repo/eksportów; manifesty i logi są dowodami testów.
`-I` izoluje ustawienia importu Pythona, a `-B` wyłącza bytecode; nie jest to
izolacja dostępu do systemu plików. Testy te nie wymagają odczytów z checkoutu rodzica.

## Zachowanie historii i zakres odbioru

Poprzedni manifest przygotowania sprawdzono dla 34 opisanych plików **w bazowym
commicie**, ponieważ aktywne dokumenty mają teraz nową wersję. Skrypty i historia
journal są zachowane. Archiwalne COMPLETE, LAUNCH_ERROR i etykiety niezależności
pozostają bez zmian. Nowe logi sprawdzono pod kątem credentiali i prywatnych sesji;
zawierają ścieżki lokalnych fixture i repo, bez dostępu do cache logowania.

**SELF_REVIEW:** wdrożenie i kontrola w jednej sesji koordynatora; brak dodatkowych
agentów i niezależnego przeglądu. Akceptacja Damiana pozostaje PENDING.
**UNKNOWN:** gotowość środowiska pilota, wycinek, model/ustawienia, budżet/rezerwa,
liczba poprawek i konkretny plan review; te wartości wymagają osobnych ustaleń.

Nie wykonano comparative review ani pozostałych rund modelu, baseline Buna,
verifiera Buna i jego kontroli, migracji, parity, pomiaru kosztu pilota, testu
sandboxa ani zdalnej publikacji. Pełna suite zawiera symulowane wywołania klienta.
Testy konfiguracji nie dowodzą G3 i nie zatwierdzają G1–G5. Comparative review
pozostaje osobnym krokiem przed G1.

## Zmienione pliki

Lista obejmuje zmiany produktu, dokumentacji i nowe dowody; wcześniejsze katalogi
wyników pozostają nietknięte.

- [README.md](../../README.md)
- [START-HERE.md](../../START-HERE.md)
- [docs/clean-context-review.md](../../docs/clean-context-review.md)
- [docs/design-review-command.md](../../docs/design-review-command.md)
- [docs/plans/001-review-pack-process-contract.md](../../docs/plans/001-review-pack-process-contract.md)
- [docs/presentation-journal.md](../../docs/presentation-journal.md)
- [results/tooling-review-pack-contract-20260909T182644Z/MANIFEST.json](../../results/tooling-review-pack-contract-20260909T182644Z/MANIFEST.json)
- [results/tooling-review-pack-contract-20260909T182644Z/before-comparative-review.txt](../../results/tooling-review-pack-contract-20260909T182644Z/before-comparative-review.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/before-design-review.txt](../../results/tooling-review-pack-contract-20260909T182644Z/before-design-review.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/comparative-review-MANIFEST.json](../../results/tooling-review-pack-contract-20260909T182644Z/comparative-review-MANIFEST.json)
- [results/tooling-review-pack-contract-20260909T182644Z/comparative-review-checks.raw.txt.gz](../../results/tooling-review-pack-contract-20260909T182644Z/comparative-review-checks.raw.txt.gz)
- [results/tooling-review-pack-contract-20260909T182644Z/comparative-review-checks.txt](../../results/tooling-review-pack-contract-20260909T182644Z/comparative-review-checks.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/consistency.json](../../results/tooling-review-pack-contract-20260909T182644Z/consistency.json)
- [results/tooling-review-pack-contract-20260909T182644Z/design-review-MANIFEST.json](../../results/tooling-review-pack-contract-20260909T182644Z/design-review-MANIFEST.json)
- [results/tooling-review-pack-contract-20260909T182644Z/design-review-checks.raw.txt.gz](../../results/tooling-review-pack-contract-20260909T182644Z/design-review-checks.raw.txt.gz)
- [results/tooling-review-pack-contract-20260909T182644Z/design-review-checks.txt](../../results/tooling-review-pack-contract-20260909T182644Z/design-review-checks.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/integrity.json](../../results/tooling-review-pack-contract-20260909T182644Z/integrity.json)
- [results/tooling-review-pack-contract-20260909T182644Z/package-acceptance.txt](../../results/tooling-review-pack-contract-20260909T182644Z/package-acceptance.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/package-runs.json](../../results/tooling-review-pack-contract-20260909T182644Z/package-runs.json)
- [results/tooling-review-pack-contract-20260909T182644Z/report.md](../../results/tooling-review-pack-contract-20260909T182644Z/report.md)
- [results/tooling-review-pack-contract-20260909T182644Z/reproduction.json](../../results/tooling-review-pack-contract-20260909T182644Z/reproduction.json)
- [results/tooling-review-pack-contract-20260909T182644Z/test-output.txt](../../results/tooling-review-pack-contract-20260909T182644Z/test-output.txt)
- [results/tooling-review-pack-contract-20260909T182644Z/test-run.json](../../results/tooling-review-pack-contract-20260909T182644Z/test-run.json)
- [tests/test_process_contract.py](../../tests/test_process_contract.py)
- [tests/test_workflow_contract.py](../../tests/test_workflow_contract.py)
- [workflow/bundles.json](../../workflow/bundles.json)
