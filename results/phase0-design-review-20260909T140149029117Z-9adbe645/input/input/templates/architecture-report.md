# Raport Architekta — SZABLON, NIE WYNIK

Status / run_id / source SHA / process SHA / input manifest SHA-256 / model / zakres odczytu.

## 1. Zakres i ograniczenia
Co odczytano w całości, co próbkowano, czego nie zbadano; platformy i build configuration. Polecenia uruchomione, niewykonane i powód.

## 2. System i przepływy
Entry points, odpowiedzialności, przepływy danych, publiczne API. FACT/INFERENCE/UNKNOWN z path:line@SHA.

## 3. Zależności
Wewnętrzne / zewnętrzne / generowane / build-time; metoda ekstrakcji, krawędzie z dowodem, unresolved, SCC, ograniczenia statycznej analizy. Osobno skutki projektowanego podziału na crates.

## 4. Kontrakty
Wejścia, wyjścia, błędy, kodowanie, efekty uboczne, ordering, zasoby i cykl życia; producenci i konsumenci; sposób pomiaru parity.

## 5. Strategia granic
Boundary ID / warianty / rekomendacja / dowód / koszt i założenia / warunek obalenia / otwarte pytania.

## 6. Ryzyka
Ownership/areny, FFI/GC, comptime, bytes/string, error model, concurrency i platformy. Dla każdej luki dowód, impact i sposób zamknięcia.

## 7. Pilotaż
Do trzech kandydatów: kontrakt, zależności, testowalność, zakres integracji i powód wyboru. Nie nazywaj ich jednostkami zatwierdzonymi do wykonania.

## 8. Rekomendacja G2
GO / REVISE / BLOCKED; warunki, brakujące dowody i lista artefaktów. Akceptacja operatora: PENDING.
