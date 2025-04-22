import webbrowser
from threading import Timer
from flask import Flask, render_template
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

with open("adatok.txt", "r") as f:
    lista=f.readlines()
    usern=lista[0]
    passwrd=lista[1]

class Kurzus:
    def __init__(self):
        self.targynev=""
        self.targykod=""
        self.nap=""
        self.kezdet=""
        self.vege=""
        self.terem=""
        self.tipus=""
    def __str__(self):
        #ki=self.targynev + " " + self.targykod + " " + self.nap + " : " + self.kezdet + "-" + self.vege + " " + self.terem + " " + self.tipus
        ki=self.targynev + " (" + self.tipus + ")<br>" + self.terem[0:-1]
        return ki

_kurzusok=[]

def magic():
    global usern
    global passwrd

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://neptun.szte.hu/hallgato/exams/registration"
        driver.get(url)
        time.sleep(4.0)

        username_input = driver.find_element(By.CSS_SELECTOR, "input[name=userName]")
        print(username_input.get_attribute("outerHTML"))
        time.sleep(0.1)
        username = usern
        username_input.send_keys(username)
        time.sleep(0.1)

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
        print(password_input.get_attribute("outerHTML"))
        time.sleep(0.1)
        password = passwrd
        password_input.send_keys(password)
        time.sleep(0.1)

        button = driver.find_element(By.CSS_SELECTOR, "button[id=login-button]")
        print(button.get_attribute("outerHTML"))
        time.sleep(0.1)
        button.click()
        time.sleep(1)

        menugomb=driver.find_element(By.CSS_SELECTOR, "button[id=menu-btn]")
        print(menugomb.get_attribute("outerHTML"))
        menugomb.click()
        time.sleep(0.5)

        targyakgomb=driver.find_element(By.CSS_SELECTOR, "button[id=Subjects]")
        print(targyakgomb.get_attribute("outerHTML"))
        targyakgomb.click()
        time.sleep(0.2)

        felvett_kurzusok=driver.find_element(By.CSS_SELECTOR, "a[id=RegisteredCourses]")
        #print(felvett_kurzusok.get_attribute("outerHTML"))
        felvett_kurzusok.click()
        time.sleep(0.5)

        alap=driver.find_element(By.CSS_SELECTOR, "div[class='neptun-wrapper ng-star-inserted']")
        #print(alap.get_attribute("outerHTML"))
        time.sleep(0.2)
#ciklus
        kurzusok=alap.find_elements(By.CSS_SELECTOR, "neptun-data-table")
        #print(kurzusok[0].get_attribute("outerHTML"))
        time.sleep(0.5)
        hossz=len(kurzusok)

        i=0
        while i < hossz:
            alap = driver.find_element(By.CSS_SELECTOR, "div[class='neptun-wrapper ng-star-inserted']")
            #print(alap.get_attribute("outerHTML"))
            #time.sleep(0.1)

            kurzusok = alap.find_elements(By.CSS_SELECTOR, "neptun-data-table")
            # print(kurzusok[0].get_attribute("outerHTML"))
            #time.sleep(0.1)

            reszletek_gomb=kurzusok[i].find_element(By.CSS_SELECTOR, "button[id=data-table-element_action-icon-btn-0-0]")
            reszletek_gomb.click()
            time.sleep(0.5)

            neptun_data_view=driver.find_element(By.CSS_SELECTOR, "neptun-data-view")
            #print(neptun_data_view.get_attribute("outerHTML"))
            #time.sleep(0.1)

            print()
            dl=neptun_data_view.find_element(By.CSS_SELECTOR, "dl")
            #time.sleep(0.1)

            divek=dl.find_elements(By.XPATH, "./*")
            #print(divek[0].get_attribute("outerHTML"))
            #time.sleep(0.1)

            adatok=[]
            for div in divek:
                lenyeg=div.find_element(By.CSS_SELECTOR, "dd")
                print(lenyeg.get_attribute("innerHTML"))
                adatok.append(lenyeg.get_attribute("innerHTML"))
            _kurzus=Kurzus()
            _kurzus.targynev=adatok[0]
            _kurzus.targykod=adatok[1]
            _kurzus.tipus=adatok[2]
            #SZE:16:00-18:00(TIK-A001-0 - TIK Alagsor I-II. Előadó (TIK-A001-0))
            #adatok[5]
            pattern=r"(\w+):(\d{1,2}):(\d{1,2})-(\d{1,2}):(\d{1,2})(.+)"
            eltarolt=re.search(pattern,adatok[5])
            if eltarolt:
                _kurzus.nap=eltarolt.group(1)
                _kurzus.kezdet=eltarolt.group(2) + ":" + eltarolt.group(3)
                _kurzus.vege=eltarolt.group(4) + ":" + eltarolt.group(5)
                _kurzus.terem=eltarolt.group(6).split(" - ")[1]
            else:
                _kurzus.nap = "nincs"
                _kurzus.kezdet = "nincs"
                _kurzus.vege = "nincs"
                _kurzus.terem = "nincs"
            #print(kurzus.__str__())
            _kurzusok.append(_kurzus)


            vissza_gomb=driver.find_element(By.CSS_SELECTOR, "button[id=breadcrumb__btn-1]")
            vissza_gomb.click()
            i+=1
            sleep(0.5)
            print("-----------------------------------------------------------------------")


    except Exception as e:
        print(f"Hiba történt: {e}")
    finally:
        driver.quit()


magic()
for _kurzus in _kurzusok:
    print(_kurzus.__str__())

def atalakit(nap):
    if nap=="Hétfő":
        return "H"
    if nap=="Kedd":
        return "K"
    if nap=="Szerda":
        return "SZE"
    if nap=="Csütörtök":
        return "CS"
    if nap=="Péntek":
        return "P"
    return "hiba"


class Ora:
    def __init__(self):
        self.kurzusok=[]
        self.kezdet="00:00"
        self.vege="01:00"
        self.nap="SZO"
        self.felirat=""
    def kurzust_keres(self):
        global _kurzusok
        for _kurzus in _kurzusok:
            if _kurzus.nap == self.nap and _kurzus.kezdet <= self.kezdet and _kurzus.vege > self.kezdet:
                self.kurzusok.append(_kurzus)
    def __str__(self):
        if len(self.kurzusok)>0:
            #return self.kurzusok[0].__str__()
            #return len(self.kurzusok).__str__() + "   "
            ki=""
            for _kurzus in self.kurzusok:
                ki+=_kurzus.__str__() + "<br><br>"
            return ki
        else:
            #return "nincs óra"
            return ""


class Orarend:
    def __init__(self):
        self.tabla=[]
        for i in range(0,14):
            sor=[]
            self.tabla.append(sor)
            for j in range(0,6):
                sor.append(Ora())
        self.tabla[0][1].felirat="Hétfő"
        self.tabla[0][2].felirat = "Kedd"
        self.tabla[0][3].felirat  = "Szerda"
        self.tabla[0][4].felirat  = "Csütörtök"
        self.tabla[0][5].felirat  = "Péntek"

        self.tabla[1][0].felirat  = "08:00"
        self.tabla[2][0].felirat  = "09:00"
        self.tabla[3][0].felirat  = "10:00"
        self.tabla[4][0].felirat  = "11:00"
        self.tabla[5][0].felirat  = "12:00"
        self.tabla[6][0].felirat = "13:00"
        self.tabla[7][0].felirat = "14:00"
        self.tabla[8][0].felirat = "15:00"
        self.tabla[9][0].felirat = "16:00"
        self.tabla[10][0].felirat = "17:00"
        self.tabla[11][0].felirat = "18:00"
        self.tabla[12][0].felirat = "19:00"
        self.tabla[13][0].felirat = "20:00"

    def tablazatot_letrehoz(self):
        for i in range(1, 14):
            for j in range(1, 6):
                ora = Ora()
                ora.nap=atalakit(self.tabla[0][j].felirat)
                ora.kezdet=self.tabla[i][0].felirat
                self.tabla[i][j] = ora
        for i in range(1, 14):
            for j in range(1, 6):
                self.tabla[i][j].kurzust_keres()
        for i in range(0, 14):
            print()
            for j in range(0, 6):
                if i==0 or j==0:
                    print(self.tabla[i][j].felirat + " ", end="")
                else:
                    print("[" + self.tabla[i][j].__str__() + "]", end="")

    def tablazat_html(self):
        ki_tabla=[]
        for i in range(0,14):
            sor=[]
            ki_tabla.append(sor)
            for j in range(0,6):
                sor.append("")
        for i in range(0, 14):
            for j in range(0, 6):
                if i == 0 or j == 0:
                    ki_tabla[i][j]=self.tabla[i][j].felirat + " "
                else:
                    ki_tabla[i][j]=self.tabla[i][j].__str__()
        return ki_tabla


orarend=Orarend()
orarend.tablazatot_letrehoz()
tabla=orarend.tablazat_html()
print()
for i in range(0,14):
    print()
    for j in range(0, 6):
        print(tabla[i][j], end="")


app = Flask(__name__)
@app.route("/")
def orarend():
    global tabla
    return render_template("index.html", tabla=tabla)
if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(debug=False)















