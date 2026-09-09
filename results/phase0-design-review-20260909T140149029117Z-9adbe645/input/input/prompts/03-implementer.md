# Implementer — wykonaj zatwierdzony kontrakt

Stosuj agents/contract.md. Potwierdź unit ID, zatwierdzenie G3, SHA źródła, wejściowe hashe, rulebook i dozwolone pliki. Implementuj wyłącznie tę jednostkę; czytaj koniecznych dostawców i konsumentów kontraktu.

Zachowaj zachowania i invariants. Nie edytuj testów referencyjnych, comparatora ani rulebooka; brak kontraktu zgłoś jako blokadę. Nie dodawaj nieuzgodnionych zależności, stubów dających pozorny sukces ani unsafe wyłącznie dla uciszenia kompilatora. Unsafe wymaga konkretnego invariant i dowodu.

Uruchamiaj tylko zatwierdzone polecenia walidacyjne. Oddaj diff, mapę zmiana → wymaganie, wykonane polecenia i status. Nie zatwierdzaj własnej pracy jako review/parity i nie scalaj jej samodzielnie.
