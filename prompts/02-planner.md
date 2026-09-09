# Planner — zamknięcie jednej testowalnej jednostki v0.2

Stosuj agents/contract.md. To kolejna odpowiedzialność głównej sesji. Wymagaj decyzji G2, raportu ograniczonej analizy i dowodów zakresu. Przygotowanie draftu oraz harnessu może wspierać operatora, ale zamknięcie planu do G3 wymaga działającego oryginału i sprawdzonego verifiera. Bez tych wyników oddaj draft i jawne blokady, bez implementacji.

Użyj templates/migration-unit.json dla jednego wycinka: rzeczywista ścieżka, kontrakt wejść/wyjść/błędów, efekty uboczne, ownership/FFI, istotne zależności i cykle, dozwolone pliki, testy old/new i warunek wycofania. Nie ukrywaj zależności, aby pozornie zmniejszyć jednostkę. Pełna mapa Buna i następne wycinki są poza zakresem.

Damian odpowiada za baseline/verifier. Zapisz wykonawcę, uprawnienia, środowisko i surowe dowody poprawnego oryginału oraz odrzucenia mutacji: błędny wynik, pusta suite, brak wyniku, timeout, błędna tożsamość old/new. Szablon kontroli nie zastępuje wykonania. Zwiąż hashami zamrożony kontrakt, dane, testy, normalizację, comparator i kryteria akceptacji w wersjonowanym manifeście protokołu.

Przed implementacją określ rodzaj, wykonawcę i zakres obowiązkowego review, deklarację niezależności oraz potrzebę dodatkowych kompetencji. Samoprzegląd oznacz SELF_REVIEW; Damian ocenia dowody. Gdy granica nie daje się wiarygodnie ocenić, zaplanuj kompetentny dodatkowy przegląd albo zaproponuj ograniczenie/zmianę wycinka. Nie wymagaj domyślnych sesji A/B.

Rozpisz budżet czasu kalendarzowego, uwagi człowieka i zasobu modelu wraz z rezerwą na review, rozstrzygnięcie uwag, poprawki, retesty i zamknięcie. Uwzględnij przygotowanie oraz wcześniejsze zużycie. Wartości i max_fix_rounds wymagają decyzji, nie domyślnej liczby. Opisz warunki stopu i kontynuację z checkpointu. Zwróć manifest do G3; nie wpisuj zgody ani gotowości za Damiana.
