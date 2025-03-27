```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Monopolipeli "1" -- "1" Vankila
    Monopolipeli "1" -- "1" Aloitusruutu
    Ruutu "1" -- "1" Vankila
    Ruutu "1" -- "1" Aloitusruutu
    Ruutu "8" -- "1" Sattuma ja yhteismaa
    Kortti "40" -- "1" Sattuma ja yhteismaa
    Asemat ja laitokset "8" -- "1" Ruutu
    Normaalit kadut "25" -- "1" Ruutu
    Toiminto "1" -- "1" Ruutu
    Normaalit kadut "1..25" -- "1" Pelaaja
    Raha "1..1000" -- "1" Pelaaja
```