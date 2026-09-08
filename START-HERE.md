# Przekazanie RustyBun do kolejnej sesji

## Stan wejściowy

Repo: `flatplanetpl/RustyBun`. To pakiet przygotowawczy v0.1 z poprawkami preflight i uruchamiania. Materiały upstream, analiza wyboru SHA, kontrakty ról, prompty, protokół recenzji i dziennik są w repo. Operator zgłosił najpierw brak rekordu, a później blokadę z powodu widocznych instrukcji i pamięci innego projektu. Nie zweryfikowaliśmy jego plików wynikowych ani ukończonego niezależnego projektu. Brak wyników parity. Nie przedstawiaj tego jako gotowej migracji.

## Najbliższe zadanie

**Najpierw niezależna ocena procesu, nie implementacja.**

1. Sprawdź repo i testy narzędzi. Przeczytaj brief i plan jako koordynator, nie jako ślepy recenzent.
2. Zachowaj istniejący pakiet `independent-design`. W zwykłym terminalu operatora przygotuj nową próbę poleceniem poniżej. Nie wznawiaj sesji, która widziała wykluczone treści; zachowaj jej raport blokady.
3. Zamroź odpowiedź, manifest, rekord i instrukcję startową w `results/<run-id>/`. Wynik z niezweryfikowaną izolacją oznacz jako rozpoznawczy, nie jako dowód niezależności. Dopiero w nowej sesji podaj pakiet `design-review`, aby ocenić nasze role/prompty. Wcześniejszy wariant recenzenta można dołączyć jako jawny dodatkowy artefakt z hashem.
4. Osobna runda `comparative-review` otrzymuje materiały referencyjne. Jej wyniki nie nadpisują ani nie są dopisywane wstecz do rundy ślepej.
5. Koordynator proponuje zmiany procesu i przedstawia Damianowi bramkę G1. Nie traktuj tej instrukcji jako automatycznej akceptacji G1.
6. Po G1 przygotuj `architect` na surowym SHA, w izolacji od źródeł migracji. Przeprowadź niezależny przegląd raportu Architekta. Zatrzymaj się na G2 — przed Plannerem i kodowaniem.

## Jedno polecenie — nowa próba na Ubuntu

Stary checkout musi najpierw otrzymać nowe narzędzie przez `git pull --ff-only`. Następnie w katalogu RustyBun:

```bash
python3 scripts/independent-review.py --update --launch --allow-unverified-isolation
```

Polecenie zastępuje ręczne tworzenie `RUN_ID`, dobieranie ścieżki wyników, uruchamianie helpera i zakładanie oddzielnego profilu. `--update` wykonuje wyłącznie `git pull --ff-only` na czystym checkoutcie i ponownie wczytuje zaktualizowany launcher. Istniejący pakiet wejściowy oraz jego process SHA nie zmieniają się. Każda próba otrzymuje nowy identyfikator i katalog; poprzednie wyniki zostają.

Skrypt wypisuje cały handoff. Z `--launch` tworzy osobny tymczasowy HOME/CODEX_HOME/XDG, prosi o logowanie kodem urządzenia do posiadanego konta ChatGPT i otwiera pustą sesję Codex CLI w katalogu wyników. Wybierz model/poziom rozumowania, a następnie wklej tekst pomiędzy `BEGIN REVIEWER PROMPT` i `END REVIEWER PROMPT`. Wypisanie następuje także po logowaniu. Kopia instrukcji pozostaje w `START-REVIEW.txt`. Nie trzeba otwierać pliku ani składać promptu z czatu.

Bez uruchamiania klienta, logowania lub sieci:

```bash
python3 scripts/independent-review.py --allow-unverified-isolation
```

Nie podawaj recenzentowi tego dokumentu, kodu launchera, journal ani całego repo. Domyślny pakiet to `../RustyBun-review-01`; inny wskaż przez `--pack`. `--output-parent` zmienia katalog nadrzędny wyników. Wartości modeli i poziomów rozumowania muszą pochodzić z rzeczywistego klienta, nie z domysłów.

**Ważne ograniczenie:** osobny profil nie jest kontenerem ani blokadą wszystkich odczytów spoza pakietu. Ustawienia systemowe/administracyjne nadal obowiązują, a niektóre pliki mogą być dostępne. `isolation_verified` pozostaje false; znany wyciek treści nadal blokuje pracę. Nie luzuj bramek i nie przekonuj zablokowanego recenzenta do kontynuacji. [Uzasadnienie, referencje i obsługa błędów](docs/independent-review-command.md).

## Gotowy prompt do sesji tekstowej koordynatora

> Pracujesz nad publicznym repo flatplanetpl/RustyBun. Nie masz zakładać żadnej wiedzy z wcześniejszej rozmowy. Pobierz aktualny stan repo, przeczytaj AGENTS.md, START-HERE.md, docs/project-brief.md, docs/experiment-plan.md i docs/clean-context-review.md. Zrealizuj najbliższy nieukończony etap przygotowania/weryfikacji procesu. Najpierw sprawdź faktyczny stan plików i testy narzędzi. Przygotuj pakiet dla niezależnego recenzenta zgodnie z allowlistą, a nie przez przekazanie całego repo. Dostarcz rekord uruchomienia i output_root przed startem. Nie udawaj niezależnej sesji, jeśli odziedziczyłeś kontekst koordynatora. Nie rozpoczynaj migracji, nie uruchamiaj płatnego API i nie zatwierdzaj bramek za Damiana. Każdą istotną decyzję lub korektę dopisz do docs/presentation-journal.md. Zapisz produkty etapu i podaj dokładne dowody wykonania oraz następny punkt wymagający decyzji.

Ten prompt jest dla koordynatora, NIE dla ślepego recenzenta. Recenzent otrzymuje wygenerowany `TASK.md`, wyłącznie pliki z manifestu oraz jawne metadane operatora: rekord uruchomienia i instrukcję startową. Launcher nie jest kolejnym agentem ani wykonawczym pipeline'em migracji.

## Eksport i niższy poziom narzędzi

Eksportuj tylko nieistniejący pakiet. Istniejącego nie zastępuj dla „naprawienia” uruchomienia:

```bash
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
```

Dotychczasowy `prepare-review-run.py` nadal działa; używa go nowe polecenie. Ręczny interfejs jest opisany w [docs/preflight-start.md](docs/preflight-start.md). `--show-handoff` tylko wyświetla istniejącą, nierozpoczętą próbę; nie przygotowuje brakującego rekordu. W trybie niskopoziomowym nowy run_id i katalog trzeba nadal podać samodzielnie.

Flaga `--allow-unverified-isolation` oznacza świadomą zgodę operatora na **rozpoznawczy projekt procesu** przy niezweryfikowanej izolacji. Nie potwierdza izolacji ani niezależności; raport musi to ujawnić. Bez flagi przygotowanie pozostawia wykonanie zablokowane. To wyjątek tylko dla `independent-design`, nie dla Architekta, migracji lub akceptacji bramek.

Nieznany model/klient/ustawienia zapisujemy jako `unknown`, niesprawdzone elementy izolacji jako `null`. `PREPARED` oznacza metadane startowe, nie wykonane zadanie. `launcher.CLIENT_EXITED` dotyczy procesu klienta, nie jakości ani ukończenia projektu. Właściwy status roli, daty wykonania i pomiary muszą wynikać z rzeczywistej pracy. Nie zmieniaj `isolation_verified` na true dla ominięcia blokady.

Brak wejść, rozbieżne hashe, niedostępny output_root lub znany wyciek wykluczonych treści nadal blokują pracę. Gdy agent zatrzymał się wyłącznie na preflight i nie dostał obcych propozycji, można dostarczyć mu instrukcję startową w tej sesji. Gdy widział dodatkowe treści — nowa sesja i osobny run_id. Dla innych ścieżek montowania kontenera jawnie dostosuj ścieżki rekordu i zapisanej instrukcji przed startem. Istniejący katalog wyników nie jest nadpisywany.

Tymczasowy profil usuwa się po normalnym zakończeniu klienta; wyniki zostają. Przed publikacją audytuj raport i metadane. Nie publikuj cache logowania ani surowych prywatnych sesji. Usunięcie profilu nie przywraca limitu konta.

## Dalsze pakiety — osobne rundy

```bash
python3 scripts/build-context-pack.py --kind design-review --out ../RustyBun-review-02
python3 scripts/build-context-pack.py --kind comparative-review --out ../RustyBun-review-03
# Dopiero po G1:
bash scripts/bootstrap-bun-baseline.sh
python3 scripts/build-context-pack.py --kind architect --bun-repo work/bun --out ../RustyBun-architect-01
```

Dla tych etapów operator nadal uzupełnia osobne rekordy z szablonu i wymagane zgody. Helper i launcher pierwszej rundy ich nie autoryzują.

Eksporter pobiera wersjonowane wejścia z HEAD, więc lokalne niezatwierdzone edycje nie trafiają do pakietu. Zawsze sprawdź SHA w MANIFEST.json. Dla Architekta eksportuje commit kodu, nie katalog roboczy; pomija historię Git, symlinki i znane pliki sterujące agentami, zapisując pominięcia. To nie jest gotowe środowisko builda.

Dla zweryfikowanego blind review operator musi zapewnić i sprawdzić izolację od dodatkowej pamięci, historii i plików oraz odpowiednie uprawnienia. Nie montuj całego home, głównego repo ani credentiali GitHub. W interfejsie bez możliwości odizolowania repo użyj nowej rozmowy i załącz tylko pliki pakietu oraz metadane operatora; brak narzędzi do kodu oznacza review metodologii, nie weryfikację implementacji.
