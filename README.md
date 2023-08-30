# Projekt_3_Election_scraper
Program Election scraper má za úkol získat vybraná data o výsledcích voleb 2017 (odkaz: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
z vybraného uzemního celku a uložit ho do libovolně pojmenovaného souboru CSV 
soubor CSV bude obsahovat: čislo obce, název obce, voliči v seznamu, vydané obálky,platné hlasy, kadidující strany(vč. počtu hlasů) 

# Průběh programu
Nejprve je nutné zadat správně dva argumenty první je url pozadovaného územního celku a druhý je název vystupního souboru csv,
jestliže uživatel nezadá dva správné argumenty program jej upozorní na chybu.

# Ukázka spuštění programu

Ukázka je na odkaz vysledků voleb v okrese Blansko
1. argument url adresa: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201
2. argument výstupní soubor CSV: vysleky_blansko.csv

pro spuštění programu je nutné vypsat do příkazové řádky:   
python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201" "vysledky_blansko.csv"   
Na základě takto správně zadaného příkazu program začne stahovat vybraná data a pote jej uloží do požadovaného souboru. 

# Ukázka výstupu programu:

![image](https://github.com/fojtZdenek/Projekt_3_Election_scraper/assets/138121824/4368d805-2eb5-41f2-b83f-5eb12b23c6d5)


![image](https://github.com/fojtZdenek/Projekt_3_Election_scraper/assets/138121824/51105ba6-0091-48b3-b965-e10057fe5e88)








