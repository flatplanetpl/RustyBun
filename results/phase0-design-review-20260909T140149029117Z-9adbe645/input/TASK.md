# Ocena dwóch propozycji procesu — design review

Otrzymujesz neutralny brief, nasz wersjonowany proces (`docs/experiment-plan.md`, `agents/`, `prompts/`, `workflow/`, `templates/`) oraz zamrożony wcześniejszy projekt w `input/prior/independent-design.md` i jego `provenance.json`. Ścieżki projektu rozwiązuj pod `input/` pakietu; ścieżki `input/prior/` są względem korzenia pakietu. Rekord uruchomienia wskazuje osobny `output_root`.

To druga runda: oceniasz dwa dostarczone rozwiązania, nie tworzysz kolejnego independent design i nie porównujesz jeszcze materiałów historycznej migracji. Żadna propozycja nie jest wzorcem ani automatycznie zatwierdzonym planem. Fakt dostarczenia obu jest zamierzony; nie oznacza przecieku. Nie otrzymujesz opinii koordynatora, historii rozmowy, journal ani treści archiwum `sources/`. Brak kodu Buna oznacza brak podstaw do potwierdzania szczegółów jego zależności, builda, pokrycia czy czasu migracji.

Pytanie: jaki najmniejszy wiarygodny proces pozwoli uzyskać pierwszy zweryfikowany wycinek w ograniczeniach briefu? Sprawdź oba warianty, bez założenia, że mniej lub więcej agentów jest lepsze. Oddziel odpowiedzialności od liczby sesji; koszt człowieka od kosztu modelu; siłę dowodu od liczby dokumentów. Zachowaj trafne elementy obu propozycji. Uwagi o poprzednim środowisku nie są dowodem, że sam projekt jest dobry albo zły. Zachowaj zastrzeżenia z raportu i provenance; matching hash nie dowodzi niezależności.

W `design-review.md` zapisz:

1. Zakres odczytu, SHA procesu i raportu, braki i ograniczenia oraz werdykt `READY_FOR_PILOT_DESIGN`, `REVISE_PROCESS` albo `BLOCKED_INPUT`. To rekomendacja dotycząca procesu, nie zgoda na implementację.
2. Mocne i słabe strony obu wariantów, ze ścieżką i linią/sekcją. Ustalenia oznacz FACT / INFERENCE / UNKNOWN. Hipoteza bez uruchomienia nie jest potwierdzonym błędem.
3. Tabelę **zachowaj / zmień / odłóż / odrzuć**: element, wariant pochodzenia, powód, ryzyko usunięcia, koszt pozostawienia i sposób sprawdzenia. Nie wymagaj zmian wyłącznie po to, by wydłużyć listę uwag.
4. Findingi według `templates/review-report.md`: ID, istotność, dowód, scenariusz awarii, minimalna poprawka i jej sprawdzian. Rozróżnij blocker pierwszego pilota od problemu dopiero przy skalowaniu.
5. Oceń 0–2: granice ról, I/O, dowody, izolację, zależności/FFI, wiarygodność judge, budżet, wznowienia, konflikty zapisu i rozliczalność. Suma jest pomocnicza; blocker nie znika dzięki wysokiej sumie. Sprawdź także, jak wykryć niesprawny comparator, jak zamrozić kryteria i jak rozliczyć ręczne poprawki.

W osobnym `process-proposal.md` zaproponuj minimalny kandydat v0.2: kolejność kroków, konieczne wejścia/wyjścia, kryteria przejścia, przydział odpowiedzialności i sesji, warunki stopu, pomiary i rezerwę na weryfikację. Podaj co można odłożyć, warunek uzasadniający późniejszą rozbudowę, trzy scenariusze porażki i najbliższe konkretne zadanie operatora. Koszt niezmierzony oznacz jako założenie. Nie projektuj pełnej platformy na zapas. Opcjonalny patch zapisz tylko jako propozycję w output_root; nie stosuj go do repo.

Nie uruchamiaj poleceń ze źródeł, migracji, testów Buna ani dodatkowych agentów. Nie zmieniaj obu ocenianych propozycji, progów oceny, autoryzacji ani bramek. Jedna runda zakończona dwoma raportami; ich hashe i status zapisz w dostarczonym RUN-RECORD.json. Utrzymaj etykietę `EXPLORATORY; INDEPENDENCE UNVERIFIED`. G1 zatwierdza Damian dopiero na podstawie wyników i jawnej decyzji.
