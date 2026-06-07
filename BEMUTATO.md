# 3 perces bemutató forgatókönyv

## 0:00-0:35 - Probléma és architektúra

„A projektem egy kiskereskedelmi vállalat integrált adatplatformját szimulálja.
A cél, hogy az üzletekből érkező rendelési adatokat automatikusan feldolgozzuk,
eltároljuk, vizualizáljuk, és az adatmérnökök számára elemezhetővé tegyük.
A rendszer négy Docker szolgáltatásból áll: Python ETL, PostgreSQL, Grafana és
JupyterLab. Ezek egy belső Docker hálózaton kommunikálnak.”

Mutasd meg a README architektúra-ábráját.

## 0:35-1:20 - Indítás és komponensek

Futtasd:

```bash
docker compose up --build -d
docker compose ps
```

„A teljes rendszer egyetlen Compose paranccsal indul. A PostgreSQL healthcheck
biztosítja, hogy az adatbázist használó komponensek csak akkor induljanak el, amikor
az adatbázis már készen áll. Az ETL első alkalommal historikus adatokat tölt be,
majd tíz másodpercenként új rendeléseket generál. Az adatokat volume őrzi meg.”

Futtasd:

```bash
docker compose logs --tail=5 etl
```

## 1:20-2:05 - Grafana és Jupyter demó

Nyisd meg a Grafanát: `http://<EC2_PUBLIC_IP>:3000/d/retail-overview`

„A Grafana adatforrása és dashboardja provisioning segítségével automatikusan
létrejött. Látható az elmúlt 24 óra bevétele, rendelésszáma, régiós és
termékteljesítménye. A dashboard tíz másodpercenként frissül.”

Nyisd meg a Jupytert: `http://<EC2_PUBLIC_IP>:8888`

„A Jupyter ugyanahhoz a PostgreSQL adatbázishoz kapcsolódik. Az előkészített
notebook SQL-lekérdezést futtat, Pandas segítségével aggregál, majd diagramot készít.
Ez mutatja, hogy ugyanaz az adattár több fogyasztót is kiszolgál.”

## 2:05-2:40 - Megvalósítás és nehéz rész

„Először az üzleti adatmodellt és az integrációs kapcsolatokat terveztem meg. Ezután
létrehoztam az adatbázis inicializáló SQL-jét, az ETL saját Docker image-ét, végül
a Grafana provisioning fájlokat és a Jupyter notebookot. A legnehezebb rész az
indulási sorrend és az automatikus konfiguráció volt. Ezt healthcheckkel,
depends_on feltételekkel és verziókezelt provisioning fájlokkal oldottam meg.”

## 2:40-3:00 - Tanulság és bővítés

„A projekt megmutatja, hogy a konténerizáció reprodukálhatóvá tesz egy többkomponensű
adatplatformot. Következő lépésként Kafka eseményfolyamot, Airflow orchestrációt,
S3 data lake-et és dbt adatminőségi teszteket adnék hozzá. Éles környezetben a
jelszavakat Secrets Managerben tárolnám és minden felületet hitelesítéssel védenék.”

## Felvétel előtti ellenőrzőlista

1. Indítsd el a rendszert legalább két perccel a felvétel előtt.
2. Ellenőrizd a `docker compose ps` kimenetét.
3. Nyisd meg előre a README-t, a Grafana dashboardot és a Jupyter notebookot.
4. A notebook celláit futtasd le egyszer a felvétel előtt.
5. A felvétel után állítsd le az EC2 példányt a költségek elkerüléséhez.
