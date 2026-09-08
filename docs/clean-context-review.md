# Weryfikacja bez odziedziczonego kontekstu

## Co oznacza „czysty”

Nowa sesja bez historii autora plus kontrola wejść, narzędzi, pamięci i dostępu do plików. Sam komunikat „zapomnij wcześniejszą rozmowę” nie zapewnia izolacji. Sam worktree też nie wystarcza: ma historię Git i może współdzielić dostęp do pozostałych plików.

Praktyka: pakiet poza repo, nowa sesja, wejścia read-only, osobny output_root, wyłączony browsing i konektory do innych repo, brak projektu współdzielącego pamięć. Sprawdź globalne AGENTS/skills, mechanizm resume oraz dodatkowy kontekst wprowadzany przez klienta. Zachowaj wymagane logowanie, ale nie publikuj credentiali ani nie przekazuj ich w pakiecie.

Nie usuniemy wiedzy z treningu modelu. „Blind” oznacza brak udostępnienia określonych artefaktów w tej próbie, nie gwarancję, że model nigdy nie widział podobnego kodu.

## Trzy rundy oceny metody

| Pakiet | Co dostaje agent | Czego nie dostaje | Produkt |
|---|---|---|---|
| independent-design | brief, zadanie zaprojektowania procesu i format odpowiedzi | nasze role/prompty/workflow, źródła historyczne, journal | niezależny wariant i lista potrzebnych danych |
| design-review | brief, nasz plan, role, kontrakt, prompty, pipeline i szablony | historia rozmowy, journal, źródła historyczne | findingi z dowodami, kontrprzykłady, minimalny patch v0.2 |
| comparative-review | propozycja procesu oraz wybrany, jawnie opisany materiał upstream | nieograniczony dostęp do innych repo i sesji | tabela adopt/adapt/reject z uzasadnieniem i kosztami |

Najpierw zamroź i zapisz wynik independent-design. Drugą i trzecią rundę uruchom w nowych sesjach. Wcześniejsze raporty można dodać jako jawne dodatkowe wejścia z hashami; nie wklejaj historii konwersacji. Wynik porównania nie zastępuje wyniku niezależnego.

## Co jeszcze jest inputem

Nie tylko opisy agentów. Recenzent potrzebuje: celu i non-goals; budżetu i jego niewiadomych; dostępnych narzędzi/uprawnień; formatów przekazania pracy; warunków zakończenia i eskalacji; reguł własności plików; definicji parity; sposobu pomiaru; wersji wszystkich ocenianych artefaktów.

Do oceny wykonalności dla Buna potrzebny jest dodatkowo surowy snapshot oraz konfiguracja builda/testów. Bez nich recenzent może ocenić spójność procesu, ale nie może potwierdzić zależności, pokrycia testami czy kosztu konkretnej migracji.

## Rubryka review

Oceń 0–2 (0 brak, 1 częściowe, 2 wystarczające na pilotaż): granice ról; kompletność I/O; dowody i niewiadome; izolacja kontekstów; dependency/FFI strategy; testy i uczciwy comparator; kontrola kosztu; wznawianie; przydziały i konflikty; rozliczalność eksperymentu. Suma jest pomocnicza. Jeden blocker dyskwalifikuje GO niezależnie od sumy.

Dla każdego findingu: ID, severity, status potwierdzenia, ścieżka/sekcja, scenariusz błędu, konsekwencja, minimalna poprawka i sposób sprawdzenia poprawki. „Dodaj więcej agentów” bez korzyści i kosztu nie jest rozwiązaniem. Recenzent może pozostawić dobre elementy bez zmian; nie nagradzamy długości listy uwag.

## Osobny blind Architect

Pakiet architect zawiera brief, kontrakt zadania, prompt Architekta i szablon raportu oraz eksport surowego źródła. Nie zawiera PORTING.md, materiałów porównawczych, naszego journal ani historii Git. Nie dołączaj pełnego RustyBun jako drugiego mounta. Recenzent raportu otrzymuje ten sam source snapshot, raport, dowody i prompts/10-architecture-review.md, bez sesji roboczej Architekta.

Eksporter pomija znane pliki instrukcji i linki symboliczne; listę pominięć zachowuje w MANIFEST.json. Ta lista jest kontrolą wejścia, nie dowodem całkowitego braku uprzedzeń. Brakujące build inputs nie mogą zostać zignorowane przy późniejszej kompilacji.

## Kontrola operatora przed każdym wywołaniem

Sprawdź manifest i hashe, zaznacz izolację konwersacji/plików/narzędzi/pamięci osobno w run-record. Niesprawdzone pole = null, nie true. Zapisz wybrany i rzeczywisty model, klienta, ustawienia, uprawnienia, limit przed/po oraz dodatkowe wejścia. Raport bez wykonania otrzymuje status NOT_RUN.

## Uwaga o kliencie

Oficjalna dokumentacja opisuje automatyczne wczytywanie AGENTS.md oraz różne tryby uwierzytelniania. Weryfikacja dokumentacji: 2026-09-08. Dlatego audytujemy również instrukcje globalne i nie zakładamy, że nowy terminal oznacza nowy kontekst lub abonamentowy tryb rozliczania.

Źródła techniczne: https://developers.openai.com/codex/guides/agents-md ; https://developers.openai.com/codex/auth ; https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan . Konkretne komendy startu i dostępność modelu trzeba potwierdzić w używanym kliencie. Pakiet nie tworzy kluczy ani nie zmienia sposobu logowania.

## Poprawka preflight — 2026-09-08

Sam eksport i TASK.md nie wystarczają: operator dostarcza dodatkowo uzupełniony rekord i output_root. Dla istniejącego pakietu independent-design służy do tego `scripts/prepare-review-run.py`; [instrukcja i semantyka](preflight-start.md). Rekord oraz wygenerowany START-REVIEW.txt są jawnymi metadanymi administracyjnymi, nie dodatkową propozycją procesu. Wejścia i manifest pozostają niezmienione.

PREPARED oznacza przygotowane metadane, nie ukończony raport. Nieznane ustawienia runtime pozostają unknown, przyszłe pomiary/timestampy null. Nie zmienia to wymogu dowodów dla deklaracji COMPLETE.

Wyłącznie przy independent-design operator może jawnie dopuścić run rozpoznawczy flagą --allow-unverified-isolation. Isolation_verified pozostaje false, a raport musi ujawniać niezweryfikowaną niezależność. Bez tej zgody helper nie autoryzuje wykonania. Znany wyciek treści lub problem z wejściem/outputem nadal blokuje pracę. To nie jest zgoda na pomijanie bramek dla następnych etapów ani na nazywanie runu rozpoznawczego zweryfikowanym blind review.
