# Plan wykonania RustyBun v0.1

Stan: kandydat procesu, bez uruchomionej migracji. Ten dokument zastępuje wcześniejszą kolejność, która kierowała do materiałów referencyjnych przed analizą niezależną. Nie zmienia przypiętego kodu.

## Kolejność i bramki

| Etap | Konkretna praca | Produkty | Warunek przejścia |
|---|---|---|---|
| G0 — przygotowanie | audyt repo, przypięcie wejść, role/prompty, eksport pakietów i testy narzędzi | obecny zestaw plików; manifest pakietu | narzędzia sprawdzone; brak deklarowania gotowej migracji |
| G1 — projekt procesu | niezależny wariant → review naszej propozycji → osobne comparative review | raporty trzech rund, patch procesu, wykaz zaakceptowanych/odrzuconych zmian | Damian zatwierdza konkretną wersję procesu i budżet |
| G2 — Architect | statyczna analiza surowego źródła, mapa i kontrakty; niezależny przegląd raportu | architecture-report, deterministyczna mapa w zakresie, rejestr luk i ryzyk | raport ma dowody; krytyczne niejasności wyjaśnione lub ograniczają zakres; decyzja Damiana przed Plannerem |
| G3 — baseline i plan | kontrolowany build oryginału; inwentaryzacja testów; Planner wydziela jednostkę i projektuje judge | environment/run-record, baseline outputs, unit manifest, test plan | wykonalny kontrakt, realny baseline i zweryfikowany judge; akceptacja planu |
| G4 — pilot | Implementer → A i B → potwierdzenie findingów → Fixer → ponowne review → Referee | diffy, findings, kompilacja, testy, wyniki old/new | brak potwierdzonych blokad; parity w zadeklarowanym zakresie; podpisana decyzja |
| G5 — decyzja o skali | analiza jakości, uwagi człowieka, limitu i kosztu weryfikacji | porównanie wariantów i decyzja stop/zmień/rozszerz | nie skalujemy tylko dlatego, że istnieją pliki .rs |

G0 jest realizacją przygotowania, nie zgodą na G1–G5. Aktualny stan bramek zapisuje workflow/pipeline.json; rekord wykonania i decyzja z hashem są dowodem, nie samo pole statusu.

## G1: czego oczekujemy od niezależnej oceny

Pełny protokół: docs/clean-context-review.md. Minimalny input to brief, kryteria review, kontrakty I/O, propozycja procesu (dopiero w drugiej rundzie), ograniczenia narzędzi i budżetu. Historia naszej rozmowy, entuzjazm autora, journal i cudze wyniki nie należą do wejścia ślepego.

Runda porównawcza może ulepszyć proces, ale nie kasuje oryginalnej wersji ani ślepego wyniku. Operator może znać oba warianty; Architekt dostaje tylko zatwierdzony minimalny kontrakt zadania, bez gotowych decyzji dotyczących Buna.

## G2: zakres analizy Architekta

Przejdź od entry points do odpowiedzialności, danych, zależności i obserwowalnych efektów. Rejestruj zależności wewnętrzne, biblioteki zewnętrzne, komponenty C/C++, generowany kod i zależności builda osobno. Sam graf @import nie jest kompletną mapą semantyczną.

Skrypt analityczny ma deterministycznie emitować krawędzie z pochodzeniem i unresolved sites. Uwzględnij warunki platformowe i build configuration; oblicz silnie spójne składowe, a następnie ponownie sprawdź cykle po proponowanym podziale na crates. Nie wyprowadzaj kolejności builda z niezweryfikowanego grafu.

Dla każdej badanej granicy porównaj PORT_1_TO_1 / ADAPT / MINIMAL_CONTRACT / BRIDGE / REDESIGN. Uzasadnij wybór przez rzeczywiście używany interfejs, ownership, błędy, efekty uboczne i koszty integracji. Mały interfejs może kryć duży kontrakt: np. callback lifetime, kodowanie, ordering czy backpressure.

Nie zakładaj, że każda zależność musi być przepisana w Rust. Przypadki C/C++ i FFI wymagają osobnej decyzji, nie automatycznego zastępstwa crate'em. Nie wprowadzaj zmian implementacji na tym etapie.

## G3: baseline i niezależny judge

Najpierw odtwórz środowisko dla przypiętego źródła. Zapisz wersje narzędzi, system, CPU/RAM, konfigurację i pobrane zależności. Niemożność pobrania toolchainu to BLOCKED_ENVIRONMENT, nie błąd portu. Brak builda nie blokuje statycznego G2, ale blokuje dowód gotowości G4.

Uruchom testy oryginału i sklasyfikuj existing failures, flaky i braki środowiska. Nie zmieniaj oczekiwanych wyników tylko po to, by suite był zielony. Judge używa identycznego publicznego interfejsu, wejść i comparatora dla old/new. Znane błędy bezpieczeństwa/UB dokumentuj; nie wymagaj odtwarzania UB ani luk w nowej implementacji. Każde dopuszczone odstępstwo od zachowania musi mieć jawny test i decyzję.

Sprawdź judge na oryginale i na kilku kontrolowanych mutacjach w kopii testowej. Musi wykryć każdą wybraną mutację; nie przedstawiaj tego jako dowodu pełnego pokrycia. Baseline fixture'y i comparator zamroź przed implementacją.

Planner wybiera najpierw jedną funkcjonalną jednostkę o zamkniętym, testowalnym kontrakcie. Kolejne dwa trudniejsze przypadki są propozycją rozszerzenia po pierwszym wyniku — nie obowiązkiem migracji trzech arbitralnych plików.

## G4: bounded execution

Przydział plików i shared ownership przed pracą. Domyślnie jeden writer, dwie niezależne sesje review. Wspólna zmiana wraca do koordynatora. Żadnych jednoczesnych edycji tych samych plików.

Budżet roboczy do zatwierdzenia: najwyżej dwie rundy poprawek jednostki, bez automatycznego fan-outu. Po wyczerpaniu budżetu/limitu zapisz dowody i checkpoint. Samo istnienie pliku nie oznacza ukończenia: stan obejmuje PLANNED, IMPLEMENTED, REVIEWED, VERIFIED, ACCEPTED lub BLOCKED.

Używaj tanich sprawdzeń wcześnie, gdy są dostępne. Centralizuj kosztowny pełny build, gdy pomiar uzasadnia to rozwiązanie. Zakaz kompilacji z cudzej instrukcji nie jest domyślną regułą RustyBun.

## Pomiary i porównanie

Mierz osobno: kontrakty pokryte testami, attempted/verified units, wyniki kompilacji i parity, potwierdzone findingi, regresje, liczbę rund, zmiany rulebooka, czas człowieka, czas wykonania i wykorzystanie limitu. Unknown zapisuj jako null/UNKNOWN, nie zero.

Porównanie strukturalnego portu z podejściem kontraktowym: ten sam SHA, zakres, harness testowy, budżet i możliwie ten sam model/ustawienia; oddzielne sesje i workspace'y. Zapisuj kolejność prób i wpływ wiedzy operatora. Zmiana modelu i metody jednocześnie jest confounderem. Abonament i historyczny rachunek API nie są równoważnymi miarami kosztu.

## Git i materiały do prezentacji

Wejścia archiwalne pozostają w sources/. Nasze decyzje i prompty są wersjonowane poza nimi. Każda runda ma unikalne results/<run-id>/, manifest wejść, run-record, raport i dowody. Nie nadpisuj wyników wcześniejszej rundy. Zmiany procesu po zatwierdzeniu wprowadzaj jako osobny reviewowany commit/PR; journal aktualizuj razem z decyzją.

Przed pierwszym realnym runem wymagane są: G1, faktyczny model i tryb logowania, limit, uprawnienia narzędzi i izolacja. Żadne z tych pól nie zostało automatycznie zatwierdzone przez przygotowanie plików.
