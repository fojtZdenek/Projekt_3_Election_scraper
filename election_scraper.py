# potřebné knihovny + knihovny třetích stran instalovaných přes
# pip install requests a pip install bs4
import requests
from bs4 import BeautifulSoup
import sys
import csv

#funkce získá čísla obci ze zadaného odkazu
def scrapuj_cisla_obci(zdroj):
    seznam_cisel_obci = []
    for cisla in zdroj.find_all('td', {'class': 'cislo'}):
        for cislo in cisla.find_all('a'):
            seznam_cisel_obci.append(cislo.text)
    return seznam_cisel_obci

#funkce získá názvy obcí ze zadaného odkazu v argumentu
def  scrapuj_nazev_obci(zdroj):
    seznam_obci = []
    for obec in zdroj.find_all('td', {'class': 'overflow_name'}):
        seznam_obci.append(obec.text)
    return seznam_obci

# funkce získá odkazy jednotlivých obcí
def scrapuj_odkaz_obci(zdroj):
    odkazy_html = []
    for cislo in zdroj.find_all('td', {'class': 'cislo'}):
        for a in cislo.find_all('a'):
            odkazy_html.append("https://volby.cz/pls/ps2017nss/" + a['href'])
    return odkazy_html

# funkce získá data jednotlivých obcí a uloží je do dvou seznamů
def scrapuj_obce(url):
    seznam_data = []
    seznam_hl_stran = []
    for udaj in url:
        obec_response = requests.get(udaj)
        zdroj_2 = BeautifulSoup(obec_response.text, "html.parser")
        seznam_data.append(scrapuj_data_obci(zdroj_2))
        seznam_hl_stran.append(scrapuj_hlasy_stran_obce(zdroj_2))
    return seznam_data, seznam_hl_stran

#funkce získá data obcí seznam voličů, vydané obálky, platné hlasy
def scrapuj_data_obci(zdroj_2):
    seznam_volicu = zdroj_2.find('td', {'headers': 'sa2'}).text
    vydane_obalky = zdroj_2.find('td', {'headers': 'sa3'}).text
    platne_hlasy = zdroj_2.find('td', {'headers': 'sa6'}).text

    return seznam_volicu, vydane_obalky, platne_hlasy

#funkce získá hlasy jednotlivých stran
def scrapuj_hlasy_stran_obce(zdroj_2):
    seznam_hl_stran = []

    hlasy_1 = zdroj_2.find_all('td', {'headers': 't1sa2 t1sb3'})
    hlasy_2 = zdroj_2.find_all('td', {'headers': 't2sa2 t2sb3'})
    for hlasy in hlasy_1:
        seznam_hl_stran.append(hlasy.text)
    for hlasy in hlasy_2:
        seznam_hl_stran.append(hlasy.text)

    return seznam_hl_stran

#funkce získá seznam jednotlivých stran 
def scrapuj_kand_strany():
    strany_req = requests.get("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=11&xnumnuts=6201")
    zdroj_strany = BeautifulSoup(strany_req.text, "html.parser")
    seznam_stran = []
    for strany in zdroj_strany.find_all('td', {'class': 'overflow_name'}):
        seznam_stran.append(strany.text)

    return seznam_stran

#funkce kontroluje správnost vstupních údajů
#v případě chybného zadání upozorní uživatele
def zkontroluj_vst_udaje():
    if len(sys.argv) != 3:
        print("Zadejte dva argumety")
        quit()
    if "https://volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("Špatně zadaný URL argument")
        quit()
    if ".csv" not in sys.argv[2]:
        print("Špatně zadaný CSV soubor")
        quit()
    else:
        return True
# hlavní funkce která vypíše získaná data ze zadaného odkazu
# v případě správného zadání dvou argumentů vytvoří CSV soubor se získanými daty.
def main():
    zkontroluj_vst_udaje()
    uzemni_celek = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    
    request = requests.get(uzemni_celek)
    zdroj = BeautifulSoup(request.text, 'html.parser')
    print(f"Stahuji data z vybrané URL adresy .... Vyčkejte prosím")

    hlavicka = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    for strana in scrapuj_kand_strany():
        hlavicka.append(strana)

    with open(vystupni_soubor, "w", newline="", encoding="utf-8") as file:
        file_write = csv.writer(file)
        file_write.writerow(hlavicka)

        cislo = scrapuj_cisla_obci(zdroj)
        nazev = scrapuj_nazev_obci(zdroj)
        volici_v_seznamu = scrapuj_obce(scrapuj_odkaz_obci(zdroj))[0]
        vydane_obalky = scrapuj_obce(scrapuj_odkaz_obci(zdroj))[0]
        platne_hlasy = scrapuj_obce(scrapuj_odkaz_obci(zdroj))[0]
        obce = scrapuj_obce(scrapuj_odkaz_obci(zdroj))[1]
        i = 0
        for radek in range(len(scrapuj_odkaz_obci(zdroj))):
            v_radek = []
            v_radek.append(cislo[radek])
            v_radek.append(nazev[radek])
            v_radek.append(volici_v_seznamu[radek][0])
            v_radek.append(vydane_obalky[radek][1])
            v_radek.append(platne_hlasy[radek][2])
            v_radek.extend(obce[radek])
            file_write.writerow(v_radek)

    print(f"Vaše data ukládám do souboru {vystupni_soubor}")
    print("Hotovo, data byla stažena a uložena do souboru CSV..., Ukončuji program...!")

if __name__ == "__main__":
    main()   