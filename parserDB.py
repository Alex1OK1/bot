import sqlite3

c = sqlite3.connect("words.db")
cur = c.cursor()
with open("slova.txt", encoding='utf-8') as a:
    for i in a.readlines():
        v = i[:i.index("[") - 1] + ":::::::" + i[i.index("]") + 2:-1].lower()
        f, g = v.split(":::::::")
        cur.execute(f"INSERT INTO words VALUES(NULL, '{f}' ,'{g}') ").fetchall()
        c.commit()
        print(g)

