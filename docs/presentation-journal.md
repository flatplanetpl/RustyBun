# RustyBun — dziennik materiałów do prezentacji

Materiał źródłowy do przyszłego wystąpienia, nie gotowe slajdy. Powstał 2026-09-08. Wpisy z rozmowy są odtworzeniem ustaleń, nie logiem wykonanych eksperymentów. Zwięzłe hasła poniżej to propozycje redakcyjne, nie dosłowne cytaty użytkownika ani autorów upstream.

## Oznaczenia

DECISION — ustalenie rozmowy; PROPOSAL — nowa propozycja do review; OBSERVATION — odczytany artefakt lub pomiar; HYPOTHESIS — teza do zbadania; CORRECTION — korekta wcześniejszego uproszczenia. Wpis wyniku wymaga ścieżki do dowodu i SHA; brak danych pozostaje UNKNOWN.

## 2026-09-08 — od historii migracji do własnego eksperymentu

**DECISION J001 — próbujemy na abonamencie.** Pomysł: użyć własnej pracy i Codexa w Pro zamiast zakładać budżet płatnego API. Nie deklarujemy, że wykonamy całość ani że koszt będzie porównywalny z cudzym rachunkiem. Dokładny koszt historycznej migracji, dostępność modeli i oferta resetów wspomniana w rozmowie wymagają osobnego potwierdzenia przed wystąpieniem.

**DECISION J002 — harness to więcej niż tooling.** Roboczo: narzędzia plus reguły ich użycia, przekazania pracy, pętle kontroli i kryteria zakończenia. Smaczek narracyjny: przejście od pytania „co to za słowo?” do świadomego zaprojektowania procesu.

**DECISION J003 — plik nie jest jednostką zachowania.** Użytkownik zakwestionował skalowanie „3 → 10 → 50 plików”. Przechodzimy do funkcjonalnych jednostek z kontraktem, zależnościami i testami. Nie każdy slice musi przecinać wszystkie warstwy; spójny moduł również może być dobrą jednostką.

**DECISION J004 — najpierw zbadać zależności.** Rozważamy port 1:1, adapter, minimalny kontrakt, bridge lub redesign. Nie wybieramy automatycznie wariantu „wszystko przepisać w Rust”. HYPOTHESIS: mniejszy używany interfejs pozwoli ograniczyć zakres. Kontrprzykład do pokazania: mała sygnatura może skrywać trudne ownership, kolejność callbacków i semantykę błędów.

**DECISION J005 — analiza przed kodowaniem.** Ustalona kolejność: Architect → Planner → implementacja → niezależny review → poprawki → mechaniczna weryfikacja. Dwie sesje review nie są dowodem poprawności; ich uwagi muszą prowadzić do sprawdzalnych ustaleń.

**DECISION J006 — publiczne repo i jawne pochodzenie.** RustyBun na koncie flatplanetpl; materiały obce w sources/github.com/<owner>/<repo>/, nasze artefakty poza nimi. Archiwum ma zachować licencje i przypięte SHA, a nie udawać naszą implementację.

**DECISION J007 — zamrożenie źródła.** Surowy kod: 0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f. Referencja z instrukcją Phase A: 46d3bc29f270fa881dd5730ef1549e88407701a5. Odrzucono nowszy base PR-a jako dodatkową zmienną eksperymentu. Dowód i ograniczenia: [analiza baseline](upstream-baseline-analysis.md), wcześniejsza wersja repo a1527be0274985ba0e48144dbdd26b2340cd9440.

**DECISION J008 — niezależna ocena promptów i ról.** Recenzent musi dostać cel, ograniczenia i kontrakty I/O, nie tylko „popraw ten prompt”. Najpierw niezależny wariant; potem krytyka naszej propozycji; materiały porównawcze ujawniamy w osobnej rundzie.

**DECISION J009 — Architekt bez podglądania instrukcji migracji.** Pierwszą analizę chcemy wykonać na kodzie, nie na gotowych decyzjach wcześniejszego portu. Wynik zamrażamy przed ewentualnym porównaniem. To kontrola udostępnionych wejść, nie dowód braku znajomości Buna przez model z treningu.

**DECISION J010 — journal jest częścią procesu.** Zapisujemy decyzję, powód, odrzucony wariant, konsekwencję, dowód i materiał narracyjny. Aktualizacja w tym samym zestawie zmian, nie retrospektywne dopisywanie wyłącznie sukcesów.

## 2026-09-08 — korekty i przygotowanie v0.1

**CORRECTION J011 — nie twierdzimy, że Sumner nie analizował architektury.** Sam [PORTING.md](../sources/github.com/oven-sh/bun/commit-46d3bc29/docs/PORTING.md) zawiera mapę crates i reguły ownership/FFI oraz odwołanie do analizy lifetime. Nasza różnica to badana dekompozycja i jawne kontrakty, nie rzekomy brak planowania u autora. Przewaga pozostaje hipotezą.

**CORRECTION J012 — „dokładnie ich pierwszy stan” było zbyt mocne.** Historia potwierdza odtwarzalną granicę Phase A i relację commitów. Nie potwierdza całej zawartości dysku ani pierwszej prywatnej sesji autora.

**CORRECTION J013 — community harness nie jest oficjalnym, działającym runnerem.** W skopiowanym [multi-agent-orchestration.ts](../sources/github.com/Lumafy/sumner-method/workflows/multi-agent-orchestration.ts) wywołania agentów są szkicami, a validateFix zwraca true. To materiał koncepcyjny do oceny, nie dowód wykonanej migracji ani komponent gotowy do podłączenia.

**OBSERVATION J014 — wyciek kontekstu był już w naszym bootstrapie.** Odczytany skrypt domyślnie wybierał commit z PORTING.md. Przygotowanie v0.1 zmienia domyślny checkout na surowe źródło i dodaje eksport pakietów bez historii Git i znanych plików instrukcji. Rozdzielamy „źródło do analizy” od „materiału do porównania”.

**PROPOSAL J015 — bounded pilot.** Jeden writer, dwie niezależne sesje review, najwyżej dwie rundy poprawek, checkpoint po blokadzie. Najpierw jedna testowalna jednostka; dwa trudniejsze przypadki dopiero po wyniku. To proponowane parametry, nie zmierzone optimum ani automatyczna zgoda na run.

**OBSERVATION J016 — stan przygotowania.** Dodano opisy ról, prompty, szablony danych, bramki, pakiety review i instrukcję przekazania. To artefakty przygotowawcze. Nie wykonano niezależnej rundy LLM, pełnego audytu źródeł, builda Buna ani testów parity. Próba pobrania repo przez Git w środowisku wykonania nie powiodła się z powodu DNS; odczyt i zapis repo odbywa się przez konektor GitHub.

**OBSERVATION J017 — narzędzia poddane testom.** Eksporter przeszedł 8 testów offline na lokalnych fixture'ach Git, a bootstrap kontrolę składni Bash. [Dowód](../results/tooling-validation-20260908/report.md). To wynik narzędzi przygotowawczych, nie migracji ani review niezależnego modelu.

## Hasła i sceny do rozważenia

- „Nie migrujemy plików. Migrujemy kontrakty i zachowania.”
- „Don't migrate Bun. Design the factory.” — propozycja hasła z rozmowy, nie cytat upstream.
- „Nowy kontekst zaczyna się od kontroli wejścia, nie od polecenia: zapomnij.”
- „Zielony build to nie zielona migracja.”
- Scena demonstracyjna: reviewer znajduje brak w kontrakcie przed pierwszą linią portu. Na razie pomysł, nie zdarzenie.
- Scena demonstracyjna: mutacja łamie zachowanie, a judge rzeczywiście ją wykrywa. Na razie zaplanowany dowód.

## Dane do zebrania przed slajdami z wynikami

SHA/model/konfiguracja każdej próby; zakres kontraktu i fixture'y; verified units zamiast LOC; czas człowieka i limit; znalezione błędy i false positives; odrzucone sugestie recenzentów; regresje po fixerze; przykłady decyzji zmienionych przez dowody. Cudze liczby cytujemy tylko z potwierdzonego źródła i nie porównujemy rachunku API wprost z ceną abonamentu.

## Szablon następnego wpisu

ID / data / typ / status decyzji; problem; decyzja lub obserwacja; alternatywa odrzucona i powód; konsekwencja; dowód (run, commit, ścieżka); teza do prezentacji; co mogłoby ją obalić. Korekty dopisuj jawnie, nie wymazuj wcześniejszego nieudanego podejścia.

## 2026-09-08 — pierwszy start zatrzymany na preflight

**OBSERVATION J018 — poprawna odmowa ujawniła brak w przekazaniu pracy.** Operator wkleił komunikat agenta: dostępny był tylko szablon NOT_RUN, brakowało uzupełnionego rekordu i output_root; agent nie zmienił plików. Eksporter w commicie fbf1b25115cd2455664d78523f127101bed66516 rzeczywiście wymagał dostarczenia rekordu przez operatora. Skrócona instrukcja z rozmowy „wykonaj TASK.md” pominęła ten krok. To zdarzenie operacyjne zgłoszone przez użytkownika, nie wykonany przez nas audyt jego sesji ani ukończony niezależny projekt. Hasło: „Agent odmówił poprawnie. Błąd był w naszym handoffie.”

**CORRECTION J019 — szablon to nie rekord, a przygotowanie to nie wykonanie.** Dodano [prepare-review-run.py](../scripts/prepare-review-run.py): odczyt manifestu, kontrola hashy, właściwy run_id/role_id/stage, rzeczywiste ścieżki input_root/output_root i status PREPARED. Rekord oraz instrukcja startowa trafiają poza wejściowy pakiet. started_at/ended_at i metryki pozostają niewypełnione do rzeczywistego wykonania. Odrzucono ręczne wpisanie fikcyjnego modelu, ścieżki dysku operatora albo statusu COMPLETE. Poprawka może obsłużyć stary pakiet bez zmiany SHA ocenianych wejść.

**PROPOSAL J020 — jawny tryb rozpoznawczy zamiast udawanej izolacji.** Helper domyślnie nie autoryzuje pracy przy niezweryfikowanej izolacji. Operator może jawnie wybrać --allow-unverified-isolation wyłącznie dla pierwszego zadania projektowego. Wynik musi wtedy ujawnić EXPLORATORY; INDEPENDENCE UNVERIFIED; isolation_verified pozostaje false. Brak danych/niezgodne hashe/niedostępny output lub znany wyciek treści nadal blokują pracę. Nie zmieniono bramek dla Architekta i migracji. Ta opcja nie jest dowodem, że operator ją już uruchomił lub że sandbox działa. [Dokładna semantyka](preflight-start.md).

**OBSERVATION J021 — testujemy również odmowę i uczciwość metadanych.** 15 nowych testów offline/CLI przeszło na Linux/Python 3.13.5. Obejmują brak nadpisywania, zachowanie wejść, wykrywanie zmiany hashy, brakujące i nadmiarowe pliki, bezpieczne ścieżki oraz brak automatycznego potwierdzania izolacji. [Raport, ograniczenia i hashe](../results/tooling-preflight-20260908/report.md). Nie wykonano jeszcze review w środowisku operatora. To nie wynik migracji.

**DECISION J022 — główny README po angielsku.** Zgodnie z prośbą operatora przetłumaczono główny README i dopisano brakujący krok przygotowania rekordu. Pozostałych promptów i briefu nie przetłumaczono ani nie rozszerzono przed pierwszą rundą. Znane materiały historyczne i pierwotne wpisy tego dziennika zachowano.

## 2026-09-08 — przekazanie do reviewera jako wynik skryptu

**DECISION J023 — instrukcja obsługi nie może pozostawać wyłącznie w rozmowie.** Użytkownik wskazał, że „co przekazać reviewerowi” powinno być częścią skryptu. Poprzedni helper zapisywał START-REVIEW.txt, ale w terminalu podawał tylko ścieżkę. Teraz po przygotowaniu wypisuje katalog wejść i wyników z zamierzonymi uprawnieniami, kompletny tekst do wklejenia między wyraźnymi znacznikami i oczekiwane miejsce raportu. Zapisana kopia zostaje do audytu. Odrzucono wymaganie osobnego otwierania pliku i składania instrukcji z czatu. Hasło do prezentacji: „Handoff jest produktem narzędzia, nie pamięcią operatora.” Nie oznacza to automatycznego montowania katalogów ani uruchomienia modelu.

**OBSERVATION J024 — poprawka działa także dla już przygotowanej próby.** Dodano --show-handoff: ponowne wypisanie po kontroli wejść/rekordu/instrukcji, bez zapisów, nowych timestampów lub zmiany zgody. Rekord wskazujący rozpoczęte/zakończone zadanie nie służy do nowego startu. 22/22 testy preflight/handoff oraz osobna próba zgodności z rekordem utworzonym poprzednim helperem przeszły lokalnie; pliki w tej próbie pozostały identyczne bajtowo. [Raport i hashe](../results/tooling-handoff-20260908/report.md). Prompt TASK, brief i bramki pozostały bez zmian. Wynik dotyczy narzędzia, nie reviewera w środowisku użytkownika.

## 2026-09-08 — ponowne wyświetlenie przed przygotowaniem rekordu

**OBSERVATION / CORRECTION J025 — komunikat błędu też jest częścią przekazania pracy.** Operator pokazał błąd Missing or non-regular input: RUN-RECORD.json po użyciu --show-handoff. Sam komunikat nie rozstrzyga, czy próby nie przygotowano, czy wskazano złą lub niepełną lokalizację. Wersja 1c1dc06128bf3df2b290569fdfa9bc687e9ff20f tylko odczytywała istniejący rekord; poprzednia odpowiedź w rozmowie zbyt mocno eksponowała redisplay zamiast pierwszego przygotowania. Poprawka podaje pełną oczekiwaną ścieżkę, wyjaśnia tryb i wskazuje składnię przygotowania, które już automatycznie wypisuje prompt. Odrzucono automatyczne tworzenie rekordu, nadpisywanie niepełnych wyników i kopiowanie pustego szablonu dla ominięcia preflight. Osiem nowych testów regresji przeszło na Linux/Python 3.13.5; pełnej wcześniejszej suite nie uruchamiano w tej poprawce. [Dowód i ograniczenia](../results/tooling-missing-record-20260908/report.md). Nadal nie jest to wykonana runda modelu. Hasło: „Nie wystarczy wykryć brak. Narzędzie powinno wskazać następny poprawny krok.”

## 2026-09-08 — nowa sesja nadal dziedziczyła kontekst

**OBSERVATION J026 — blokada przez widoczne obce instrukcje i pamięć.** Operator wkleił komunikat BLOCKED — EXPLORATORY; INDEPENDENCE UNVERIFIED. Reviewer zgłosił zapisanie raportu blokady i zamknięcie rekordu, zanim rozpoczął projekt lub ponownie sprawdził hashe wejść. To relacja użytkownika; nie odczytaliśmy jego plików ani nie potwierdziliśmy konkretnego źródła dodatkowego kontekstu. Poprzednia rada „nowa sesja” była niewystarczająca. Odrzucono przekonywanie agenta do zignorowania jawnego warunku stopu. Hasło: „Czyste wejście do zadania nie oznacza czystego środowiska agenta.”

**DECISION J027 — jedno polecenie i osobny profil przy nowej próbie.** Zgodnie z dwiema prośbami operatora dodano [independent-review.py](../scripts/independent-review.py): opcjonalny git pull --ff-only, automatyczny run_id i katalog wyników, istniejący helper oraz kompletny handoff. Z --launch otwiera nowy profil HOME/CODEX_HOME/XDG, z żądaniem wyłączenia pamięci/konektorów/browsingu, i logowanie posiadanym kontem ChatGPT. Nie kopiuje starych credentiali ani pamięci. Aktualizacja narzędzi nie zmienia SHA istniejącego pakietu. Osobny profil nie jest kontenerem ani dowodem izolacji: ograniczenia pozostają jawne, isolation_verified=false, znane wykluczone treści nadal blokują. Ustawienia systemowe pozostają nadrzędne. [Powód, użycie i oficjalne referencje](independent-review-command.md). Nowy profil nie resetuje limitu abonamentu.

**OBSERVATION J028 — testy polecenia, nie wynik review.** 20 nowych testów offline/CLI przeszło z rzeczywistym helperem o blob SHA 9f4700ae0b8d49da7cff0747894c3d55be7dd2d7. Wywołania Codexa i logowania były symulowane. Osobna próba na lokalnym repo Git potwierdziła rzeczywisty fast-forward i ponowne uruchomienie zaktualizowanego launchera, bez zmiany process SHA pakietu. [Raport i ograniczenia](../results/tooling-launcher-20260908/report.md). Nie wykonano prawdziwego logowania, sesji modelu, testu skuteczności sandboxa ani całej wcześniejszej suite. HYPOTHESIS: ograniczenie ręcznych kroków zmniejszy liczbę nieudanych startów; potrzebna kolejna rzeczywista próba na serwerze operatora.

## 2026-09-08 — od alternatywnego projektu do oceny dwóch propozycji

**OBSERVATION / CORRECTION J029 — pierwszy wynik to projekt, nie recenzja naszej propozycji.** Operator dostarczył wklejoną treść independent-design.md z próby phase0-independent-20260908T154456Z. Dokument proponuje minimalny pilot i zachowuje etykietę EXPLORATORY; INDEPENDENCE UNVERIFIED. W rozmowie zbyt swobodnie nazywaliśmy to „review naszego rozwiązania” i „zamkniętym audytem”. Autor miał brief, nie naszą propozycję. Nie odczytaliśmy oryginalnego RUN-RECORD.json z serwera; podsumowanie terminala nie zastępuje tego rekordu. Ślad źródłowy: załącznik użytkownika „Wklejony tekst.txt”, treść raportu po poleceniu cat independent-design.md. Surowego terminala i identyfikatora sesji nie publikujemy w repo.

**DECISION J030 — druga runda ocenia oba projekty bez narzucania wyniku.** Użytkownik zatwierdził przygotowanie i commit polecenia [design-review.py](../scripts/design-review.py). Nowy pakiet zawiera nasz proces z jednego commita oraz niezmienioną kopię wcześniejszego raportu, sprawdzoną lokalnie względem ukończonego rekordu. Recenzent ma rozstrzygnąć zachowaj / zmień / odłóż / odrzuć i zaproponować minimalny wiarygodny proces; nie zakładamy zwycięstwa jednego agenta ani rozbudowanej orkiestracji. Odrzucono powtarzanie independent design aż uzyskamy pożądany wynik. Comparative review pozostaje późniejszą rundą. G1 i migracja nie są zatwierdzone.

**DECISION / CORRECTION J031 — mniej ręcznych kroków, bez obchodzenia nieudanego sandboxa.** Drugie polecenie generuje run_id, pakiet i output_root oraz automatycznie podaje zapisany prompt po logowaniu w nowym profilu. Nie wymaga kopiowania instrukcji ani zgadywania folderu. Dostarczony raport ujawniał awarię bwrap i zatwierdzone wykonanie poza sandboxem oraz wewnętrznego subagenta. Drugi launcher żąda workspace-write z polityką never, zakazuje delegowania i nie ma fallbacku poza sandbox; to nie jest naprawa konfiguracji serwera ani dowód egzekwowania ustawień przez klienta. Nowa kopia wejść ma bity tylko do odczytu, lecz właściciel nadal może je zmienić. isolation_verified pozostaje false. Hasło: „Uprościć uruchomienie, nie osłabić dowód”. [Użycie i ograniczenia](design-review-command.md).

**OBSERVATION J032 — testy drugiego polecenia, nie wykonane drugie review.** 34 testy offline/CLI przeszły na Linux/Python 3.13.5. Testy użyły rzeczywistych wersji eksportera i helperów zgodnych z blobami repo; wywołania Codexa i logowania były jawnie symulowane. Test z lokalnym bare remote potwierdził fast-forward, ponowne uruchomienie i zachowanie starego raportu/pakietu. Zbadano brakujące/niezgodne hashe, odmowę restartu i nadpisania, niezmienność wejść, brak fikcyjnego COMPLETE oraz brak fallbacku sandboxa. [Wyniki i zakres](../results/tooling-design-review-20260908/report.md). Nie wykonano prawdziwego drugiego review, logowania, builda Buna ani całej wcześniejszej suite. Rzeczywisty rekord pierwszej próby sprawdzi dopiero polecenie na serwerze operatora.

## 2026-09-09 — zachowanie wyniku drugiej rundy

**DECISION J033 — wskazany wynik trafia do repo jako archiwum.** Użytkownik wskazał `phase0-design-review-20260909T140149029117Z-9adbe645` i potrzebę przeniesienia go zgodnie z zasadami projektu. Koordynator zachował 40 plików wejść/wyjść bez zmiany bajtów, oryginalne ścieżki i statusy oraz dodał manifest archiwizacji i [raport kontroli](../results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md). Oryginalny katalog pozostawiono na miejscu. Decyzja dotyczy zachowania dowodów, nie przyjęcia v0.2, G1, publikacji zdalnej ani kolejnego runu.

**OBSERVATION / CORRECTION J034 — FACT: oba raporty są dostępne i zgodne z rekordem; błąd launchera pozostaje jawny.** Zweryfikowano rzeczywisty rekord, manifest i 34 wejścia, hashe dwóch raportów, konfigurację i prompt; 29 plików procesu odpowiada blobom Git z `47764bace389f908e9e58473ded7ad07909dfe2b`. Rekord ma `status=COMPLETE`, werdykt `REVISE_PROCESS`, a równocześnie `launcher.status=LAUNCH_ERROR`, przy zapisanym wyjściu klienta 0. Bieżąca kontrola przechodzi; brak tracebacka pozostawia przyczynę UNKNOWN. Nie poprawiano historycznego rekordu ani nie ogłoszono sukcesu launchera. Zaktualizowano wcześniejsze instrukcje startu, które wskazywały drugie review jako dopiero oczekujące. Izolacja, faktyczny model i zużycie limitu pozostają niepotwierdzone. Hasło: „Zamknięty raport i poprawnie zamknięty launcher to dwa osobne fakty”.

**PROPOSAL J035 — kandydat v0.2 pochodzi od recenzenta, decyzje pozostają PENDING.** Raport proponuje połączenie kontroli judge'a z A, małego wycinka i rezerwy z B, jawnego właściciela baseline oraz checkpointów i interwencji. Ograniczenie G2 i domyślnego A/B wymaga decyzji Damiana; obecny proces obowiązuje. Rekomendacje zachowano w oryginalnym `process-proposal.md`, nie zastosowano ich do promptów/pipeline. Żadnej zmiany procesu nie przyjęto ani nie odrzucono za użytkownika. Następna runda według planu to osobny comparative review, następnie decyzja o wersji i budżecie na G1. Koszt tych etapów pozostaje UNKNOWN.

**OBSERVATION J036 — FACT: 92 lokalne testy narzędzi przeszły podczas archiwizacji.** `python3 -m unittest discover -s tests -v`: 92/92 OK, 7.794 s; [pełny zapis](../results/phase0-design-review-20260909T140149029117Z-9adbe645/test-output.txt). Kontrola publikacyjna wskazanego zestawu nie ujawniła credentiali; dwa adresy e-mail są syntetycznymi fixture'ami. Nie odczytywano prywatnych sesji/cache logowania. To weryfikacja koordynatora, nie testy wykonane przez recenzenta ani wynik Buna. Nie uruchomiono comparative review, migracji, płatnego API ani dodatkowych agentów; nie zatwierdzono bramek.

**DECISION J037 — commit i push archiwum oraz dokumentacji.** Po lokalnej archiwizacji użytkownik jawnie polecił „commit i push”. Zakres to katalog wyników `phase0-design-review-20260909T140149029117Z-9adbe645` oraz `README.md`, `START-HERE.md`, `results/README.md` i ten dziennik. Zgoda obejmuje publikację sprawdzonych artefaktów do repo; nie przyjmuje propozycji v0.2 ani nie zatwierdza G1. Historyczne raporty, hashe, LAUNCH_ERROR i etykieta niezweryfikowanej niezależności pozostają bez zmian. Wynik transportu wymaga zgodności SHA commita z odczytem zdalnej gałęzi; testy lokalne nie są wynikiem CI ani akceptacją procesu.

## 2026-09-09 — decyzje po omówieniu design review

**DECISION J038 — przyjmujemy kierunek uproszczenia, nie uruchamiamy pilota.** Po omówieniu drugiej rundy Damian polecił zapisać aktualne ustalenia w osobnym commicie; następnie poprosił o kontynuację. [Decyzje D01–D08](decisions/2026-09-09-pilot-v0.2.md) są podstawą następnego wdrożenia procesu: jeden testowalny wycinek, jedna główna sesja i jeden aktywny writer. Raport recenzenta pozostaje niezmienioną rekomendacją; nie przyjmujemy automatycznie wszystkich jego szczegółów. Dowód ustaleń: rozmowa z 2026-09-09 po odczycie archiwum w commicie 9e5fbb737451c3d0aeeaef9faa104c8af8dde58e. Nie wybrano konkretnego fragmentu Buna.

**CORRECTION J039 — liczba agentów i równoległość to różne osie.** W rozmowie różnicę uproszczono do „wiele agentów równolegle kontra jeden liniowo”. Wcześniejszy plan już zakładał jednego writera, a role nie wymagały osobnych modeli. Nowa decyzja zmniejsza domyślną liczbę sesji, przekazań pracy i zakres analizy przed pierwszym wynikiem. Zachowuje analizę, planowanie, review i odpowiedzialność operatora. Samoprzegląd nie jest niezależnym review; dodatkowy kompetentny przegląd może być potrzebny przy trudnej granicy. Odniesienie: [plan](experiment-plan.md), [role](../agents/roles.md) i omówienie w decyzjach D02/D07. Hasło: „Mniej przekazań pracy, nie mniej odpowiedzialności”.

**DECISION J040 — dowód musi być przygotowany i mieć własny budżet.** Przed portem ma działać oryginał i verifier, który odrzuca wybrane celowo błędne wyniki; kontrakt i kryteria są zamrożone. Operator odpowiada za gotowość baseline/judge, z pomocą modelu i narzędzi. Rezerwa obejmuje review, poprawki, retesty i zamknięcie. Ręczne zmiany są jawne, unieważniają dowody jako potwierdzenie nowego kandydata, ale nie kasują historii. Checkpoint przenosi stan, hashe i zużyty budżet. To wybór kierunku odpowiedzi na DR-01–DR-04, nie wykonane kontrole ani zatwierdzone wartości limitów. Kontrola mutacji była już mocną stroną A, nie brakującym elementem obu wariantów. Szczegóły: D03–D06 i zamrożony raport drugiej rundy.

**DECISION J041 — osobny commit decyzji, osobny commit wdrożenia.** Teraz dodajemy zapis ustaleń i uaktualniamy orientację w README/START-HERE. Nie zmieniamy jeszcze promptów, skryptów, szablonów, pipeline ani archiwów. Następne zadanie to spójna redakcja procesu v0.2 i przegląd zmian, bez uruchamiania migracji. Comparative review nie zostało zniesione, konkretna wersja i budżet nie otrzymały akceptacji G1; G1–G5 pozostają PENDING. Odrzucono traktowanie potwierdzenia kierunku jako zgody na każdy kolejny etap. J035 opisuje wcześniejszy stan przed decyzją; zachowujemy go jako historię, nie nadpisujemy.

**HYPOTHESIS J042 — uproszczenie ma zmniejszyć koszt uzyskania dowodu.** Nie zmierzyliśmy jeszcze przewagi jednej sesji nad wieloma. Mniej orkiestracji może przenieść więcej pracy na człowieka; dlatego mierzymy również jego uwagę i cały koszt weryfikacji. Hipotezę może podważyć trudna do oceny granica albo istotne błędy wykrywane przez dodatkowy przegląd przy akceptowalnym koszcie. Nie stawiamy tezy, że systemy wieloagentowe są ogólnie gorsze. Hasło do rozważenia: „Upraszczamy organizację, nie definicję poprawności”. To materiał narracyjny i plan pomiaru, nie wynik pilota.

## 2026-09-09 — przygotowanie spójnego procesu v0.2

**DECISION J043 — wykonanie zaakceptowanego planu w jednym commicie przygotowawczym.** Damian polecił „Implement the plan” po planie dostosowania istniejącego repo do D01–D08. Zakres obejmuje dokumenty, role, prompty, szablony, pipeline/pakiety i testy zgodności, bez nowego projektu ani recenzenta. Wprowadzono jedną główną sesję, kolejność odpowiedzialności i jeden wycinek; obowiązkowy review ma rodzaj i wykonawcę ustalone przed G3, bez domyślnego A/B. Dodatkowe kompetencje wynikają z ryzyka, a odbiór należy do Damiana. Upoważnienie obejmuje lokalny commit przygotowawczy, bez push i bez wykonania pilota.

**DECISION / CLARIFICATION J044 — gotowość dowodu przed portem i jawna kontynuacja.** Pipeline opisuje przygotowanie baseline/verifiera przed zamknięciem planu G3; operator jest właścicielem gotowości. Szablony zapisują wymagania kontroli negatywnych, hashe zamrożonego protokołu, budżet z rezerwą, interwencje i checkpoint. Limit dwóch rund zastąpiono wartością null do decyzji. Ręczna zmiana kandydata wymaga nowego review/parity, zmiana protokołu nowej wersji i decyzji; kontynuacja zachowuje wcześniejsze dowody i zużycie. Pipeline nadal nie jest runnerem: pole statusu i test struktury nie egzekwują bramki operacyjnej. Format manifestu eksportera, CLI i profile launchera pozostają bez zmian; generyczne kopiowanie nowych pól rekordu sprawdzono testami.

**CORRECTION J045 — jedna sesja pilota nie znosi odrębnych rund metody.** Independent-design zachowuje neutralny brief. Nowe pakiety oceniające proces obejmują D01–D08 jako jawne ograniczenia; osobny pakiet ślepego Architekta jest opcją, nie domyślnym etapem. Comparative review nadal wymaga odrębnego przygotowania, wskazania raportów/propozycji i hashy przed G1. Eksport konfiguracji w teście nie jest kompletną rundą porównawczą. Historyczny zapis decyzji zachowano z oznaczoną aktualizacją wykonania; odnośniki do v0.1 kierują do zamrożonych plików. Wpisy J038–J042 opisują stan przed tym przygotowaniem.

**OBSERVATION J046 — FACT: 104 lokalne testy narzędzi przeszły.** `python3 -m unittest discover -s tests -v`: 104/104 OK, czas suite 8.141 s. Dodano 12 testów: kontrakty konfiguracji, rzeczywiste aktualne szablony i eksport na tymczasowym lokalnym repo Git oraz zachowanie nowych pól przez oba helpery przygotowania. Najpierw testy kontraktu ujawniły brak v0.2, wymaganych pól i zależności w bazie. Końcowa suite używa rzeczywistych lokalnych operacji plików/Git i jawnie symulowanych wywołań klienta. Nie uruchomiono modelu, logowania, Buna ani migracji. [Raport, log i mapowanie D01–D08](../results/tooling-process-v02-20260909T174417Z/report.md).

**OBSERVATION J047 — FACT: wcześniejsze dowody są zachowane.** Sprawdzono 40 plików archiwizacji i 34 wejścia drugiej rundy według ich manifestów. Wszystkie 87 wcześniej śledzonych plików w results/, sources/ i upstream/ odpowiadają blobom z `b1ba7a9f946cd0de6c1c79869faeaa110ac96782`. COMPLETE, LAUNCH_ERROR i ograniczenia niezależności zachowano. Przegląd zmian przygotowawczych jest samoprzeglądem tej sesji; akceptacja Damiana i G1–G5 pozostają PENDING. Nie wykonano comparative review, wyboru wycinka, baseline/verifiera Buna, praktycznej próby wznowienia pilota ani pomiaru jego kosztu. Nadal otwarte są środowisko, wycinek, model/ustawienia, budżet/rezerwa i konkretny plan review. Hipoteza J042 pozostaje niezmierzona.
