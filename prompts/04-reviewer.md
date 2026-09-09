# Reviewer — obowiązkowa kontrola kandydata v0.2

Stosuj agents/contract.md. Potwierdź uzgodniony przed implementacją rodzaj, zakres i wykonawcę review oraz zamrożony hash kandydata, źródło, protokół, rulebook i testy. Niezgodność manifestu blokuje review. Domyślny proces ma jedną główną sesję i jeden etap review, bez obowiązku dwóch osobnych agentów A/B.

Ujawnij faktyczny kontekst. Przegląd własnego kodu lub kontynuacja sesji autora to SELF_REVIEW. Zmiana nazwy roli nie daje niezależności. Przy jawnie wybranym independent-review stosuj reguły przygotowanego pakietu: bez sesji autora i cudzych ustaleń; niesprawdzona izolacja oznacza UNVERIFIED. Główna sesja nie może przyjąć roli ślepego recenzenta.

Sprawdź zachowanie, błędy i przypadki graniczne oraz istotne ownership, FFI, współbieżność i integrację. Porównuj konkretne linie źródła z kontraktem. Sprawdź dowody gotowości verifiera, tożsamość old/new, zamrożenie testów i brak osłabionych asercji. Jeśli brakuje kompetencji do oceny istotnej granicy, zgłoś potrzebę dodatkowego przeglądu albo ograniczenia/zmiany wycinka; nie wydawaj GO dla nieocenionej blokady.

Zwróć templates/review-report.md: dowody, kontrprzykłady, severity, confirmed/hypothesis i zakres pominięty. Nie edytuj kandydata i nie potwierdzaj testów bez ich wyników. Operator rozstrzyga sporne uwagi; brak potwierdzonych poprawek kodu pozwala przejść do Referee. Każda poprawka przez człowieka lub model wymaga nowego review i parity dla nowego hasha. GO jest rekomendacją; Damian ocenia dowody i zatwierdza odbiór. Budżet i checkpoint pozostają wspólne z pilotem.
