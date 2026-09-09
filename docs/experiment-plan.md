# Plan wykonania RustyBun v0.2

Stan: proces przygotowany zgodnie z [D01–D08](decisions/2026-09-09-pilot-v0.2.md), oczekuje na przegląd zmian z Damianem i wymagane bramki. G1–G5 pozostają PENDING. Ten plan nie uruchamia analizy Buna ani migracji. Kierunek, przygotowanie procesu i zgoda na wykonanie to odrębne decyzje.

## Kolejność i bramki

Pierwszy pilot obejmuje **jeden ograniczony wycinek, jedną główną sesję roboczą i jednego aktywnego wykonawcę zmian**. Analiza, planowanie, implementacja, review i poprawki następują kolejno. Role oznaczają odpowiedzialności; zmiana odpowiedzialności nie wymaga nowego agenta. Wznowienia są dozwolone na podstawie checkpointu i skumulowanego budżetu.

| Etap | Konkretna praca | Produkty | Warunek przejścia |
|---|---|---|---|
| G0 — przygotowanie | spójne dokumenty, szablony, deklaratywny pipeline i testy narzędzi | diff procesu, dowody kontroli | przygotowanie nie jest zgodą na pilota |
| G1 — projekt procesu | independent design → design review → osobne comparative review | zamrożone raporty, konkretna wersja procesu i decyzje o zmianach | Damian zatwierdza wersję i budżet obejmujący przygotowanie oraz rezerwę |
| G2 — analiza wycinka | ograniczona analiza źródła, istotnych zależności i kontraktów; ocena dowodów przez operatora | architecture-report, rekomendacja jednego wycinka, ryzyka i luki | Damian ocenia zakres i dowody; wymagany przez ryzyko dodatkowy przegląd musi być zakończony |
| G3 — baseline, verifier i plan | operator z pomocą modelu przygotowuje oryginał i verifier; Planner zamyka manifest jednostki | środowisko, surowe wyniki kontroli dodatnich i ujemnych, zamrożony protokół, plan review i budżet wycinka | działający baseline i sprawdzony verifier; Damian zatwierdza manifest i kryteria przed implementacją |
| G4 — pilot | implementacja → review → rozstrzygnięcie uwag → ewentualne poprawki → ponowne review i testy → Referee | diffy, rozliczone interwencje, review i parity dla aktualnego hasha | brak potwierdzonych blokad; wykonane porównanie w zadanym zakresie; decyzja Damiana |
| G5 — decyzja o skali | analiza jakości, uwagi człowieka i całego kosztu dowodu | decyzja stop/zmień/rozszerz | rozszerzenie wymaga osobnej decyzji; wygenerowany kod nie dowodzi gotowości |

Stan bramek zapisuje [pipeline](../workflow/pipeline.json). Jest deklaracją zależności, **nie runnerem ani automatycznym egzekwowaniem bramek**. Operator sprawdza rekordy, polecenia, hashe i decyzje. Istnienie pliku, status COMPLETE i testy narzędzi nie są akceptacją etapu.

## G1: ocena metody pozostaje osobnym procesem

[Protokół kontekstów](clean-context-review.md) zachowuje trzy odrębne rundy. Independent-design dostaje neutralny brief, bez przyjętej metody. Design-review dostaje wersjonowany proces, zapis decyzji jako jawne ograniczenia i zamrożoną alternatywę. Comparative-review wymaga wybranych materiałów historycznych oraz wcześniejszych raportów i propozycji jako jawnych wejść z hashami.

Przygotowanie v0.2 nie jest kolejnym review i nie znosi comparative review przed G1. Nie uruchamiamy ponownie zamkniętych rund. Zmiana tej kolejności wymaga nowej decyzji Damiana. Wcześniejsze raporty i statusy zachowują swoje ograniczenia, w tym niezweryfikowaną niezależność.

## G2: ograniczona analiza, jeden wycinek

Po G1 badaj wyłącznie zakres potrzebny do wskazania testowalnego wycinka i jego rzeczywistej ścieżki wejście → wynik. Można porównać ograniczoną listę kandydatur; do pilota trafia jedna. Nie wybieramy jej w commicie przygotowawczym. Granicę określa zachowanie i wykonalność weryfikacji, nie liczba plików. Atrapy służą testom izolowanym; nie zastępują wymaganej rzeczywistej ścieżki.

Zapisuj entry points, producentów/konsumentów, ownership, błędy, efekty uboczne i platformy. Rozróżniaj zależności wewnętrzne, zewnętrzne, generowane i build-time. Graf, gdy jest potrzebny w tym zakresie, ma dowody krawędzi, unresolved sites i sprawdzone istotne cykle. Pełna mapa Buna, pełny graf SCC i podział całego systemu na crates są odłożone.

Dla istotnych granic porównaj PORT_1_TO_1 / ADAPT / MINIMAL_CONTRACT / BRIDGE / REDESIGN. Uzasadnij strategię rzeczywiście używanym interfejsem, cyklem życia i integracją. C/C++ i FFI wymagają świadomej decyzji; nie każdą zależność trzeba przepisać w Rust.

Główna sesja nie jest ślepym Architektem. Osobna analiza w pakiecie architect oraz dodatkowy przegląd raportu są opcjami wybieranymi jawnie z powodu ryzyka. Damian ocenia dowody do G2. Brak builda dopuszcza ograniczoną analizę statyczną, ale blokuje G3 i implementację.

## G3: działający oryginał i sprawdzony verifier

**Właścicielem gotowości baseline i verifiera jest Damian jako operator.** Model może projektować harness i wykonywać dozwolone polecenia. Przed startem trzeba wskazać wykonawcę, dozwolone operacje i środowisko; operator nie musi ręcznie wpisywać każdej komendy. Planner może przygotować draft podczas budowy harnessu, ale zamknięcie planu i G3 wymagają rzeczywistych wyników.

Odtwórz środowisko przypiętego źródła w wymaganym zakresie. Zapisz wersje narzędzi, konfigurację, system, CPU/RAM i pobrane zależności. Uruchom oryginalny punkt odniesienia i jego testy; oddziel existing failures, flaky i braki środowiska. Niemożliwy build to BLOCKED_ENVIRONMENT. Nie zmieniaj oczekiwanych wyników dla uzyskania zielonej suite.

Judge/verifier oznacza mechaniczny łańcuch uruchomienia i porównania. Old/new muszą używać identycznego publicznego interfejsu, danych, normalizacji i comparatora. Zapisz tożsamość faktycznie uruchomionego artefaktu. Znane luki/UB dokumentuj; nie wymagaj ich odtwarzania. Dopuszczone odstępstwo wymaga decyzji i jawnego testu.

Najpierw sprawdź poprawne wykonanie oryginału, następnie odrzucenie kontrolowanych mutacji z właściwego powodu. Wymagane przypadki: celowo błędny wynik (`wrong_result`), pusty zestaw testów (`empty_test_set`), brak wyniku (`missing_output`), timeout oraz błędna identyfikacja uruchamianego old/new (`wrong_implementation`). Każdy musi uniemożliwiać PASS. Kontrole wykonuj na kopiach testowych; kilka mutacji nie dowodzi pełnego pokrycia. Szablon wymagań nie jest dowodem ich wykonania.

Przed implementacją zamroź **kontrakt, dane, testy, normalizację, comparator i kryteria akceptacji**. Manifest protokołu identyfikuje wszystkie te artefakty, dozwolone komendy i wersję środowiska. Ich hashe oraz surowe dowody gotowości wpisz do manifestu jednostki. Zmiana protokołu wymaga nowej wersji, jawnej decyzji i ponownej walidacji baseline/verifiera oraz dowodów kandydata, których dotyczy. Implementer i Fixer nie mogą go osłabiać.

## G4: review, poprawki i mechaniczny odbiór

Przed G3 ustal rodzaj review, zakres, wykonawcę, deklarację niezależności oraz potrzebę dodatkowych kompetencji. Review jest obowiązkowe, bez domyślnego podwójnego A/B. Samoprzegląd modelu jest oznaczony jako SELF_REVIEW i obejmuje osobny etap pracy; model nie akceptuje własnego wyniku. Damian ocenia dowody i odbiera wynik.

Gdy ownership/FFI/unsafe lub inna istotna granica przekracza możliwości podstawowego przeglądu, przed implementacją zaplanuj kompetentny dodatkowy przegląd albo ogranicz/zmień wycinek. Zmiana nazwy roli lub nowy profil nie dowodzą niezależności. Każdy przegląd obejmuje zachowanie i istotne granice, niezależnie od specjalizacji recenzenta.

Przydziel dozwolone pliki i własność współdzielonych elementów. Jeden aktywny writer obejmuje również ręczne zmiany operatora. Findingi wymagają dowodów i rozstrzygnięcia confirmed/hypothesis. Potwierdzona blokada zatrzymuje odbiór. Gdy uwagi nie wymagają zmian kodu, po ich rozstrzygnięciu przejdź do Referee; Fixer nie jest obowiązkową pustą rundą.

Każda zmiana kandydata przez model lub człowieka wymaga nowego review i parity dla nowego hasha. Nie przenoś poprzedniego werdyktu na zmieniony artefakt i nie usuwaj starych logów. Referee wykonuje polecenia dla aktualnych old/new i protokołu, zapisuje exit codes, stdout/stderr, timeout i porównanie. Compile/test/parity i akceptacja Damiana pozostają odrębne. Niewykonane sprawdzenie to NOT_RUN.

## Budżet, interwencje i checkpoint

G1 zatwierdza budżet obejmujący przygotowanie, a G3 konkretny przydział wycinka. [Manifest jednostki](../templates/migration-unit.json) rozdziela limit i rezerwę czasu kalendarzowego, uwagi człowieka oraz zasobu modelu/planu. Jednostka i sposób pomiaru zasobu modelu wymagają jawnego ustalenia. Rezerwa obejmuje review, rozstrzygnięcie uwag, poprawki, retesty i zamknięcie. Jej wykorzystanie na te czynności jest planowym wydatkiem; nie wolno przeznaczyć jej na nową implementację bez zapewnienia obowiązkowej weryfikacji.

Nie rozpoczynaj nowej zmiany, jeśli pozostałe zasoby nie wystarczą na zmianę i jej wymagane sprawdzenia. Brak zatwierdzonych wartości blokuje wykonanie pilota, nie przygotowanie tego procesu. `max_fix_rounds=null` oznacza brak uzgodnionej wartości, nie nieskończone próby. Limit dwóch rund nie jest przyjętym domyślnym budżetem. Brak pomiaru zapisuj jako null/UNKNOWN, nie zero; nie dodawaj płatnego API ani nie obchodź limitów.

[Kontrakt wykonania](../agents/contract.md) definiuje pola ręcznych interwencji i checkpointu w istniejącym run-record. Interwencja zapisuje aktora, cel, powód, czas i hashe przed/po. Checkpoint wiąże wejścia, protokół, kandydata, dowody, ostatni potwierdzony stan, otwarte uwagi, zużyty/pozostały budżet i następne dozwolone działanie.

Przy braku zasobów zatrzymaj pracę i zamroź rekord. Brak limitu modelu oznacza BLOCKED_QUOTA; wyczerpanie innej części budżetu oznacza NEEDS_REVISION z przyczyną i checkpointem. Wznowienie tworzy nowy rekord kontynuacji wskazujący hash poprzedniego; nie zmienia zamkniętych wyników. Operator sprawdza hashe i przenosi skumulowane zużycie oraz liczbę poprawek. Zmianę sesji/modelu zapisuje się jawnie. Komendy review z fazy G1 nie służą do wznawiania pilota.

## Pomiary i zachowanie dowodów

Mierz osobno attempted/verified units, pokryte kontrakty, kompilację, parity, potwierdzone findingi, regresje, rundy poprawek, zmiany protokołu, czas człowieka, czas wykonania i zasób modelu. Stan jednostki PLANNED / IMPLEMENTED / REVIEWED / VERIFIED / ACCEPTED lub BLOCKED wymaga odpowiednich dowodów. COMPLETE dotyczy odpowiedzialności, a nie odbioru wycinka.

Ewentualne późniejsze porównanie metod wymaga tego samego SHA, zakresu, harnessu i budżetu oraz odnotowania modeli, kolejności i wiedzy operatora. Abonament i historyczny rachunek API nie są równoważnymi kosztami. Mniejszy narzut jednej sesji pozostaje hipotezą do pomiaru.

Archiwa sources/ i wcześniejsze results/ pozostają niezmienione. Nowe wyniki zapisuj w unikalnym results/<run-id>/ z manifestem, rekordem i surowymi dowodami; sprawdź dane prywatne przed publikacją. Journal aktualizuj razem z decyzją. Nadal do ustalenia: wycinek, środowisko, model/ustawienia, budżet/rezerwa, plan review i warunki osobnego comparative review. Nie zatwierdzaj żadnego z tych pól za Damiana.
