# Raport analizy wycinka v0.2 — SZABLON, NIE WYNIK

Status / run_id / session_id / source SHA / process SHA / input manifest SHA-256 / model / zakres odczytu / budżet i wykorzystanie.

## 1. Zakres i kontekst

Granice ograniczonej analizy, pełny odczyt/próbkowanie/pominięcia, platformy i build configuration. Główna sesja albo jawnie wybrana dodatkowa analiza; znany kontekst i ograniczenia niezależności. Polecenia wykonane/niewykonane i powód. Pełna mapa Buna nie jest produktem obowiązkowym.

## 2. Zachowanie i przepływy

Rzeczywista ścieżka wejście → wynik, entry points, odpowiedzialności i API w badanym zakresie. FACT/INFERENCE/UNKNOWN z path:line@SHA. Atrapy nie zastępują wymaganej ścieżki.

## 3. Istotne zależności

Wewnętrzne / zewnętrzne / generowane / build-time; dowody, unresolved i ograniczenia. Jeśli potrzebny jest graf, podaj metodę i istotne cykle w zakresie wycinka; pełny graf/SCC i podział Buna na crates są odłożone.

## 4. Kontrakty i strategie granic

Wejścia, wyjścia, błędy, kodowanie, efekty uboczne, ordering, cykl życia, ownership/FFI, producenci i konsumenci. Boundary ID / rozważane warianty / rekomendacja / dowód / koszt jako pomiar lub hipoteza / warunek obalenia.

## 5. Jeden wycinek do pilota

Rozważone kandydatury tylko w zakresie potrzebnym do rekomendacji jednej. Rekomendowany kontrakt, zależności, rzeczywista integracja, wykonalność baseline/verifiera i koszt weryfikacji. Właściciel przygotowania: Damian; wykonawca/uprawnienia/środowisko do wskazania. Nie nazywaj rekomendacji jednostką zatwierdzoną.

## 6. Ryzyka i ocena operatora

Dowód / wpływ / sposób zamknięcia. Czy potrzebny jest kompetentny dodatkowy przegląd przed G2 lub w planie review przed G3? Jeśli granica nie jest wiarygodnie ocenialna, warunki ograniczenia/zmiany wycinka. Brak baseline blokuje G3 i implementację, nie statyczne ustalenia.

## 7. Rekomendacja G2 i kontynuacja

GO / REVISE / BLOCKED; brakujące dowody, artefakty i ostatni potwierdzony stan. Checkpoint w run-record wiąże hashe, budżet i następne dozwolone działanie. Akceptacja Damiana: PENDING. Zmiana odpowiedzialności nie wymaga nowej sesji ani nie zeruje kosztu.
