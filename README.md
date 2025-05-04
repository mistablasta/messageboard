# messageboard

### Sovelluksen toiminnot

* Käyttäjä pystyy luomaan oman tunnuksen ja kirjautua sisään. ✅
* Käyttäjä pystyy julkaista omia viestejä, joita voi luokitella kategorioihin ✅
* Käyttäjä voi selata muiden viestejä, sekä hakea niitä ✅
* Käyttäjä voi muokata ja poistaa omia viestejä ✅
* Käyttäjä voi reagoida muiden viesteihin. ✅
* Käyttäjä voi selata muiden profiileja, joissa näkyy käyttäjän tilastoja ja kaikki käyttäjän viestit. ✅
* Sovelluksessa on paikattu CSRF ja XSS aukot. ✅



### Asentaminen
Varmista, että sinulla on `flask`-kirjasto, jonka jälkeen luot tietokantaan taulut komennolla

```
$ sqlite3 database.db < schema.sql
```

Ohjelman voit käynnisää komennolla

```
flask run
```


# Suuri tietomäärä
* init.sql lisää sovellukseen miljoona käyttäjää, reaktiota sekä viestiä kategorioilla.
* Vaikka sovellus käyttää sivutusta, indexejä, niin tulos on aika hidas. Reaktion lisääminen, seuraavan sivun avaaminen tai viestin lähettäminen kestää yli 5 sekuntia.
```
127.0.0.1 - - [04/May/2025 23:28:15] "POST /reaction/3/thumbs_down HTTP/1.1" 302 -
elapsed time: 5.94 s
127.0.0.1 - - [04/May/2025 23:28:21] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 5.83 s
127.0.0.1 - - [04/May/2025 23:28:48] "POST /messages HTTP/1.1" 302 -
elapsed time: 6.13 s
```
Jos haluat itse kokeilla testidataa, suorita komento.
```
$ sqlite3 database.db < init.sql
```

