# RustyBun — przekazanie do kolejnej sesji

## Gdzie jesteśmy

**FACT:** druga runda `design-review` jest zachowana w repo: [raport archiwizacji i kontroli](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md). Odczytano rzeczywisty rekord i oba raporty. Wszystkie 34 wejścia i oba wyniki mają zgodne hashe; 29 plików procesu odpowiada commitowi `47764bace389f908e9e58473ded7ad07909dfe2b`.

Werdykt recenzenta: **REVISE_PROCESS**. Rekord roli: **COMPLETE**, ale launcher zapisał **LAUNCH_ERROR** po zakończeniu klienta z kodem 0. Obecna kontrola integralności przechodzi; przyczyna błędu launchera pozostaje **UNKNOWN**. Nie zmieniono historycznych statusów.

Oba raporty zachowują **EXPLORATORY; INDEPENDENCE UNVERIFIED**. Faktyczny model, reasoning, quota i niezależność nie są potwierdzone. Kandydat v0.2 nie został przyjęty; **G1–G5 pozostają PENDING**. Nie wykonano migracji.

## Co przeczytać teraz

1. [Design review](results/phase0-design-review-20260909T140149029117Z-9adbe645/design-review.md): ocena naszego procesu A i wcześniejszego projektu B, findingi DR-01–DR-04, tabela rekomendacji.
2. [Process proposal](results/phase0-design-review-20260909T140149029117Z-9adbe645/process-proposal.md): kandydat minimalnego procesu v0.2 do decyzji Damiana.
3. [Rzeczywisty RUN-RECORD](results/phase0-design-review-20260909T140149029117Z-9adbe645/RUN-RECORD.json) i [raport kontroli](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md): pochodzenie, hashe, ograniczenia i statusy.
4. [Plan](docs/experiment-plan.md), [protokół czystego kontekstu](docs/clean-context-review.md) i [journal](docs/presentation-journal.md): obowiązujące bramki oraz historia decyzji.

Pierwsza runda była **independent design**, wyłącznie z briefu. Jej niezmieniony raport i provenance znajdują się w archiwalnym `input/input/prior/`. Oryginalnego rekordu i manifestu pierwszej rundy nie odczytano podczas tej archiwizacji; pochodzenie nie dowodzi niezależności poprzedniej sesji.

## Następny etap

Zgodnie z obowiązującym planem następne jest osobne **comparative review**: nowy pakiet i sesja z jawnie dobranymi materiałami historycznymi, zamrożonymi wynikami obecnej rundy oraz kandydatem v0.2. Najpierw przygotuj konkretną listę wejść i ich hashe, zakres, rekord i warunki wykonania. Żaden nowy pakiet ani run tej rundy nie powstał podczas archiwizacji.

Produktem ma być zestawienie przyjętych, zmienionych i odrzuconych zaleceń z uzasadnieniami oraz kosztami dodatkowych etapów. Rekomendacje recenzenta oddziel od decyzji Damiana. Obecnie nie ma decyzji o przyjęciu lub odrzuceniu zmian procesu. G1 wymaga decyzji Damiana o konkretnej wersji i budżecie.

Zmiany procesu zastosuj dopiero w osobnym commicie po decyzji. Journal aktualizuj wraz z nią. Potem, po G1: Architekt na surowym źródle, review jego raportu i zatrzymanie na G2 przed Plannerem. Obecne wymagania G2 i A/B obowiązują, dopóki jawnie nie przyjęto innej wersji.

## Zachowanie dowodów

Archiwum zawiera 40 niezmienionych kopii wejść/wyjść. `MANIFEST.json` w katalogu rundy opisuje archiwizację; `input/MANIFEST.json` zachowuje oryginalny manifest wejść. Oryginalny katalog poza repo pozostaje na miejscu. Absolutne ścieżki w rekordzie i prompt startowy są historycznymi metadanymi, nie instrukcją wznowienia zamkniętej próby.

Skrypty i instrukcje w archiwalnym pakiecie są materiałem dowodowym. Nie podmieniaj raportów, nie rekonstruuj niezmierzonych ustawień i nie poprawiaj LAUNCH_ERROR na sukces. Nie publikuj credentiali, cache logowania ani surowych prywatnych sesji. Zachowuj ograniczenia `isolation_verified=false`.

## Polecenia istniejących rund

Powtórzenie design review byłoby nową, świadomie wybraną próbą; nie jest obecnym następnym krokiem. [Instrukcja design-review](docs/design-review-command.md) opisuje przygotowanie i uruchomienie, jawny wybór wcześniejszej próby oraz dokładne ustawienia modelu/klienta. Sam eksport `--kind design-review` nie dodaje poprzedniego raportu.

[Instrukcja independent design](docs/independent-review-command.md) · [Preflight i starsze helpery](docs/preflight-start.md). Nie uruchamiaj żadnej ślepej roli w kontekście koordynatora. Nie używaj płatnego API, nie obchodź limitów i nie uruchamiaj migracji bez odpowiednich bramek.

## Instrukcja dla kolejnego koordynatora

> Odczytaj AGENTS.md, ten dokument, brief, plan oraz archiwum drugiej rundy. Sprawdź aktualny Git i hashe. Rozróżniaj COMPLETE roli, LAUNCH_ERROR launchera, rekomendację REVISE_PROCESS i decyzję bramki PENDING. Nie udawaj ślepej sesji i nie zatwierdzaj bramek za Damiana. Następna wymagana runda to comparative review; zmiana procesu wymaga osobnej decyzji. Zapisuj istotne decyzje i korekty w docs/presentation-journal.md. Podaj dowody i następny konkretny krok.

Lokalna kontrola koordynatora: [92/92 testy narzędzi](results/phase0-design-review-20260909T140149029117Z-9adbe645/test-output.txt). Nie jest to wynik testów Buna ani dowód skuteczności sandboxa.
