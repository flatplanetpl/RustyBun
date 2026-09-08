# Przekazanie RustyBun do kolejnej sesji

## Stan wejściowy

Repo: `flatplanetpl/RustyBun`. To pakiet przygotowawczy v0.1. Materiały upstream i analiza wyboru SHA już istniały; obecny etap dodaje kontrakty ról, prompty, protokół recenzji i dziennik. Brak wykonanych rund agentowych i wyników parity. Nie przedstawiaj tego jako gotowej migracji.

## Najbliższe zadanie

**Najpierw niezależna ocena procesu, nie implementacja.**

1. Sprawdź repo i testy narzędzi. Przeczytaj brief i plan.
2. Przygotuj pakiet `independent-design`. W nowej sesji recenzent widzi tylko cel i ograniczenia; projektuje własny wariant bez naszej propozycji.
3. Zamroź jego odpowiedź i manifest w `results/<run-id>/`. Dopiero w nowej sesji podaj pakiet `design-review`, aby ocenić nasze role/prompty. Wcześniejszy wariant recenzenta można dołączyć jako jawny dodatkowy artefakt z hashem.
4. Osobna runda `comparative-review` otrzymuje materiały referencyjne. Jej wyniki nie nadpisują ani nie są dopisywane wstecz do rundy ślepej.
5. Koordynator proponuje zmiany procesu i przedstawia Damianowi bramkę G1. Nie traktuj tej instrukcji jako automatycznej akceptacji G1.
6. Po G1 przygotuj `architect` na surowym SHA, w izolacji od źródeł migracji. Przeprowadź niezależny przegląd raportu Architekta. Zatrzymaj się na G2 — przed Plannerem i kodowaniem.

## Gotowy prompt do sesji tekstowej koordynatora

> Pracujesz nad publicznym repo flatplanetpl/RustyBun. Nie masz zakładać żadnej wiedzy z wcześniejszej rozmowy. Pobierz aktualny stan repo, przeczytaj AGENTS.md, START-HERE.md, docs/project-brief.md, docs/experiment-plan.md i docs/clean-context-review.md. Zrealizuj najbliższy nieukończony etap przygotowania/weryfikacji procesu. Najpierw sprawdź faktyczny stan plików i testy narzędzi. Przygotuj pakiet dla niezależnego recenzenta zgodnie z allowlistą, a nie przez przekazanie całego repo. Nie udawaj niezależnej sesji, jeśli odziedziczyłeś kontekst koordynatora. Nie rozpoczynaj migracji, nie uruchamiaj płatnego API i nie zatwierdzaj bramek za Damiana. Każdą istotną decyzję lub korektę dopisz do docs/presentation-journal.md. Zapisz produkty etapu i podaj dokładne dowody wykonania oraz następny punkt wymagający decyzji.

Ten prompt jest dla koordynatora, NIE dla ślepego recenzenta. Recenzent otrzymuje wygenerowany `TASK.md` oraz wyłącznie pliki z manifestu.

## Uruchomienie pakietów

```bash
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
python3 scripts/build-context-pack.py --kind design-review --out ../RustyBun-review-02
python3 scripts/build-context-pack.py --kind comparative-review --out ../RustyBun-review-03
# Dopiero po G1:
bash scripts/bootstrap-bun-baseline.sh
python3 scripts/build-context-pack.py --kind architect --bun-repo work/bun --out ../RustyBun-architect-01
```

Skrypt eksportuje wersjonowane wejścia z HEAD, więc lokalne niezatwierdzone edycje nie trafiają do pakietu. Zawsze sprawdź SHA w MANIFEST.json. RUN-RECORD.template.json skopiuj do rekordu nowej próby, uzupełnij run_id, role_id, ustawienia i output_root przed wywołaniem; template sam nie spełnia preflight. Dla Architekta eksportuje commit kodu, nie katalog roboczy; pomija historię Git, symlinki i znane pliki sterujące agentami, zapisując pominięcia. To nie jest gotowe środowisko builda.

Uruchom agenta w odizolowanym środowisku z wejściami read-only i oddzielnym katalogiem wyjściowym. Nie montuj całego home, głównego repo ani credentiali GitHub. Konto/model wybiera operator; zapisz faktyczne ustawienia. W interfejsie bez możliwości odizolowania repo użyj nowej rozmowy i załącz tylko pliki pakietu; brak narzędzi do kodu oznacza review metodologii, nie weryfikację implementacji.
