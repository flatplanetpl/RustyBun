# RustyBun — przekazanie do kolejnej sesji

## Gdzie jesteśmy

**Proces v0.2 został przygotowany zgodnie z D01–D08.** Zmiany dokumentów, ról, promptów, szablonów i konfiguracji oczekują na przegląd z Damianem oraz właściwe autoryzacje. **G1–G5 pozostają PENDING.** Nie wybrano wycinka, nie zatwierdzono budżetu i nie rozpoczęto analizy Buna ani migracji.

Pilot ma jeden ograniczony wycinek, jedną główną sesję i jednego aktywnego writera. Kolejne role oznaczają odpowiedzialności. Operator odpowiada za działający oryginał i sprawdzony verifier przed G3. Review jest obowiązkowe, z rodzajem i zakresem uzgodnionym przed implementacją; nie ma domyślnego podwójnego A/B. Samoprzegląd jest ujawniony, a dowody i odbiór ocenia Damian.

Budżet obejmuje przygotowanie i rezerwę na review, rozstrzygnięcie uwag, poprawki, retesty i zamknięcie. Ręczne zmiany i wznowienia są rozliczalne. Nieznane wartości są null; żadna liczba rund nie została domyślnie zatwierdzona. Pipeline pozostaje deklaratywny, bez runnera.

## Co przeczytać teraz

1. [Plan v0.2](docs/experiment-plan.md), [role](agents/roles.md) i [kontrakt z definicjami pól](agents/contract.md): aktywne reguły, szablony, checkpoint i warunki stopu.
2. [D01–D08](docs/decisions/2026-09-09-pilot-v0.2.md): zachowany zapis decyzji; [journal](docs/presentation-journal.md) odróżnia przyjęty kierunek od przygotowania procesu i pomiarów.
3. [Raport przygotowania](results/tooling-process-v02-20260909T174417Z/report.md): mapowanie decyzji na zmiany i kontrole, lista plików i ograniczenia dowodów.
4. [Protokół kontekstów](docs/clean-context-review.md): odrębne rundy metody oraz opcjonalne niezależne zadania kontrolne.

## Następny krok i kwestie otwarte

Przejrzeć przygotowane zmiany z Damianem. Następnie jako osobne zadanie przygotować wymagane **comparative review**: jawna lista wejść z hashami, zamrożone raporty i propozycja, zakres, rekord i warunki wykonania. Konfiguracja pakietu jest zaktualizowana, ale kompletnej operacyjnej rundy porównawczej nie przygotowano ani nie uruchomiono. Eksport testowy na lokalnej fixture nie jest taką rundą.

Comparative review nie zostało zniesione. G1 wymaga konkretnej wersji procesu i budżetu zatwierdzonych przez Damiana. Zmiana lub pominięcie tej rundy wymaga nowej decyzji. Potem, w granicach odpowiednich bramek, można analizować źródło, rekomendować jeden wycinek, przygotować baseline/verifier i zamknąć plan G3.

Nadal do ustalenia: wycinek i środowisko; model i ustawienia; jednostka pomiaru zasobu modelu, limity, rezerwa i liczba poprawek; rodzaj/wykonawca/zakres review zależny od ryzyka wycinka. Null w szablonie nie jest zgodą na nieograniczoną pracę ani potwierdzeniem gotowości.

## Wznowienie pilota po przyszłym przerwaniu

Wznowienie opiera się na zamrożonym run-record i checkpointcie, nie pamięci sesji. Sprawdź hashe wejść, protokołu, kandydata i dowodów, ostatni potwierdzony stan, otwarte findingi, budżet oraz następne dozwolone działanie. Nowy rekord kontynuacji wskazuje hash poprzedniego, przenosi zużycie i liczbę poprawek oraz zapisuje zmianę sesji/modelu.

Zmiana kandydata przez człowieka lub model wymaga nowych review/parity; starych dowodów nie kasujemy. Zmiana protokołu wymaga nowej wersji, decyzji i rewalidacji. Brak zasobów na obowiązkową weryfikację blokuje kolejną zmianę; brak limitu modelu oznacza BLOCKED_QUOTA. Istniejące komendy metodologicznego review i `--show-handoff` nie wznawiają pilota.

## Zamrożone wyniki drugiej rundy

**FACT:** [archiwum](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md) zachowuje 40 kopii wejść/wyjść. Historyczny manifest opisuje 34 wejścia; 29 plików procesu odpowiada commitowi `47764bace389f908e9e58473ded7ad07909dfe2b`. [Design review](results/phase0-design-review-20260909T140149029117Z-9adbe645/design-review.md), [propozycja recenzenta](results/phase0-design-review-20260909T140149029117Z-9adbe645/process-proposal.md) i [RUN-RECORD](results/phase0-design-review-20260909T140149029117Z-9adbe645/RUN-RECORD.json) pozostają niezmienione.

Werdykt to REVISE_PROCESS, rola COMPLETE, launcher LAUNCH_ERROR przy zapisanym kodzie klienta 0. Przyczyna błędu launchera pozostaje UNKNOWN. Oba raporty zachowują EXPLORATORY; INDEPENDENCE UNVERIFIED. Model, reasoning, quota i niezależność nie są potwierdzone. Pierwszy wynik był independent design z briefu; oryginalnego rekordu i manifestu tej pierwszej rundy nie odczytano przy archiwizacji drugiej. Nie uzupełniaj tych braków domysłami.

`MANIFEST.json` katalogu rundy opisuje archiwizację, a `input/MANIFEST.json` zachowuje manifest pierwotnych wejść. Oryginalny katalog poza repo pozostaje na miejscu. Absolutne ścieżki, prompt i statusy są historycznymi metadanymi, nie instrukcją restartu. Nie publikuj credentiali, cache logowania ani surowych prywatnych sesji.

## Istniejące narzędzia

[Design-review](docs/design-review-command.md) · [Independent design](docs/independent-review-command.md) · [Preflight](docs/preflight-start.md). Powtórzenie zamkniętej rundy jest nowym, świadomie wybranym zadaniem, nie domyślnym następnym krokiem. Ślepe role wykonuje się wyłącznie w przygotowanym pakiecie. Koordynator znający repo nie jest ślepym recenzentem ani Architektem.

Testy przygotowania obejmują narzędzia i kontrakty konfiguracji, nie skuteczność sandboxa, Bun ani gotowość G3. [Nowe wyniki](results/tooling-process-v02-20260909T174417Z/test-output.txt) są odrębne od [historycznych 92 testów przy archiwizacji](results/phase0-design-review-20260909T140149029117Z-9adbe645/test-output.txt).

## Instrukcja dla kolejnego koordynatora

> Odczytaj AGENTS.md, ten dokument, aktywny plan v0.2, kontrakt i raport przygotowania. Sprawdź Git i zachowaj cudze zmiany. D01–D08 są zastosowane do procesu; nie przygotowuj ich ponownie jako nowego projektu. Przed dalszą pracą uwzględnij przegląd zmian z Damianem, osobne comparative review i bramki. Nie wybieraj ani nie portuj wycinka bez odpowiedniej zgody. Nie traktuj testów narzędzi jako akceptacji procesu. Zachowaj archiwa, nieznane pomiary i status LAUNCH_ERROR. Journal aktualizuj razem z decyzją; każdą przyszłą kontynuację oprzyj na hashach i skumulowanym budżecie.
