# 001 — Domknięcie procesu v0.2 po audycie

## Idea

Zapewnić uruchamialność kontroli procesu v0.2 wewnątrz ograniczonych pakietów
design-review i comparative-review. Baza to `874c55a`: pełna suite nie wykrywała,
że eksportowany `test_workflow_contract.py` wymaga wejść z całego repozytorium.
Polecenie użytkownika „Implement the plan” upoważnia do tej korekty i jednego
lokalnego commita, bez publikacji zdalnej ani uruchamiania rund review.

## Zadania

- [x] Zapisać uzgodniony plan w projekcie z sekcją Idea i checklistą.
- [x] Wydzielić do `tests/test_process_contract.py` samodzielne kontrole v0.2,
  używające wyłącznie dostarczonych konfiguracji, szablonów i promptów.
- [x] Zachować kontrole kompletności repo oraz integracji eksportera w
  dotychczasowym module, bez utraty pokrycia wymagań.
- [x] W obu pakietach zastąpić moduł wymagający całego repo nowym modułem;
  zachować pozostałe granice wejść.
- [x] Dodać regresję: rzeczywisty eksport obu pakietów i uruchomienie ich
  kontroli w osobnym procesie Pythona z katalogu `input`.
- [x] Uzupełnić instrukcje o komendę kontroli pakietu; zaktualizować README,
  START-HERE i journal o lukę oraz nowe dowody.
- [x] Zapisać nowe wyniki w `results/`, zweryfikować odbiór i przygotować jeden
  lokalny commit korekcyjny, zachowując oceniany commit i wcześniejsze raporty.

## Testy i warunki odbioru

- Pełna suite: `python3 -m unittest discover -s tests -v`.
- W obu eksportach, z katalogu `input`:
  `python3 -I -B -m unittest discover -s tests -p test_process_contract.py -v`.
- Kontrole negatywne na kopiach: brak wymaganej konfiguracji, wyłączenie
  obowiązkowego review, dwóch writerów oraz usunięcie wymagania baseline lub
  verifiera muszą powodować niepowodzenie z właściwego powodu.
- Ponownie sprawdzić hashe wcześniejszych wyników i archiwów, lokalne odnośniki,
  składnię JSON oraz `git diff --check`.
- Raport wskazuje commit, zmienione pliki, wykonane polecenia, wyniki i etapy
  niewykonane; samoprzegląd pozostaje SELF_REVIEW.

## Granice

G1–G5 pozostają PENDING. Wycinek, środowisko, model, wartości budżetu i plan
review pozostają do ustalenia. Comparative review nadal jest osobnym krokiem.
Zakres nie obejmuje migracji, baseline Buna, agentów, płatnego API, publikacji,
nowego runnera, fallbacków ani zmian schematów JSON. Archiwalne wyniki są read-only.
