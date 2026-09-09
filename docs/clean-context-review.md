# Konteksty pilota i niezależnych ocen v0.2

Pilot domyślnie prowadzi jedna główna sesja, kolejno dla jednego wycinka, z jednym aktywnym writerem. Zmiana odpowiedzialności nie wymaga osobnego agenta. Główna sesja zna wcześniejszy kontekst; samoprzegląd oznacza SELF_REVIEW i nie jest niezależny. Damian ocenia dowody i odbiera wynik. Rodzaj, zakres i wykonawca review są uzgodnione przed G3. Trudna granica wymaga kompetentnego dodatkowego przeglądu albo ograniczenia/zmiany wycinka.

Poniższe reguły czystego wejścia dotyczą odrębnych rund metody i jawnie wybranych niezależnych zadań, nie każdej odpowiedzialności pilota. Wznowienie głównej pracy zachowuje checkpoint, hashe i budżet zgodnie z [kontraktem](../agents/contract.md). Przygotowanie v0.2 nie uruchamia żadnej rundy.

## Co oznacza „czysty”

Nowa sesja bez historii autora plus kontrola wejść, narzędzi, pamięci i dostępu do plików. Sam komunikat „zapomnij wcześniejszą rozmowę” nie zapewnia izolacji. Sam worktree też nie wystarcza: ma historię Git i może współdzielić dostęp do pozostałych plików.

Praktyka: pakiet poza repo, nowa sesja, wejścia read-only, osobny output_root, wyłączony browsing i konektory do innych repo, brak projektu współdzielącego pamięć. Sprawdź globalne AGENTS/skills, mechanizm resume oraz dodatkowy kontekst wprowadzany przez klienta. Zachowaj wymagane logowanie, ale nie publikuj credentiali ani nie przekazuj ich w pakiecie.

Nie usuniemy wiedzy z treningu modelu. „Blind” oznacza brak udostępnienia określonych artefaktów w tej próbie, nie gwarancję, że model nigdy nie widział podobnego kodu.

## Trzy rundy oceny metody

| Pakiet | Co dostaje agent | Czego nie dostaje | Produkt |
|---|---|---|---|
| independent-design | brief, zadanie zaprojektowania procesu i format odpowiedzi | nasze role/prompty/workflow, źródła historyczne, journal | niezależny wariant i lista potrzebnych danych |
| design-review | brief, aktualny proces, D01–D08 jako jawne ograniczenia oraz zamrożony independent design z provenance | historia rozmowy, journal, źródła historyczne | findingi z dowodami, kontrprzykłady, minimalny patch v0.2 |
| comparative-review | aktualny proces, D01–D08, zamrożone wcześniejsze raporty/propozycja oraz wybrany materiał upstream | nieograniczony dostęp do innych repo i sesji | tabela adopt/adapt/reject z uzasadnieniem i kosztami |

Wynik independent-design zamraża się przed drugą rundą. Drugą i trzecią rundę wykonuje się w nowych sesjach po odpowiedniej autoryzacji; nie wkleja się historii konwersacji. Zamkniętych wyników nie uruchamiamy ponownie. Comparative review nadal jest wymagane przed G1; rewizja dokumentów go nie zastępuje.

Bieżące pakiety design-review i comparative-review zawierają zapis decyzji jako jawne ograniczenia operatora, nie ocenę niezależnego recenzenta. Jego historyczne odnośniki nie uprawniają do czytania plików spoza manifestu. Independent-design pozostaje neutralny: bez D01–D08, ról i pipeline; administracyjny run-record nie narzuca liczby sesji ani metody.

Wrapper design-review dołącza zamrożony independent design i provenance. Sam eksport comparative-review zawiera skonfigurowane dokumenty i materiały, ale nie dodaje automatycznie wcześniejszych raportów ani propozycji. Operator ma je jawnie wskazać, sprawdzić hashe i ująć w finalnym manifeście nowego pakietu przed osobną rundą. Ich brak oznacza BLOCKED_INPUT. Nie zmieniaj zamrożonych pakietów; nie budujemy nowego launchera porównawczego.

## Kontrole procesu wewnątrz pakietu

W nowych eksportach design-review i comparative-review przejdź do katalogu
`input` wewnątrz pakietu, gdzie znajdują się `tests/`, `workflow/` i `templates/`:

```bash
python3 -I -B -m unittest discover -s tests -p test_process_contract.py -v
```

Moduł sprawdza dostarczony kontrakt v0.2 i referencje do promptów. Korzysta tylko
z biblioteki standardowej Pythona i jawnych wejść pakietu; nie wymaga całego repo,
narzędzi innych rund ani materiałów historycznych spoza allowlisty. Brak wymaganego
pliku lub osłabienie kontrolowanej reguły daje niepowodzenie. `-I` pomija ustawienia
importu z otoczenia Pythona, a `-B` wyłącza zapis bytecode; nie zapewniają sandboxa.

Kontrole kompletności repo i integracji eksportera pozostają w
`tests/test_workflow_contract.py` i działają w pełnej suite koordynatora.
Starszy eksport tego modułu wymagał całego repo i nie był uruchamialny w obu
ograniczonych pakietach. Zamrożonych pakietów nie poprawiamy; nowe zawierają
`test_process_contract.py`. Wynik tych testów to kontrola konfiguracji, bez
zatwierdzenia bramek, dowodu izolacji czy zastąpienia właściwego review.

## Co jeszcze jest inputem

Nie tylko opisy agentów. Recenzent potrzebuje: celu i non-goals; budżetu i jego niewiadomych; dostępnych narzędzi/uprawnień; formatów przekazania pracy; warunków zakończenia i eskalacji; reguł własności plików; definicji parity; sposobu pomiaru; wersji wszystkich ocenianych artefaktów.

Do oceny wykonalności dla Buna potrzebny jest dodatkowo surowy snapshot oraz konfiguracja builda/testów. Bez nich recenzent może ocenić spójność procesu, ale nie może potwierdzić zależności, pokrycia testami czy kosztu konkretnej migracji.

## Rubryka review

Oceń 0–2 (0 brak, 1 częściowe, 2 wystarczające na pilotaż): granice ról; kompletność I/O; dowody i niewiadome; izolacja kontekstów; dependency/FFI strategy; testy i uczciwy comparator; kontrola kosztu; wznawianie; przydziały i konflikty; rozliczalność eksperymentu. Suma jest pomocnicza. Jeden blocker dyskwalifikuje GO niezależnie od sumy.

Dla każdego findingu: ID, severity, status potwierdzenia, ścieżka/sekcja, scenariusz błędu, konsekwencja, minimalna poprawka i sposób sprawdzenia poprawki. „Dodaj więcej agentów” bez korzyści i kosztu nie jest rozwiązaniem. Recenzent może pozostawić dobre elementy bez zmian; nie nagradzamy długości listy uwag.

## Opcjonalny blind Architect i dodatkowy przegląd

Pakiet architect służy dodatkowej, jawnie wybranej analizie po G1. Nie jest domyślną sesją pilota ani wymogiem pełnego grafu Buna. Zawiera brief, kontrakt zadania, prompt Architekta i szablon ograniczonego raportu oraz eksport surowego źródła. Nie zawiera PORTING.md, materiałów porównawczych, naszego journal ani historii Git. Nie dołączaj pełnego RustyBun jako drugiego mounta. Jeśli wybrano niezależny przegląd raportu, jego pakiet musi zawierać ten sam source snapshot, raport, dowody, zakres i prompts/10-architecture-review.md, bez sesji roboczej autora. Operator przygotowuje ten zakres jawnie; eksporter nie dostarcza osobnego rodzaju pakietu architecture-review. Analiza i próbkowanie obejmują istotne granice wycinka.

Eksporter pomija znane pliki instrukcji i linki symboliczne; listę pominięć zachowuje w MANIFEST.json. Ta lista jest kontrolą wejścia, nie dowodem całkowitego braku uprzedzeń. Brakujące build inputs nie mogą zostać zignorowane przy późniejszej kompilacji.

## Kontrola operatora przed każdym wywołaniem

Sprawdź manifest i hashe, zaznacz izolację konwersacji/plików/narzędzi/pamięci osobno w run-record. Niesprawdzone pole = null, nie true. Zapisz wybrany i rzeczywisty model, klienta, ustawienia, uprawnienia, limit przed/po oraz dodatkowe wejścia. Raport bez wykonania otrzymuje status NOT_RUN.

## Uwaga o kliencie

Oficjalna dokumentacja opisuje automatyczne wczytywanie AGENTS.md oraz różne tryby uwierzytelniania. Weryfikacja dokumentacji: 2026-09-08. Dlatego audytujemy również instrukcje globalne i nie zakładamy, że nowy terminal oznacza nowy kontekst lub abonamentowy tryb rozliczania.

Źródła techniczne: https://developers.openai.com/codex/guides/agents-md ; https://developers.openai.com/codex/auth ; https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan . Konkretne komendy startu i dostępność modelu trzeba potwierdzić w używanym kliencie. Pakiet nie tworzy kluczy ani nie zmienia sposobu logowania.

## Poprawka preflight — 2026-09-08

Sam eksport i TASK.md nie wystarczają: operator dostarcza dodatkowo uzupełniony rekord i output_root. Dla istniejącego pakietu independent-design służy do tego `scripts/prepare-review-run.py`; [instrukcja i semantyka](preflight-start.md). Rekord oraz wygenerowany START-REVIEW.txt są jawnymi metadanymi administracyjnymi, nie dodatkową propozycją procesu. Wejścia i manifest pozostają niezmienione.

PREPARED oznacza przygotowane metadane, nie ukończony raport. Nieznane ustawienia runtime pozostają unknown, przyszłe pomiary/timestampy null. Nie zmienia to wymogu dowodów dla deklaracji COMPLETE.

Helper prepare-review-run obsługuje flagę --allow-unverified-isolation wyłącznie dla independent-design. Osobny launcher design-review ma własną zgodę o zakresie design-review-only; nie dziedziczy zgody pierwszej rundy. Isolation_verified pozostaje false, a raport musi ujawniać niezweryfikowaną niezależność. Bez tej zgody helper nie autoryzuje wykonania. Znany wyciek treści lub problem z wejściem/outputem nadal blokuje pracę. To nie jest zgoda na pomijanie bramek dla następnych etapów ani na nazywanie runu rozpoznawczego zweryfikowanym blind review.
