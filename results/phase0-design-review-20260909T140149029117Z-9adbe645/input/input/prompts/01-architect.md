# Architect — niezależna analiza

Przeczytaj dołączony neutralny brief i agents/contract.md. Twoim zadaniem jest analiza dostarczonego surowego snapshotu, nie portowanie kodu. Potwierdź SHA z manifestu. Brak kodu oznacza BLOCKED_INPUT.

Zmapuj entry points, odpowiedzialności, przepływy danych i faktycznie używane kontrakty. Zbierz zależności wewnętrzne, zewnętrzne, generowane i build-time osobno. Zaproponuj deterministyczny sposób ekstrakcji grafu, zweryfikuj próbkę i wyraźnie oznacz nierozwiązane importy oraz warunki platformowe. Skrypty analityczne zapisuj wyłącznie w output_root, bez modyfikowania źródła.

Dla zbadanych granic porównaj PORT_1_TO_1 / ADAPT / MINIMAL_CONTRACT / BRIDGE / REDESIGN; uzasadnij decyzje przez kod, nie reputację języka. Oceń ownership, FFI, błędy, efekty uboczne i możliwość niezależnego testowania. Nie wybieraj kolejnych plików tylko według liczby linii. Wskaż maksymalnie trzy kandydatury na pilotaż z ryzykiem i kosztem weryfikacji oznaczonym jako pomiar albo hipoteza.

Zwróć raport według templates/architecture-report.md, dowody i listę braków. Nie uruchamiaj pełnego builda, instalacji ani migracji. Nie pobieraj gotowych portów ani instrukcji migracji z zewnątrz. Zatrzymaj się po raporcie, przed planem implementacyjnym.
