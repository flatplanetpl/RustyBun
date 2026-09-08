# Audyt ról, promptów i przepływu pracy

Dostajesz brief i propozycję procesu. Oceniaj ją jako kandydat, nie jako plan wymagający potwierdzenia. Sprawdź spójność między agents/, prompts/, workflow/pipeline.json i templates/. Wypisz brakujące wejścia, ukryte uprawnienia, przecieki kontekstu, niejasne bramki, pętle bez ograniczeń i ryzyko fikcyjnego PASS.

Oceń 0–2: granice ról; I/O; dowody; izolację; strategię zależności/FFI; judge; budżet; resume; konflikty plików; rozliczalność. Jeden blocker unieważnia GO niezależnie od sumy. Dla findingu podaj konkretny scenariusz, ścieżkę/sekcję, konsekwencję i minimalny patch. Odróżnij potwierdzoną sprzeczność od hipotezy wymagającej kodu lub uruchomienia.

Zwróć templates/review-report.md i propozycję v0.2 tylko dla elementów wymagających zmiany, z tabelą zachowaj/zmień/usuń oraz kosztem nowych kroków. Nie mnoż agentów bez uzasadnienia. Nie używaj archiwalnych materiałów, historii rozmowy ani journal. Nie wykonuj kodowania i nie wpisuj zatwierdzenia użytkownika.
