# Neutralny brief eksperymentu

## Cel

Sprawdzić, jaki mierzalny, poprawny fragment migracji Bun z Zig do Rust może wykonać jeden programista z pomocą Codexa w ramach posiadanego planu Pro. Nie zakładamy ukończenia całej migracji ani przewagi konkretnego modelu czy metody.

## Ograniczenia

- Bez płatnego API i bez automatycznych zakupów kredytów. Dostępne modele, limit i ewentualne promocje trzeba odczytać z faktycznego konta w dniu uruchomienia; obecnie nie są zmierzone.
- Przed implementacją potrzebna jest analiza granic funkcjonalnych, zależności oraz sposobu weryfikacji. Granica pliku nie musi być granicą zadania.
- Zachowanie obserwowalne ma być zgodne w jawnie zdefiniowanym zakresie. Uproszczenie zależności musi zachować wymagany kontrakt, nie tylko pasującą sygnaturę.
- Bez zmian produkcyjnych, publikowania pakietów i wdrożeń. To eksperyment na odizolowanym snapshotcie.
- Ludzkie decyzje, odstępstwa i ręczne poprawki muszą być rozliczalne. Żadnych wymyślonych metryk ani ukrytego luzowania testów.
- Kolejne podejścia porównujemy na tym samym kodzie, zakresie i zestawie testów. Czas analizy, przygotowania i ludzkiej uwagi też jest kosztem.

## Dane wejściowe do analizy kodu

Repo źródłowe: `oven-sh/bun`.
SHA kodu: `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.
Sam identyfikator nie oznacza, że kod jest dostępny. Bez dostarczonego snapshotu wszystkie oceny konkretnej implementacji pozostają UNKNOWN.

## Pytania badawcze

Czy wcześniejsze zdefiniowanie kontraktów i strategii zależności zmniejsza liczbę poprawek? Kiedy zachować strukturę, kiedy zastosować adapter, a kiedy wybrać inną implementację? Czy niezależny przegląd poprawia wykrywanie błędów w stopniu uzasadniającym koszt? Jaka jest najmniejsza jednostka, która daje wiarygodny dowód end-to-end?

## Sukces pierwszego pilotażu

Jeden jawnie ograniczony fragment: zweryfikowane wejście, opis kontraktu, działający baseline, równoważny interfejs testowy, wykonana implementacja, przegląd, surowe wyniki testów i pomiary zasobów. Sama liczba wygenerowanych plików lub zielony status od modelu nie wystarcza.

## Niewiadome

Sprzęt docelowy, dostępność historycznego toolchainu/dependencji, czas builda, stan suite'u, identyfikatory modeli i rzeczywisty budżet limitu nie są jeszcze ustalone. Recenzent ma wskazać, jakie minimum danych pozwoli przejść od projektu procesu do wykonania.
