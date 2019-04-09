# Sieci projekt 1 - kalkulator podsieci

### Cel zadania: stworzenie kalkulatora podsieci

## Opis działania skryptu:


1. Skrypt przyjmuje jako argument adres IP (hosta lub sieci) wraz z maską w formacie:
a.b.c.d/maska

2. Jeśli argument nie został podany to skrypt pobiera adres komputera, na którym jest
uruchomiony

3. Skrypt sprawdza, czy wprowadzony adres jest poprawnym adresem IP. Jeśli nie,
wyświetla komunikat o błędzie.

4. Skrypt oblicza następujące dane:
    * Adres sieci
    * Klasę sieci
    * Czy adres należy do puli adresów publicznych czy prywatnych
    * Maska sieci w formacie dziesiętnym (np. 255.255.255.0) i binarnym
    * Adres broadcast (dziesiętnie i binarnie)
    * Pierwszy adres hosta (dziesiętnie i binarnie)
    * Ostatni adres hosta (dziesiętnie i binarnie)
    * Maksymalna ilość hostów, która może być przypisana do danej podsieci
5. Obliczone wartości są wyświetlane na ekranie oraz zapisywane do pliku tekstowego
6. Adresy w systemie dwójkowym są prezentowane tak, aby każdy oktet był
przedstawiony przy pomocy 8 znaków.
7. Jeżeli podany adres jest adresem hosta to skrypt pyta, czy wykonać polecenie ping
dla podanego adresu. Jeśli użytkownik wpisze Y to skrypt wykonuje polecenie ping
oraz prezentuje jego wyniki.
