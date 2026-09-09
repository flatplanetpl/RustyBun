# RustyBun — przekazanie do kolejnej sesji

## Gdzie jesteśmy

**Decyzja z 2026-09-09:** Damian przyjął kierunek uproszczenia pilota opisany w [decyzjach v0.2](docs/decisions/2026-09-09-pilot-v0.2.md). Ten commit zapisuje ustalenia; wdrożenie ich do procesu pozostaje osobnym następnym zadaniem. Nie jest to przyjęcie wszystkich szczegółów propozycji recenzenta ani zgoda na migrację. **G1–G5 pozostają PENDING**.

**FACT:** druga runda `design-review` jest zachowana w repo: [raport archiwizacji i kontroli](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md). Odczytano rzeczywisty rekord i oba raporty. Wszystkie 34 wejścia i oba wyniki mają zgodne hashe; 29 plików procesu odpowiada commitowi `47764bace389f908e9e58473ded7ad07909dfe2b`.

Werdykt recenzenta: **REVISE_PROCESS**. Rekord roli: **COMPLETE**, ale launcher zapisał **LAUNCH_ERROR** po zakończeniu klienta z kodem 0. Obecna kontrola integralności przechodzi; przyczyna błędu launchera pozostaje **UNKNOWN**. Nie zmieniono historycznych statusów.

Oba raporty zachowują **EXPLORATORY; INDEPENDENCE UNVERIFIED**. Faktyczny model, reasoning, quota i niezależność nie są potwierdzone. Nie wykonano migracji. Nowa decyzja nie uzupełnia brakujących pomiarów ani nie zmienia tych ograniczeń.

## Co przeczytać teraz

1. [Decyzje po review](docs/decisions/2026-09-09-pilot-v0.2.md): przyjęty kierunek D01–D08, granice zgody i zakres osobnego commita przygotowawczego.
2. [Design review](results/phase0-design-review-20260909T140149029117Z-9adbe645/design-review.md) i [process proposal](results/phase0-design-review-20260909T140149029117Z-9adbe645/process-proposal.md): zamrożone rekomendacje, nie instrukcje do automatycznego wykonania.
3. [Rzeczywisty RUN-RECORD](results/phase0-design-review-20260909T140149029117Z-9adbe645/RUN-RECORD.json) i [raport kontroli](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md): pochodzenie, hashe, ograniczenia i statusy.
4. [Plan](docs/experiment-plan.md), [protokół czystego kontekstu](docs/clean-context-review.md) i [journal](docs/presentation-journal.md): dotychczasowe reguły i historia, których ten zapis decyzji jeszcze nie przebudowuje.

Pierwsza runda była **independent design**, wyłącznie z briefu. Jej niezmieniony raport i provenance znajdują się w archiwalnym `input/input/prior/`. Oryginalnego rekordu i manifestu pierwszej rundy nie odczytano podczas tej archiwizacji; pochodzenie nie dowodzi niezależności poprzedniej sesji.

## Następne zadanie przygotowawcze — osobny commit v0.2

Dostosować istniejące dokumenty procesu, role, prompty i szablony do D01–D08; zmieniać skrypty tylko w zakresie koniecznej spójności. Nie budować pełnego runnera. Nie wykonywać teraz analizy kodu Buna, wyboru konkretnego slice'a ani migracji.

Docelowy pilot: jeden ograniczony wycinek, jedna główna sesja robocza i jeden writer; baseline i sprawdzony verifier przed portem; zamrożone kryteria; jawny review, poprawki i retesty; budżet z rezerwą oraz rejestrowane interwencje i checkpoint. Właścicielem przygotowania baseline/judge i odbioru dowodów jest operator, wspomagany modelem i narzędziami. Dodatkowy kompetentny przegląd pozostaje opcją wynikającą z ryzyka, nie domyślnym podwójnym A/B ani automatycznym dowodem poprawności.

Po przygotowaniu zmian przejrzeć je z Damianem. Konkretne wartości budżetu, model/ustawienia, środowisko i wycinek pozostają do ustalenia. Ten dokument nie jest poleceniem uruchomienia istniejących skryptów ani akceptacją ich następnej wersji.

## Co nadal musi poprzedzić G1

Wymagane osobne **comparative review** z materiałami historycznymi nie zostało zniesione. Przygotowanie dokumentacji v0.2 nie zastępuje tej rundy. Do jej wykonania potrzebne są jawna lista wejść i hashe, zamrożone raporty/propozycja, zakres, rekord i warunki wykonania. Nie przygotowano ani nie uruchomiono jej w commicie decyzji.

G1 nadal wymaga decyzji Damiana o konkretnej wersji i budżecie. Zmiana lub pominięcie comparative review wymagałaby nowej jawnej decyzji. Dotychczasowe pliki procesu i pipeline pozostają niezmienione do osobnego wdrożenia v0.2; nie należy uruchamiać nieuzgodnionej mieszanki reguł obu wersji.

## Zachowanie dowodów

Archiwum zawiera 40 niezmienionych kopii wejść/wyjść. `MANIFEST.json` w katalogu rundy opisuje archiwizację; `input/MANIFEST.json` zachowuje oryginalny manifest wejść. Oryginalny katalog poza repo pozostaje na miejscu. Absolutne ścieżki w rekordzie i prompt startowy są historycznymi metadanymi, nie instrukcją wznowienia zamkniętej próby.

Skrypty i instrukcje w archiwalnym pakiecie są materiałem dowodowym. Nie podmieniaj raportów, nie rekonstruuj niezmierzonych ustawień i nie poprawiaj LAUNCH_ERROR na sukces. Nie publikuj credentiali, cache logowania ani surowych prywatnych sesji. Zachowuj ograniczenia `isolation_verified=false`.

## Polecenia istniejących rund

Powtórzenie design review byłoby nową, świadomie wybraną próbą; nie jest obecnym następnym krokiem. [Instrukcja design-review](docs/design-review-command.md) opisuje przygotowanie i uruchomienie, jawny wybór wcześniejszej próby oraz dokładne ustawienia modelu/klienta. Sam eksport `--kind design-review` nie dodaje poprzedniego raportu.

[Instrukcja independent design](docs/independent-review-command.md) · [Preflight i starsze helpery](docs/preflight-start.md). Nie uruchamiaj żadnej ślepej roli w kontekście koordynatora. Nie używaj płatnego API, nie obchodź limitów i nie uruchamiaj migracji bez odpowiednich bramek.

## Instrukcja dla kolejnego koordynatora

> Odczytaj AGENTS.md, ten dokument, docs/decisions/2026-09-09-pilot-v0.2.md, brief, plan oraz archiwum drugiej rundy. Sprawdź aktualny Git i nie nadpisuj cudzych zmian. Kierunek D01–D08 jest przyjęty; wdrożenie procesu jest osobnym zadaniem. Przygotuj spójną aktualizację istniejących dokumentów, ról, promptów i szablonów, a narzędzi tylko tam, gdzie to konieczne. Nie wybieraj jeszcze wycinka Buna, nie uruchamiaj pilota i nie zatwierdzaj bramek za Damiana. Wymagane comparative review nie zostało pominięte ani wykonane. Zachowaj zamrożone raporty, statusy i hashe; rozróżniaj decyzję o kierunku, implementację procesu i autoryzację wykonania. Aktualizuj journal, sprawdź zmieniane narzędzia i przedstaw diff oraz otwarte decyzje do przeglądu.

Historyczna kontrola koordynatora przy archiwizacji: [92/92 testy narzędzi](results/phase0-design-review-20260909T140149029117Z-9adbe645/test-output.txt). Nie jest to wynik nowego uruchomienia testów w commicie decyzji, testów Buna ani dowód skuteczności sandboxa.
