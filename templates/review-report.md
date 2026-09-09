# Raport review v0.2 — SZABLON, NIE WYNIK

run_id / session_id / rodzaj zadania / review kind / aktor i kompetencje / candidate SHA-256 / protocol SHA-256 / process SHA / source SHA / model (jeśli użyty) / input manifest SHA-256.

## Zakres i rodzaj przeglądu

Uzgodniony zakres oraz wykonawcy; faktycznie odczytane materiały, wykonane sprawdzenia, pominięcia i narzędzia. Kind: self-review / human-review / independent-review. Dla review kandydata podaj odnośnik do zatwierdzonego planu. Dla oceny metody oznacz jej osobne zadanie i zakres.

Deklaracja kontekstu: SELF_REVIEW / UNVERIFIED / VERIFIED z dowodami. Samoprzegląd modelu i zmiana nazwy roli nie są niezależnym review. Czy istotne granice wymagają dodatkowych kompetencji albo ograniczenia/zmiany wycinka? Bez wyników poleceń nie potwierdzaj testów. Nie ma domyślnego wymogu dwóch osobnych recenzentów.

## Ustalenia i rozstrzygnięcie

ID / severity (blocker, high, medium, low) / confirmed lub hypothesis / path:line@SHA albo sekcja / kontrprzykład / skutek / minimalna poprawka / test poprawki / rozstrzygnięcie operatora i dowód.

## Elementy poprawne i odrzucone podejrzenia

Co zachować i dlaczego odrzucono podejrzenia. Brak findingów nie dowodzi pełnej poprawności. Potwierdzona blokada wymaga zamknięcia przed odbiorem; zgodność opinii nie zastępuje dowodu.

## Propozycja zmian i ważność dowodów

Minimalna propozycja, bez edycji kandydata. Wskaż potrzebne poprawki, ich weryfikację i zasoby. Każda zmiana przez model lub człowieka wymaga nowego review/parity dla nowego hasha; zachowaj poprzednie raporty. Proponowana zmiana protokołu wymaga wersji, decyzji i rewalidacji.

## Werdykt i kontynuacja

Rekomendacja GO / REVISE / BLOCKED; nierozwiązane blokady, dokładny hash i zakres ważności. Bez zmian wymagających kodu można przejść do Referee po rozstrzygnięciu uwag. Zużycie i checkpoint zapisane w run-record; koszt nie zeruje się przy wznowieniu. Akceptacja Damiana: PENDING. Review nie jest mechanicznym werdyktem testów.
