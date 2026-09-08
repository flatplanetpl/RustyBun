# RustyBun — przekazanie do kolejnej sesji

## Gdzie jesteśmy

Pierwsza runda **independent design** stworzyła alternatywny proces wyłącznie z briefu, bez naszej propozycji. Operator przekazał treść raportu z próby `phase0-independent-20260908T154456Z`. To ukończone zadanie projektowe według dostarczonego materiału, nie migracja ani dowód niezależności. Raport zachowuje `EXPLORATORY; INDEPENDENCE UNVERIFIED`, opisuje awarię sandboxa i wewnętrznego subagenta. Oryginalnego RUN-RECORD.json z serwera nie odczytano podczas przygotowania tej zmiany.

Następna runda to **design review**: nowy recenzent otrzymuje nasz aktualny proces oraz zamrożony alternatywny projekt. Ma ocenić oba, bez naszych komentarzy i bez z góry założonego werdyktu. Dopiero osobne **comparative review** ujawnia materiały historycznej migracji. Nie myl tych trzech nazw. G1 i dalsze bramki pozostają niezatwierdzone.

## Teraz uruchom drugą rundę

W zwykłym terminalu operatora w `~/RustyBun` pobierz nowe pliki:

```bash
git pull --ff-only
```

Następnie:

```bash
python3 scripts/design-review.py --update --launch --allow-unverified-isolation
```

Domyślna wcześniejsza próba to `../phase0-independent-20260908T154456Z-output`, wskazana przez operatora. Nie wybieramy automatycznie najnowszego folderu. Skrypt odczytuje jej raport i rekord, wymaga zakończenia i zgodności zapisanego SHA-256. Brak rekordu albo niezgodny hash to blokada, nie powód do wymyślania metadanych. Inny ukończony przebieg wskaż jawnie przez `--prior-run PATH`.

Polecenie zamraża nasz proces z jednego commita i kopię poprzedniego raportu w nowym pakiecie; tworzy nowy run_id oraz `output_root`. Po logowaniu kodem urządzenia do posiadanego konta ChatGPT **automatycznie podaje prompt nowej sesji Codexa**. Nie trzeba składać ścieżek, kopiować plików ani wklejać promptu. To zmiana względem starego launchera independent-design, który otwiera pustą sesję.

Model i poziom można podać przed startem przez `--model` i `--reasoning`, używając identyfikatorów z faktycznego klienta. Bez tych opcji klient używa swoich ustawień domyślnych, nie automatycznie najmocniejszego modelu. Nie zgaduj wartości „Ultra”/„max” ani identyfikatorów API. Faktyczne ustawienia trzeba odnotować w wyniku.

Powstaną `design-review.md` (ocena obu projektów) i `process-proposal.md` (kandydat minimalnego procesu v0.2). Nie są tworzone przez samo przygotowanie. Szczegóły: [docs/design-review-command.md](docs/design-review-command.md).

## Warunki wykonania

`--update` działa tylko na czystym checkoutcie, wyłącznie fast-forward, i ponownie wczytuje aktualny skrypt. Nie zmienia starego pakietu ani wyników. Nie uruchamiaj przygotowania w sesji recenzenta mającej dostęp do całego repo.

Flaga `--allow-unverified-isolation` dotyczy wyłącznie eksploracyjnego zadania tej rundy. Osobny profil i read-only bity nowej kopii nie stanowią pełnej izolacji. `isolation_verified` pozostaje false. Obie propozycje są tu celowo dozwolonym wejściem; historia rozmowy, ocena koordynatora i obce instrukcje nadal nie są dozwolone. Journal oraz całe repo nie trafiają do recenzenta.

Po doświadczeniu z pierwszej próby drugi launcher żąda `workspace-write` z polityką `never`: nie wolno ponawiać operacji poza niesprawnym sandboxem. To nie naprawia konfiguracji serwera ani nie dowodzi działania zabezpieczeń. Zachowaj wynik blokady; nie luzuj ustawień, nie zmieniaj starego statusu i nie traktuj powrotu klienta z kodem zero jako dowodu ukończenia.

## Co robi koordynator po drugiej rundzie

Przeczytaj oba raporty i rzeczywisty rekord, sprawdź identyfikatory/hashe, ograniczenia i deklarowane ustawienia. Zachowaj wejścia i wyniki z jednoznacznym pochodzeniem; przed publikacją usuń sekrety z ewentualnych logów, ale nie podmieniaj zamrożonego raportu. Nie publikuj cache logowania lub pełnych prywatnych sesji.

Oddziel rekomendacje recenzenta od decyzji Damiana. Zestaw zaakceptowane i odrzucone zmiany, koszt dodatkowych etapów oraz warunki pilotażu. Comparative review pozostaje osobną rundą zgodnie z planem; nie deklaruj, że ten skrypt je wykonał. Zmiany procesu stosuj dopiero jako jawny kolejny commit po decyzji, a journal aktualizuj wraz z decyzją. Po G1: Architekt na surowym źródle, potem review jego raportu i zatrzymanie przed Plannerem na G2. Nie uruchamiaj teraz migracji.

## Instrukcja dla kolejnego koordynatora

> Pracujesz nad flatplanetpl/RustyBun. Odczytaj aktualne AGENTS.md, ten dokument, brief, plan i instrukcję design-review. Najpierw sprawdź faktyczny stan repo i dostarczone artefakty. Nie zakładaj, że przygotowany pakiet lub zamknięcie klienta oznacza ukończony raport. Rozróżniaj independent design, design review i comparative review. Nie udawaj czystej sesji, jeśli odziedziczyłeś kontekst koordynatora. Nie zatwierdzaj bramek za Damiana. Nie uruchamiaj płatnego API ani migracji. Ważne decyzje i korekty dopisuj do docs/presentation-journal.md. Podaj dowody wykonania i następny konkretny krok.

Ten tekst jest dla koordynatora, nie dla recenzenta. Recenzent otrzymuje wyłącznie wygenerowany pakiet i jawne metadane startowe.

## Pozostałe polecenia

Przygotowanie drugiej rundy bez logowania i modelu:

```bash
python3 scripts/design-review.py --allow-unverified-isolation
```

Pierwszą rundę powtarzaj tylko świadomie jako inny eksperyment:

```bash
python3 scripts/independent-review.py --update --launch --allow-unverified-isolation
```

[Instrukcja pierwszej rundy](docs/independent-review-command.md) · [Preflight i starsze helpery](docs/preflight-start.md) · [Protokół czystego kontekstu](docs/clean-context-review.md).

`build-context-pack.py` nadal eksportuje tylko wersjonowane wejścia. Sam `--kind design-review` nie dodaje poprzedniego wyniku — do kompletnej drugiej rundy użyj nowego polecenia. Comparative review i Architect wymagają własnych rekordów oraz odpowiednich decyzji; ten launcher ich nie autoryzuje.
