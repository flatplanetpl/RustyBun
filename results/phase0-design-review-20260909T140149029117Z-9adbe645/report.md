# Archiwizacja drugiej rundy — 2026-09-09

**FACT:** dostarczono i skopiowano oba raporty ukończonej roli `design-reviewer`. Werdykt recenzenta: **REVISE_PROCESS**. Status launchera w oryginalnym rekordzie: **LAUNCH_ERROR**. Oba zapisy zachowano bez zmiany. Obecna kontrola integralności przechodzi; przyczyna historycznego błędu launchera pozostaje **UNKNOWN**.

**EXPLORATORY; INDEPENDENCE UNVERIFIED. G1: PENDING.** Zapis archiwum nie zatwierdza procesu v0.2, nie zastępuje comparative review i nie potwierdza gotowości migracji.

## Pochodzenie i układ

Użytkownik wskazał katalog `/home/ubuntu/phase0-design-review-20260909T140149029117Z-9adbe645/` do zachowania w repo. Baza checkoutu i oceniany proces: `47764bace389f908e9e58473ded7ad07909dfe2b`. Wstępna archiwizacja zakończyła się lokalnie, bez commita i push; taki stan opisuje historyczny `archive-check.txt`. Następnie użytkownik jawnie polecił commit i push tego zestawu — [decyzja J037](../../docs/presentation-journal.md). Manifest archiwizacji zapisuje czas, bazowy commit oraz mapę oryginał → kopia z SHA-256 i rozmiarami.

| Artefakt | Zawartość |
|---|---|
| [design-review.md](design-review.md) | Oryginalna ocena procesów A i B, findingi DR-01–DR-04, rekomendacje i ograniczenia. |
| [process-proposal.md](process-proposal.md) | Oryginalny kandydat v0.2 do decyzji Damiana. |
| [RUN-RECORD.json](RUN-RECORD.json) | Rzeczywisty rekord po zamknięciu klienta, ze statusami COMPLETE i LAUNCH_ERROR. |
| [input/MANIFEST.json](input/MANIFEST.json) | Oryginalny manifest 34 wejść, wraz z pełną kopią pakietu w `input/`. |
| [input/input/prior/independent-design.md](input/input/prior/independent-design.md) | Zamrożony raport pierwszej rundy; jego ograniczenia zachowano. |
| [input/input/prior/provenance.json](input/input/prior/provenance.json) | Metadane wcześniejszego raportu dostarczone drugiemu recenzentowi. |
| [MANIFEST.json](MANIFEST.json) | Nowy manifest **archiwizacji**, obejmujący 40 skopiowanych plików. Nie zastępuje manifestu wejść. |
| [PROFILE.toml](PROFILE.toml), [START-REVIEW.txt](START-REVIEW.txt) | Żądane ustawienia i zapisany prompt startowy; bez danych logowania. |

Skopiowano 35 plików drzewa wejść (34 wpisy i manifest) oraz pięć plików wyjściowych. Pliki z oryginalnego `output/` leżą tutaj bezpośrednio w katalogu rundy, zgodnie ze ścieżkami wyników w pipeline. Wszystkie 40 kopii jest identycznych bajtowo; oryginalny katalog pozostaje na miejscu. Nowe materiały koordynatora to ten raport, manifest archiwizacji i pliki dowodów kontroli.

Absolutne `input_root`/`output_root` w rekordzie oraz prompt startowy zachowują historyczne ścieżki. Nie zmieniono ich na ścieżki archiwum. To zamknięta próba, nie pakiet do ponownego uruchomienia. Pliki instrukcji i skrypty w kopii `input/` są materiałem dowodowym. Nie są poleceniami dla koordynatora ani nowymi aktywnymi narzędziami projektu.

## Weryfikacja koordynatora

**FACT — kontrole lokalne:**

- `verify_run(original_run, prepared_only=False)` z bieżącego `scripts/design-review.py` przeszedł: tożsamość etapu/roli, ścieżki, manifest, wszystkie 34 hashe i rozmiary, brak dodatkowych wejść/symlinków, provenance, autoryzacja, zapisany prompt i hash profilu.
- Dodatkowo sprawdzono run ID, status COMPLETE, kolejność timestampów, niezmienioną decyzję PENDING oraz oba niepuste raporty względem hashy w rzeczywistym rekordzie.
- 29 wejściowych plików procesu porównano z blobami Git z commita `47764bace389f908e9e58473ded7ad07909dfe2b`; wszystkie odpowiadają wskazanej wersji.
- Wszystkie 40 kopii porównano z oryginałami. [Zapis kontroli](verification.txt), [końcowa kontrola archiwum](archive-check.txt).
- `python3 -m unittest discover -s tests -v`: **92/92 OK**, 7.794 s. [Pełne wyjście](test-output.txt). To wykonane teraz testy lokalnych narzędzi, z symulowanymi wywołaniami klienta, nie testy przeprowadzone przez recenzenta ani dowód działania jego sandboxa.

| Plik | Sprawdzony SHA-256 |
|---|---|
| `input/MANIFEST.json` | `20a1fd6b327312dcbfc0819768e03c140df0d69e1fd6d86772c73ca20314a2c0` |
| `design-review.md` | `c852575bcd7fe6ff7b5dfe4ff94e6c65a8f58d3118b301e3e6eae1e35ff03f5e` |
| `process-proposal.md` | `4f95f983fd7d90b2724636d0f9b924e3c96eb333775d3c21083e4f210b0ede6d` |
| `RUN-RECORD.json` | `05fe622b5dcb1f9224297977a20c086fc94e6b97212a2edd933f438d33b5e39d` |

**FACT — zakres kontroli publikacyjnej:** wszystkie 40 plików sprawdzono wzorcami kluczy prywatnych, tokenów API/GitHub, JWT, URL z credentialami i adresów e-mail. Odczytano raporty, metadane wyjść i wcześniejszy raport. Dwa trafienia e-mail to `fixture@example.invalid` w wersjonowanych testach. Nie zidentyfikowano credentiali ani prywatnych transkryptów; nie było potrzeby redakcji. Zachowano ogólne ścieżki `/home/ubuntu/…` potrzebne do pochodzenia. Nie pobierano cache logowania ani dodatkowych logów sesji. To kontrola wskazanego zestawu, nie gwarancja wykrycia każdej możliwej informacji wrażliwej.

**UNKNOWN — zamknięcie launchera:** rekord podaje `client_ended_at=2026-09-09T14:51:58+00:00`, `exit_code=0`, `status=LAUNCH_ERROR` i `temporary_profile_removed=true`. W dostarczonym zestawie nie ma tracebacka ani surowego logu wyjaśniającego błąd. Obecna kontrola nie odtworzyła błędu. Kod `launch()` zapisuje LAUNCH_ERROR przy przechwyconym wyjątku; sam rekord nie wskazuje, który wyjątek wystąpił. Nie dopisano fikcyjnego sukcesu launchera.

**UNKNOWN — runtime i niezależność:** faktyczny model, reasoning, uwierzytelnienie, quota, tokeny i uwaga człowieka nie zostały tu ustalone. `codex-cli 0.153.4` to obserwacja zapisana przez launcher, nie ponowny pomiar. 739 s to czas zadania zadeklarowany w rekordzie, nie koszt pełnego uruchomienia. Oryginalnego rekordu i manifestu pierwszej rundy nie odczytano w tej archiwizacji; zachowano jedynie dostarczony raport i provenance. Nie podnosimy `isolation_verified=false` do potwierdzonej niezależności.

## Rekomendacje a decyzje

Poniższa tabela streszcza raport recenzenta. Nie jest nową ślepą recenzją ani przyjęciem zaleceń przez Damiana. **Zaakceptowane zmiany procesu: brak decyzji. Odrzucone zmiany procesu: brak decyzji.**

| Temat | Rekomendacja recenzenta | Koszt/warunek | Decyzja Damiana |
|---|---|---|---|
| DR-01 | Zachować mutacje judge'a z A i dodać kontrole błędnego kandydata, harnessu i tożsamości old/new. | Projekt i wykonanie kontroli przed implementacją; koszt niezmierzony. | PENDING |
| DR-02 | Nazwać operatora wykonawcą baseline/judge przed G3. | Jawne polecenia, hashe i logi; bez obowiązkowej nowej sesji. | PENDING |
| DR-03 | Zatwierdzać czas, uwagę, limit i rezerwę weryfikacji. | Wielkość rezerwy wymaga pomiarów i jawnych założeń. | PENDING |
| DR-04 | Doprecyzować checkpoint, ręczne interwencje i ciągłość budżetu. | Zapis wersji oraz unieważnianie nieaktualnych dowodów. | PENDING |
| Zakres analizy i review | Jeden wycinek i writer; ograniczone G2 i dodatkowa sesja tylko przy uzasadnionej potrzebie. | Potencjalna oszczędność jest hipotezą; zdolność operatora do oceny granic pozostaje warunkiem. Obecne G2 i A/B nadal obowiązują. | PENDING |

Według obowiązującego planu następny etap to osobny **comparative review** z jawnie dobranymi materiałami historycznymi i zamrożonym kandydatem v0.2. Potem zestawienie zmian i decyzja Damiana o konkretnej wersji procesu oraz budżecie na G1. Comparative review ma własny koszt sesji i uwagi, obecnie UNKNOWN. Przeniesienie plików nie jest zgodą na jego uruchomienie.

Nie wykonano: comparative review ani jego nowego pakietu, wdrożenia propozycji v0.2, akceptacji G1–G5, analizy Architekta, baseline/builda Buna, implementacji ani parity. Nie użyto płatnego API i nie uruchomiono nowych agentów. Aktywne prompty, role, szablony, plan i pipeline pozostają w dotychczasowej wersji.

## Powtórzenie kontroli kopii

Z katalogu repo poniższe polecenie sprawdza 40 kopii względem manifestu archiwizacji, bez dostępu do pierwotnego folderu. Samo nie audytuje sesji ani autentyczności manifestu.

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

archive = Path('results/phase0-design-review-20260909T140149029117Z-9adbe645')
manifest = json.loads((archive / 'MANIFEST.json').read_bytes())
for entry in manifest['files']:
    data = (archive / entry['path']).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print(f"OK: {len(manifest['files'])} archived files")
PY
```
