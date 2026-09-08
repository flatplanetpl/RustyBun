# Wyniki

Obecnie brak ukończonych rund agentowych i wyników migracji. Szablony nie są wynikami.

Dla każdej rzeczywistej próby utwórz nowy results/<run-id>/ z MANIFEST.json, run-record.json, report.md oraz dowodami poleceń. Nie nadpisuj wcześniejszych prób. Run record zapisuje pełny SHA źródła i procesu, faktyczny model, zakres, uprawnienia, pomiary oraz decyzję bramki.

Dodatkowe wejścia (np. raport poprzedniego recenzenta) wymagają osobnego wpisu z SHA-256. Akceptacja odnosi się do konkretnych hashy; zmiana kandydata unieważnia wcześniejszy werdykt dla tej wersji.

Przed publicznym commitem sprawdź logi pod kątem sekretów, danych konta i prywatnych ścieżek. Nie publikuj tokenów, credentiali ani ukrytego toku rozumowania. Do prezentacji zapisuj zwięzły, sprawdzalny ślad decyzji i wyników.
