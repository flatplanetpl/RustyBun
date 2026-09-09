# Niezależny przegląd raportu Architekta

Stosuj agents/contract.md. Wymagaj tego samego snapshotu, manifestu wejść, raportu i dowodów. Nie dostajesz sesji autora ani gotowych materiałów poprzedniej migracji. Brak kodu oznacza ocenę dokumentu, nie weryfikację faktów o repo.

Spróbuj obalić granice funkcjonalne, graf i strategie zależności. Sprawdź niezależną próbkę krawędzi w obie strony (misses i invented edges), cykle oraz wpływ ponownego podziału na crates. Zbadaj przynajmniej jeden kontrakt u producenta i konsumenta, również ownership, błędy, efekty uboczne i warunki platformowe. Gdy proponowany MINIMAL_CONTRACT pomija zachowanie, pokaż konkretny scenariusz.

Zwróć templates/review-report.md z dowodami, zakresem próbkowania i rekomendacją do G2. Nie poprawiaj raportu autora w miejscu, nie uruchamiaj portowania i nie zatwierdzaj bramki za użytkownika.
