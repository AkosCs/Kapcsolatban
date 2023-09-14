import psycopg2 as psql

#A kapcsolathoz egy "iskolarendszer" nevű adatbázist hoztam létre PostgreSQL-ben.

kapcsolat = psql.connect(host="localhost",dbname="iskolarendszer",user="csako",password="password", port=5432)

cur = kapcsolat.cursor()

"""
A "DROP TABLE..." csak azért van ott, hogy ne legyen hiba többszöri futtatás esetén. Utána a program létrehozza
a táblákat ("tantargy", "eredmeny", "tanulok").
"""


cur.execute("""
DROP TABLE IF EXISTS tanulok, tantargy, eredmeny; 

CREATE TABLE tantargy (
id INT PRIMARY KEY NOT NULL,
targynev VARCHAR(50) NOT NULL
);

CREATE TABLE eredmeny (
id INT PRIMARY KEY NOT NULL,
erdemjegy VARCHAR(50) NOT NULL

);

CREATE TABLE tanulok (
id BIGSERIAL PRIMARY KEY NOT NULL,
vezeteknev VARCHAR(50) NOT NULL,
keresztnev VARCHAR(50) NOT NULL,
nem CHAR NOT NULL,
szuletesi_ev DATE NOT NULL,
targy_id INT REFERENCES tantargy(id),
jegy INT REFERENCES eredmeny(id)
);

""")

# Majd feltöltöm értékekkel a táblákat.

cur.execute("""
INSERT INTO tantargy (id, targynev) VALUES (1, 'Gasztronómia'), (2, 'Idegen nyelv'), (3, 'TV-nézés');
INSERT INTO eredmeny (id, erdemjegy) VALUES (1, 'elégtelen'), (2, 'elégséges'), (3, 'közepes'), (4, 'jó'), (5, 'jeles');
INSERT INTO tanulok (vezeteknev, keresztnev, nem, szuletesi_ev, targy_id, jegy) VALUES
('Gasztronómikus', 'Botond', 'F', DATE ('1998-08-16'), 1, 5),
('Hústagadó', 'Endre', 'F', DATE ('1762-09-30'), 1, 3),
('Nyelvtanuló', 'Anikó', 'L', DATE ('1997-03-20'), 2, 4),
('Akcentusos', 'Eszter', 'L', DATE ('2003-11-13'), 2, 2),
('Csekő', 'Ákos', 'F', DATE ('1989-12-21'), 3, 5);
""")

# Elvégzek pár kiválasztást.

cur.execute("SELECT * FROM tanulok WHERE vezeteknev = 'Csekő';")

print(cur.fetchone())

cur.execute("SELECT * FROM tanulok WHERE nem LIKE 'L';")

print(cur.fetchall())

cur.execute("SELECT * FROM tanulok ORDER BY vezeteknev;")

print(cur.fetchall())

cur.execute("""
SELECT tanulok.vezeteknev, tanulok.keresztnev, tantargy.targynev, eredmeny.erdemjegy FROM tanulok
JOIN tantargy ON tanulok.targy_id = tantargy.id
JOIN eredmeny ON tanulok.jegy = eredmeny.id;
""")

print(cur.fetchall())



kapcsolat.commit()

cur.close()
kapcsolat.close()





