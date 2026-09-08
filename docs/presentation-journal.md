# RustyBun — dziennik materiałów do prezentacji

Materiał źródłowy do przyszłego wystąpienia, nie gotowe slajdy. Powstał 2026-09-08. Wpisy z rozmowy są odtworzeniem ustaleń, nie logiem wykonanych eksperymentów. Zwięzłe hasła poniżej to propozycje redakcyjne, nie dosłowne cytaty użytkownika ani autorów upstream.

## Oznaczenia

DECISION — ustalenie rozmowy; PROPOSAL — nowa propozycja do review; OBSERVATION — odczytany artefakt lub pomiar; HYPOTHESIS — teza do zbadania; CORRECTION — korekta wcześniejszego uproszczenia. Wpis wyniku wymaga ścieżki do dowodu i SHA; brak danych pozostaje UNKNOWN.

## 2026-09-08 — od historii migracji do własnego eksperymentu

**DECISION J001 — próbujemy na abonamencie.** Pomysł: użyć własnej pracy i Codexa w Pro zamiast zakładać budżet płatnego API. Nie deklarujemy, że wykonamy całość ani że koszt będzie porównywalny z cudzym rachunkiem. Dokładny koszt historycznej migracji, dostępność modeli i oferta resetów wspomniana w rozmowie wymagają osobnego potwierdzenia przed wystąpieniem.

**DECISION J002 — harness to więcej niż tooling.** Roboczo: narzędzia plus reguły ich użycia, przekazania pracy, pętle kontroli i kryteria zakończenia. Smaczek narracyjny: przejście od pytania „co to za słowo?” do świadomego zaprojektowania procesu.

**DECISION J003 — plik nie jest jednostką zachowania.** Użytkownik zakwestionował skalowanie „3 → 10 → 50 plików”. Przechodzimy do funkcjonalnych jednostek z kontraktem, zależnościami i testami. Nie każdy slice musi przecinać wszystkie warstwy; spójny moduł również może być dobrą jednostką.

**DECISION J004 — najpierw zbadać zależności.** Rozważamy port 1:1, adapter, minimalny kontrakt, bridge lub redesign. Nie wybieramy automatycznie wariantu „wszystko przepisać w Rust”. HYPOTHESIS: mniejszy używany interfejs pozwoli ograniczyć zakres. Kontrprzykład do pokazania: mała sygnatura może skrywać trudne ownership, kolejność callbacków i semantykę błędów.

**DECISION J005 — analiza przed kodowaniem.** Ustalona kolejność: Architect → Planner → implementacja → niezależny review → poprawki → mechaniczna weryfikacja. Dwie sesje review nie są dowodem poprawności; ich uwagi muszą prowadzić do sprawdzalnych ustaleń.

**DECISION J006 — publiczne repo i jawne pochodzenie.** RustyBun na koncie flatplanetpl; materiały obce w sources/github.com/<owner>/<repo>/, nasze artefakty poza nimi. Archiwum ma zachować licencje i przypięte SHA, a nie udawać naszą implementację.

**DECISION J007 — zamrożenie źródła.** Surowy kod: 0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f. Referencja z instrukcją Phase A: 46d3bc29f270fa881dd5730ef1549e88407701a5. Odrzucono nowszy base PR-a jako dodatkową zmienną eksperymentu. Dowód i ograniczenia: [analiza baseline](upstream-baseline-analysis.md), wcześniejsza wersja repo a1527be0274985ba0e48144dbdd26b2340cd9440.

**DECISION J008 — niezależna ocena promptów i ról.** Recenzent musi dostać cel, ograniczenia i kontrakty I/O, nie tylko „popraw ten prompt”. Najpierw niezależny wariant; potem krytyka naszej propozycji; materiały porównawcze ujawniamy w osobnej rundzie.

**DECISION J009 — Architekt bez podglądania instrukcji migracji.** Pierwszą analizę chcemy wykonać na kodzie, nie na gotowych decyzjach wcześniejszego portu. Wynik zamrażamy przed ewentualnym porównaniem. To kontrola udostępnionych wejść, nie dowód braku znajomości Buna przez model z treningu.

**DECISION J010 — journal jest częścią procesu.** Zapisujemy decyzję, powód, odrzucony wariant, konsekwencję, dowód i materiał narracyjny. Aktualizacja w tym samym zestawie zmian, nie retrospektywne dopisywanie wyłącznie sukcesów.

## 2026-09-08 — korekty i przygotowanie v0.1

**CORRECTION J011 — nie twierdzimy, że Sumner nie analizował architektury.** Sam [PORTING.md](../sources/github.com/oven-sh/bun/commit-46d3bc29/docs/PORTING.md) zawiera mapę crates i reguły ownership/FFI oraz odwołanie do analizy lifetime. Nasza różnica to badana dekompozycja i jawne kontrakty, nie rzekomy brak planowania u autora. Przewaga pozostaje hipotezą.

**CORRECTION J012 — „dokładnie ich pierwszy stan” było zbyt mocne.** Historia potwierdza odtwarzalną granicę Phase A i relację commitów. Nie potwierdza całej zawartości dysku ani pierwszej prywatnej sesji autora.

**CORRECTION J013 — community harness nie jest oficjalnym, działającym runnerem.** W skopiowanym [multi-agent-orchestration.ts](../sources/github.com/Lumafy/sumner-method/workflows/multi-agent-orchestration.ts) wywołania agentów są szkicami, a validateFix zwraca true. To materiał koncepcyjny do oceny, nie dowód wykonanej migracji ani komponent gotowy do podłączenia.

**OBSERVATION J014 — wyciek kontekstu był już w naszym bootstrapie.** Odczytany skrypt domyślnie wybierał commit z PORTING.md. Przygotowanie v0.1 zmienia domyślny checkout na surowe źródło i dodaje eksport pakietów bez historii Git i znanych plików instrukcji. Rozdzielamy „źródło do analizy” od „materiału do porównania”.

**PROPOSAL J015 — bounded pilot.** Jeden writer, dwie niezależne sesje review, najwyżej dwie rundy poprawek, checkpoint po blokadzie. Najpierw jedna testowalna jednostka; dwa trudniejsze przypadki dopiero po wyniku. To proponowane parametry, nie zmierzone optimum ani automatyczna zgoda na run.

**OBSERVATION J016 — stan przygotowania.** Dodano opisy ról, prompty, szablony danych, bramki, pakiety review i instrukcję przekazania. To artefakty przygotowawcze. Nie wykonano niezależnej rundy LLM, pełnego audytu źródeł, builda Buna ani testów parity. Próba pobrania repo przez Git w środowisku wykonania nie powiodła się z powodu DNS; odczyt i zapis repo odbywa się przez konektor GitHub.

**OBSERVATION J017 — narzędzia poddane testom.** Eksporter przeszedł 8 testów offline na lokalnych fixture'ach Git, a bootstrap kontrolę składni Bash. [Dowód](../results/tooling-validation-20260908/report.md). To wynik narzędzi przygotowawczych, nie migracji ani review niezależnego modelu.

## Hasła i sceny do rozważenia

- „Nie migrujemy plików. Migrujemy kontrakty i zachowania.”
- „Don't migrate Bun. Design the factory.” — propozycja hasła z rozmowy, nie cytat upstream.
- „Nowy kontekst zaczyna się od kontroli wejścia, nie od polecenia: zapomnij.”
- „Zielony build to nie zielona migracja.”
- Scena demonstracyjna: reviewer znajduje brak w kontrakcie przed pierwszą linią portu. Na razie pomysł, nie zdarzenie.
- Scena demonstracyjna: mutacja łamie zachowanie, a judge rzeczywiście ją wykrywa. Na razie zaplanowany dowód.

## Dane do zebrania przed slajdami z wynikami

SHA/model/konfiguracja każdej próby; zakres kontraktu i fixture'y; verified units zamiast LOC; czas człowieka i limit; znalezione błędy i false positives; odrzucone sugestie recenzentów; regresje po fixerze; przykłady decyzji zmienionych przez dowody. Cudze liczby cytujemy tylko z potwierdzonego źródła i nie porównujemy rachunku API wprost z ceną abonamentu.

## Szablon następnego wpisu

ID / data / typ / status decyzji; problem; decyzja lub obserwacja; alternatywa odrzucona i powód; konsekwencja; dowód (run, commit, ścieżka); teza do prezentacji; co mogłoby ją obalić. Korekty dopisuj jawnie, nie wymazuj wcześniejszego nieudanego podejścia.

## 2026-09-08 — pierwszy start zatrzymany na preflight

**OBSERVATION J018 — poprawna odmowa ujawniła brak w przekazaniu pracy.** Operator wkleił komunikat agenta: dostępny był tylko szablon NOT_RUN, brakowało uzupełnionego rekordu i output_root; agent nie zmienił plików. Eksporter w commicie fbf1b25115cd2455664d78523f127101bed66516 rzeczywiście wymagał dostarczenia rekordu przez operatora. Skrócona instrukcja z rozmowy „wykonaj TASK.md” pominęła ten krok. To zdarzenie operacyjne zgłoszone przez użytkownika, nie wykonany przez nas audyt jego sesji ani ukończony niezależny projekt. Hasło: „Agent odmówił poprawnie. Błąd był w naszym handoffie.”

**CORRECTION J019 — szablon to nie rekord, a przygotowanie to nie wykonanie.** Dodano [prepare-review-run.py](../scripts/prepare-review-run.py): odczyt manifestu, kontrola hashy, właściwy run_id/role_id/stage, rzeczywiste ścieżki input_root/output_root i status PREPARED. Rekord oraz instrukcja startowa trafiają poza wejściowy pakiet. started_at/ended_at i metryki pozostają niewypełnione do rzeczywistego wykonania. Odrzucono ręczne wpisanie fikcyjnego modelu, ścieżki dysku operatora albo statusu COMPLETE. Poprawka może obsłużyć stary pakiet bez zmiany SHA ocenianych wejść.

**PROPOSAL J020 — jawny tryb rozpoznawczy zamiast udawanej izolacji.** Helper domyślnie nie autoryzuje pracy przy niezweryfikowanej izolacji. Operator może jawnie wybrać --allow-unverified-isolation wyłącznie dla pierwszego zadania projektowego. Wynik musi wtedy ujawnić EXPLORATORY; INDEPENDENCE UNVERIFIED; isolation_verified pozostaje false. Brak danych/niezgodne hashe/niedostępny output lub znany wyciek treści nadal blokują pracę. Nie zmieniono bramek dla Architekta i migracji. Ta opcja nie jest dowodem, że operator ją już uruchomił lub że sandbox działa. [Dokładna semantyka](preflight-start.md).

**OBSERVATION J021 — testujemy również odmowę i uczciwość metadanych.** 15 nowych testów offline/CLI przeszło na Linux/Python 3.13.5. Obejmują brak nadpisywania, zachowanie wejść, wykrywanie zmiany hashy, brakujące i nadmiarowe pliki, bezpieczne ścieżki oraz brak automatycznego potwierdzania izolacji. [Raport, ograniczenia i hashe](../results/tooling-preflight-20260908/report.md). Nie wykonano jeszcze review w środowisku operatora. To nie wynik migracji.

**DECISION J022 — główny README po angielsku.** Zgodnie z prośbą operatora przetłumaczono główny README i dopisano brakujący krok przygotowania rekordu. Pozostałych promptów i briefu nie przetłumaczono ani nie rozszerzono przed pierwszą rundą. Znane materiały historyczne i pierwotne wpisy tego dziennika zachowano.

## 2026-09-08 — przekazanie do reviewera jako wynik skryptu

**DECISION J023 — instrukcja obsługi nie może pozostawać wyłącznie w rozmowie.** Użytkownik wskazał, że „co przekazać reviewerowi” powinno być częścią skryptu. Poprzedni helper zapisywał START-REVIEW.txt, ale w terminalu podawał tylko ścieżkę. Teraz po przygotowaniu wypisuje katalog wejść i wyników z zamierzonymi uprawnieniami, kompletny tekst do wklejenia między wyraźnymi znacznikami i oczekiwane miejsce raportu. Zapisana kopia zostaje do audytu. Odrzucono wymaganie osobnego otwierania pliku i składania instrukcji z czatu. Hasło do prezentacji: „Handoff jest produktem narzędzia, nie pamięcią operatora.” Nie oznacza to automatycznego montowania katalogów ani uruchomienia modelu.

**OBSERVATION J024 — poprawka działa także dla już przygotowanej próby.** Dodano --show-handoff: ponowne wypisanie po kontroli wejść/rekordu/instrukcji, bez zapisów, nowych timestampów lub zmiany zgody. Rekord wskazujący rozpoczęte/zakończone zadanie nie służy do nowego startu. 22/22 testy preflight/handoff oraz osobna próba zgodności z rekordem utworzonym poprzednim helperem przeszły lokalnie; pliki w tej próbie pozostały identyczne bajtowo. [Raport i hashe](../results/tooling-handoff-20260908/report.md). Prompt TASK, brief i bramki pozostały bez zmian. Wynik dotyczy narzędzia, nie reviewera w środowisku użytkownika.

## 2026-09-08 — ponowne wyświetlenie przed przygotowaniem rekordu

**OBSERVATION / CORRECTION J025 — komunikat błędu też jest częścią przekazania pracy.** Operator pokazał błąd Missing or non-regular input: RUN-RECORD.json po użyciu --show-handoff. Sam komunikat nie rozstrzyga, czy próby nie przygotowano, czy wskazano złą lub niepełną lokalizację. Wersja 1c1dc06128bf3df2b290569fdfa9bc687e9ff20f tylko odczytywała istniejący rekord; poprzednia odpowiedź w rozmowie zbyt mocno eksponowała redisplay zamiast pierwszego przygotowania. Poprawka podaje pełną oczekiwaną ścieżkę, wyjaśnia tryb i wskazuje składnię przygotowania, które już automatycznie wypisuje prompt. Odrzucono automatyczne tworzenie rekordu, nadpisywanie niepełnych wyników i kopiowanie pustego szablonu dla ominięcia preflight. Osiem nowych testów regresji przeszło na Linux/Python 3.13.5; pełnej wcześniejszej suite nie uruchamiano w tej poprawce. [Dowód i ograniczenia](../results/tooling-missing-record-20260908/report.md). Nadal nie jest to wykonana runda modelu. Hasło: „Nie wystarczy wykryć brak. Narzędzie powinno wskazać następny poprawny krok.”
