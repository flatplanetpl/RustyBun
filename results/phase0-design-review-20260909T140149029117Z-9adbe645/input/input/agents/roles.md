# Role i odpowiedzialności v0.1

Projekt do niezależnego przeglądu. Role nie wymagają osobnych modeli ani jednoczesnego uruchomienia. Dwie instancje review muszą mieć rozdzielone konteksty.

| Rola | Dostaje | Odpowiada za | Nie może |
|---|---|---|---|
| Architect | neutralny brief, surowy snapshot, kontrakt i szablon raportu | mapa systemu, kontrakty, ryzyka, warianty zależności, kandydaci do pilotażu | pisać portu; przyjmować cudzych instrukcji migracji jako prawdy |
| Planner | zatwierdzony raport Architekta, dowody, decyzja o baseline i testach | ograniczone migration units, kolejność, zależności, przydział plików, kryteria odbioru | wybierać architektury sprzecznej z zatwierdzonym kontraktem; sam zatwierdzać planu |
| Implementer | jedna zatwierdzona jednostka, source, zależności, testy i rulebook | implementacja w wyznaczonym zakresie; jawne blokady | samoreview; zmiana kontraktu/testów; nieuzgodnione zależności |
| Reviewer A | zamrożony diff, oryginał, kontrakt i testy | przede wszystkim semantyka, błędy, przypadki graniczne | edycja kodu; czytanie opinii B lub sesji autora |
| Reviewer B | ten sam zamrożony artefakt w nowym kontekście | przede wszystkim ownership, FFI, współbieżność, integracja | edycja kodu; czytanie opinii A lub sesji autora |
| Fixer | potwierdzone ustalenia, aktualny hash kandydata, źródło i kontrakt | minimalne poprawki, mapowanie finding → zmiana | maskowanie błędu stubem; osłabianie asercji; uznanie hipotezy za potwierdzony błąd |
| Referee operator | zatwierdzone polecenia, dwie implementacje, fixture'y i comparator | uruchomienie kompilacji/testów, exit codes, surowe wyniki i parity | zastępowanie wyniku testów opinią LLM; zmiana comparatora w rundzie |

A i B nie mają wyłączności na kategorię błędów; każdy zgłasza dowolny znaleziony problem. Ich zgodność nie jest głosowaniem rozstrzygającym. Jedno potwierdzone naruszenie kontraktu blokuje odbiór.

## Role kontrolne przed kodowaniem

**Method reviewer:** projektuje wariant niezależny, potem w oddzielnej rundzie audytuje nasze role/prompty; później porównuje materiały referencyjne. Produkt: konkretne kontrprzykłady, ocena kosztu z założeniami i minimalny patch v0.2. Bez kodu nie stwierdza wykonalności migracji Buna.

**Architecture reviewer:** sprawdza raport Architekta na tym samym snapshotcie, bez jego sesji roboczej. Próbuje obalić wskazane granice, mapę zależności i kontrakty. Nie widzi rezultatów poprzedniej migracji w rundzie ślepej.

**Koordynator/operator:** przygotowuje izolację, manifesty i przydziały; scala wyniki, sprawdza dowody spornych findingów, chroni budżet, prowadzi journal. Nie jest niezależnym recenzentem. Damian zatwierdza bramki; proponowana zmiana architektury wraca do tej decyzji.

## Sposób współpracy

Początkowo jeden aktywny writer. Review może być sekwencyjne w oddzielnych sesjach. Każda poprawka Fixera unieważnia poprzedni werdykt dla zmienionego artefaktu: nowe review i Referee odnoszą się do nowego hasha.
