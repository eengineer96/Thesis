**Tesztelő:** Póta László

**Tesztelés dátuma:** 2025. 03. 18.

**Talált hibák száma:** 2

Tesztszám | Funkció | Teszt leírása | Eredmény 
----------|--------------|---------------|----------
FT-01 | Grafikus felület inicializálása | Alkalmazás indításakor a GUI ellenőrzése, hogy megfelelően betöltődik | ✅ - Az alkalmazás hiánytalanul betöltődik
FT-02 | Kamerakép inicializálása | Alkalmazás indításakor a kamerakép frissítésének ellenőrzése | ✅ - A kamera stream elindul, folyamatos
FT-03 | Grafikus felület elemei | Gombok, csúszkák ellenőrzése a GUI-n | ✅ - A GUI vezérlők hibátlanul működnek, reszponzívak 
FT-04 | Képkiértékelés ellenőrzése | Megvizsgálni, hogy megtörténik-e és frissül-e a kiértékelés eredménye | ✅ - A beállított időn belül megtörténik a képkiértékelés, frissítés
FT-05 | NOK kiértékelés értesítés küldése | Rossz nyomtatás szimulálása, hogy értesítést generáljon | ✅ - Az értesítés elküldésre kerül Telegramon
FT-06 | NOK kiértékelés ismételt értesítés | NOK kiértékelés fenntartása, hogy ne küldjön újra értesítést | ✅ - Kizárólag a beállított idő letelte után jött új értesítés
FT-07 | Nyomtató leállítása automata | Hosszasan fennálló NOK kiértékelés során, automata módban ellenőrizni, hogy a nyomtató részére elküldésre kerül a stop parancs | ✅ - A beállított tolerancia és kitartás értékek felett a nyomtató megkapta a stop parancsot
FT-08 | Nyomtató leállítása manuális  | Hosszasan fennálló NOK kiértékelés során, manuális módban ellenőrizni, hogy a nyomtató részére **nem** kerül elküldésre a stop parancs | ✅ - Manuális módban nem áll meg a nyomtató
FT-09 | Telegram parancs - Üzemmódváltó | Telegram automata parancs tesztelése | ✅ - A parancs elküldése után a változó értéke beállítása és a GUI-n is visszajelzésre kerül
FT-10 | Telegram parancs - Üzemmódváltó | Telegram manuális parancs tesztelése | ✅ - A parancs elküldése után a változó értéke beállítása és a GUI-n is visszajelzésre kerül
FT-11 | Telegram parancs - Leállítás | Telegramon a leállítás parancs tesztelése | ✅ - A parancs elküldése után a nyomtató leállítása kerül <br>*Megjegyzés: Kizárólag manuális üzemmódban*
FT-12 | Telegram parancs - Szünet | Telegramon a szünet parancs tesztelése | ✅ - A parancs elküldése után a nyomtatás szünetel <br>*Fejlesztési lehetőség: Folytatás parancs lefejlesztése*
FT-13 | Telegram parancs - Státusz | Telegramon a státusz parancs tesztelése | ✅ - A Telegramon megérkezik a válasz a kameraképpel és a paraméterekkel
FT-14 | Telegram parancsok spamelése | Több Telegram parancs elküldése rövid időn belül | ⚠️ - Nem minden parancsra érkezik válasz
FT-15 | Telegram ismeretlen parancs | Telegramon ismeretlen parancs vagy üzenet küldése | ✅ - Ismeretlen parancsokra és üzenetekre nem történik akció
FT-16 | Telegram ismeretlen által küldött parancs | Telegramon 3. fél által küldött üzenet a bot részére | ✅ - Illetéktelen nem tudja használni a bot-ot
FT-18 | Rendszer stabilitás | Hosszú (10+ óra) nyomtatás esetén túlemelegdés, instabilitás vizsgálata | ✅ - A rendszer folyamatosan működött, hiba nélkül
FT-19 | Hálózatkiesés szimulálása | Hálózat lekapcsolása esetén rendszer helyreállás ellenőrzése | ✅ - A rendszer automatikusan helyrell hálózatkiesés után
FT-20 | Áramkimaradás szimulálása | Tápfeszültség együttes lekapcsolása esetén rendszer helyreállás ellenőrzése | ❌ - A rendszer nem képes önállóan felállni hiba esetén
FT-21 | Kamera leválasztása  | Értékelés közben a kamera leválasztása a Raspberry-ről | ❌ - A program kivételt dob, nem képes önállóan felállni újracsatalkoztatás után <br>*Fejlesztési lehetőség: Kivételkezelés és kamera újrainicializálása kiesés esetén*
