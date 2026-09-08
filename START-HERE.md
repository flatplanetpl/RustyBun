# Przekazanie RustyBun do kolejnej sesji

## Stan wejściowy

Repo: `flatplanetpl/RustyBun`. To pakiet przygotowawczy v0.1 z poprawką kroku preflight. Materiały upstream, analiza wyboru SHA, kontrakty ról, prompty, protokół recenzji i dziennik są w repo. Zgłoszona próba review zatrzymała się na braku rekordu uruchomienia; nie jest ukończoną rundą projektową. Brak wyników parity. Nie przedstawiaj tego jako gotowej migracji.

## Najbliższe zadanie

**Najpierw niezależna ocena procesu, nie implementacja.**

1. Sprawdź repo i testy narzędzi. Przeczytaj brief i plan.
2. Przygotuj pakiet `independent-design` oraz oddzielny rekord uruchomienia i output_root. W nowej sesji recenzent widzi tylko cel i ograniczenia; projektuje własny wariant bez naszej propozycji. Nie podawaj samego TASK.md bez metadanych operatora.
3. Zamroź jego odpowiedź, manifest, rekord i instrukcję startową w `results/<run-id>/`. Wynik z niezweryfikowaną izolacją oznacz jako rozpoznawczy, nie jako dowód niezależności. Dopiero w nowej sesji podaj pakiet `design-review`, aby ocenić nasze role/prompty. Wcześniejszy wariant recenzenta można dołączyć jako jawny dodatkowy artefakt z hashem.
4. Osobna runda `comparative-review` otrzymuje materiały referencyjne. Jej wyniki nie nadpisują ani nie są dopisywane wstecz do rundy ślepej.
5. Koordynator proponuje zmiany procesu i przedstawia Damianowi bramkę G1. Nie traktuj tej instrukcji jako automatycznej akceptacji G1.
6. Po G1 przygotuj `architect` na surowym SHA, w izolacji od źródeł migracji. Przeprowadź niezależny przegląd raportu Architekta. Zatrzymaj się na G2 — przed Plannerem i kodowaniem.

## Gotowy prompt do sesji tekstowej koordynatora

> Pracujesz nad publicznym repo flatplanetpl/RustyBun. Nie masz zakładać żadnej wiedzy z wcześniejszej rozmowy. Pobierz aktualny stan repo, przeczytaj AGENTS.md, START-HERE.md, docs/project-brief.md, docs/experiment-plan.md i docs/clean-context-review.md. Zrealizuj najbliższy nieukończony etap przygotowania/weryfikacji procesu. Najpierw sprawdź faktyczny stan plików i testy narzędzi. Przygotuj pakiet dla niezależnego recenzenta zgodnie z allowlistą, a nie przez przekazanie całego repo. Dostarcz rekord uruchomienia i output_root przed startem. Nie udawaj niezależnej sesji, jeśli odziedziczyłeś kontekst koordynatora. Nie rozpoczynaj migracji, nie uruchamiaj płatnego API i nie zatwierdzaj bramek za Damiana. Każdą istotną decyzję lub korektę dopisz do docs/presentation-journal.md. Zapisz produkty etapu i podaj dokładne dowody wykonania oraz następny punkt wymagający decyzji.

Ten prompt jest dla koordynatora, NIE dla ślepego recenzenta. Recenzent otrzymuje wygenerowany `TASK.md`, wyłącznie pliki z manifestu oraz jawne metadane operatora: rekord uruchomienia i instrukcję startową. Nie otrzymuje tej strony ani journal.

## Pierwsza runda — pakiet i rekord

```bash
# W katalogu RustyBun; istniejącego pakietu nie eksportuj ponownie.
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
python3 scripts/prepare-review-run.py --pack ../RustyBun-review-01 --out ../RustyBun-review-01-output --run-id phase0-independent-20260908-01 --allow-unverified-isolation
```

Druga komenda działa również na pakiecie wyeksportowanym ze starego commita. Weryfikuje hashe; nie modyfikuje wejść ani MANIFEST.json. Tworzy `RUN-RECORD.json` i `START-REVIEW.txt` w oddzielnym output_root. **Wypisuje od razu kompletną instrukcję przekazania:** katalog wejść tylko do odczytu, katalog wyników do odczytu/zapisu, gotowy tekst pomiędzy znacznikami `BEGIN REVIEWER PROMPT` / `END REVIEWER PROMPT` oraz miejsce oczekiwanego raportu. Wklej tekst między znacznikami do sesji recenzenta mającej dostęp tylko do tych katalogów. Nie trzeba osobno otwierać pliku. Nie uruchamiaj przygotowania metadanych wewnątrz ślepej sesji z dostępem do całego repo.

Jeżeli katalog wyników już przygotowano, ale zadanie jeszcze nie ruszyło, skrypt może ponownie wypisać instrukcję bez zapisu, nowego rekordu lub zmiany autoryzacji:

```bash
python3 scripts/prepare-review-run.py --show-handoff ../RustyBun-review-01-output
```

Tryb ten kontroluje spójność wejść, rekordu i zapisanej instrukcji. Nie służy do ponownego uruchamiania rozpoczętej lub zakończonej próby. Samo wypisanie/wklejenie tekstu nie nadaje agentowi dostępu do katalogów ani nie tworzy sandboxa.

Flaga `--allow-unverified-isolation` oznacza świadomą zgodę operatora na **rozpoznawczy projekt procesu** przy niezweryfikowanej izolacji. Nie potwierdza izolacji ani niezależności; raport musi to ujawnić. Bez flagi przygotowanie pozostawia wykonanie zablokowane do czasu kontroli/zgody operatora. To wyjątek tylko dla `independent-design`, nie dla Architekta, migracji lub akceptacji bramek.

Nieznany model/klient/ustawienia zapisujemy jako `unknown`, niesprawdzone elementy izolacji jako `null`. `PREPARED` oznacza uzupełnione metadane startowe, a nie wykonane zadanie. `started_at`, `ended_at` i pomiary uzupełnia się dopiero przy rzeczywistym wykonaniu. Nie zmieniaj `isolation_verified` na `true` dla ominięcia blokady.

Brak wejść, rozbieżne hashe, niedostępny output_root lub znany wyciek wykluczonych treści nadal blokują pracę. Gdy agent zatrzymał się wyłącznie na preflight i nie dostał obcych propozycji, można dostarczyć mu instrukcję startową w tej sesji. Gdy widział dodatkowe treści — nowa sesja i osobny run_id. Dla innych ścieżek montowania kontenera jawnie dostosuj ścieżki rekordu i zapisanej instrukcji przed startem. Istniejący katalog wyników nie jest nadpisywany; dla kolejnej próby wybierz nowy.

## Dalsze pakiety — osobne rundy

```bash
python3 scripts/build-context-pack.py --kind design-review --out ../RustyBun-review-02
python3 scripts/build-context-pack.py --kind comparative-review --out ../RustyBun-review-03
# Dopiero po G1:
bash scripts/bootstrap-bun-baseline.sh
python3 scripts/build-context-pack.py --kind architect --bun-repo work/bun --out ../RustyBun-architect-01
```

Dla tych etapów operator nadal uzupełnia osobne rekordy z szablonu i wymagane zgody. Helper pierwszej rundy ich nie autoryzuje.

Eksporter pobiera wersjonowane wejścia z HEAD, więc lokalne niezatwierdzone edycje nie trafiają do pakietu. Zawsze sprawdź SHA w MANIFEST.json. Dla Architekta eksportuje commit kodu, nie katalog roboczy; pomija historię Git, symlinki i znane pliki sterujące agentami, zapisując pominięcia. To nie jest gotowe środowisko builda.

Uruchom agenta w odizolowanym środowisku z wejściami read-only i oddzielnym katalogiem wyjściowym. Nie montuj całego home, głównego repo ani credentiali GitHub. Konto/model wybiera operator; zapisz faktyczne ustawienia. W interfejsie bez możliwości odizolowania repo użyj nowej rozmowy i załącz tylko pliki pakietu oraz metadane operatora; brak narzędzi do kodu oznacza review metodologii, nie weryfikację implementacji.
