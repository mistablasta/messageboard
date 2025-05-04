# messageboard

### Sovelluksen toiminnot

* Käyttäjä pystyy luomaan oman tunnuksen ja kirjautua sisään. ✅
* Käyttäjä pystyy julkaista omia viestejä, joita voi luokitella kategorioihin ✅
* Käyttäjä voi selata muiden viestejä, sekä hakea niitä ✅
* Käyttäjä voi muokata ja poistaa omia viestejä ✅
* Käyttäjä voi reagoida muiden viesteihin. ✅
* Käyttäjä voi selata muiden profiileja, joissa näkyy käyttäjän tilastoja ja kaikki käyttäjän viestit. ✅

### TODO:
* Optimisointi suurelle tietomäärälle. ❌
* Vahvistusviesti ennen viestin poistoa. ❌
* Käyttäjäkokemuksen parantaminen (näppäiden asettelu, ulkoasu yms.) ❌ 
* Kyberturvallisuus. ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌

### Asentaminen
Varmista, että sinulla on `flask`-kirjasto, jonka jälkeen luot tietokantaan taulut komennolla

```
$ sqlite3 database.db < schema.sql
```

Ohjelman voit käynnisää komennolla

```
flask run
```