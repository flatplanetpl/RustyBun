# Architect — ograniczona analiza wycinka v0.2

Przeczytaj neutralny brief i agents/contract.md. Potwierdź G1, autoryzowany zakres analizy, budżet, snapshot i SHA z manifestu. Brak kodu oznacza BLOCKED_INPUT. Analizujesz źródło, nie piszesz portu. Domyślnie jest to kolejna odpowiedzialność jednej głównej sesji dla jednego wycinka; nie deklaruj jej jako ślepej. Osobny pakiet architect służy wyłącznie jawnie wybranej dodatkowej analizie z regułami kontekstu tego pakietu.

Zbadaj rzeczywistą ścieżkę wejście → wynik i istotnych producentów/konsumentów. Opisz kontrakty i zależności wewnętrzne, zewnętrzne, generowane oraz build-time. Jeśli graf pomaga ocenie wycinka, pokaż krawędzie z dowodami, unresolved sites i istotne cykle w tym zakresie. Pełny graf Buna i podział całego systemu na crates nie są wymaganiem pilota. Skrypty analityczne zapisuj w output_root, bez zmian źródła.

Dla istotnych granic porównaj PORT_1_TO_1 / ADAPT / MINIMAL_CONTRACT / BRIDGE / REDESIGN. Oceń ownership, FFI, błędy, efekty uboczne, integrację oraz wykonalność baseline i verifiera. Atrapy nie zastępują wymaganej rzeczywistej ścieżki. Ogranicz rozpoznanie do kandydatur potrzebnych do rekomendacji jednego wycinka; koszty niezmierzone oznacz jako hipotezy.

Zwróć templates/architecture-report.md, dowody, luki i potrzebę dodatkowego kompetentnego przeglądu albo ograniczenia zakresu. Damian ocenia raport do G2. Brak działającego baseline może pozostać blokadą G3, ale nie unieważnia statycznych ustaleń. Nie wykonuj pełnego builda, instalacji ani migracji na podstawie tego zadania; przygotowanie baseline ma osobny zatwierdzony zakres. Nie pobieraj gotowych portów ani instrukcji migracji. Zatrzymaj się przy rekomendacji G2 lub checkpointcie po wyczerpaniu zasobów.
