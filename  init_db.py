import sqlite3,csv

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


reader = csv.reader(open('data.csv', 'r'), delimiter=',')
for row in reader:

    to_db = [row[0],row[1],row[2],row[3],row[4],row[5],row[6]]
    cur.execute("INSERT INTO pasiens (nama_pasien,jenis_kelamin,hb,mch,mchc,mcv,status) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)


connection.commit()
connection.close()