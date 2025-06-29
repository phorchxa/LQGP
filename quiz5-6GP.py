import sqlite3
import matplotlib.pyplot as plt

#1 ბაზასთან დაკავშირება
conn = sqlite3.connect("boloquiz.db")
cursor = conn.cursor()

#2 fetchall-ის გამოყენება, იმ დღეების წაკითხვა როცა ფასი იყო 900-ზე მეტი
cursor.execute("SELECT * FROM Nvidia_stock WHERE High > 900")
rows = cursor.fetchall()
for row in rows:
    print(row)
#3 input-ით შეყვნაილი მონაცემების ცხრილში დამატება
date = input("შეიყვანე თარიღი (YYYY-MM-DD): ")
close = float(input("Close ფასი: "))
high = float(input("High ფასი: "))
low = float(input("Low ფასი: "))
open_ = float(input("Open ფასი: "))
volume = int(input("Volume (მოცულობა): "))

cursor.execute("""
INSERT INTO Nvidia_stock (Date, Close, High, Low, Open, Volume)
VALUES (?, ?, ?, ?, ?, ?)
""", (date, close, high, low, open_, volume))
conn.commit()
#4 (crud ბრძანებები) update ფასი მითითებულ თარიღში
date = input("შეიყვანე თარიღი, რომლის Close ფასი უნდა განაახლო: ")
new_close = float(input("შეიყვანე ახალი Close ფასი: "))

cursor.execute("UPDATE Nvidia_stock SET Close = ? WHERE Date = ?", (new_close, date))
conn.commit()

#5 (crud ბრძანებები) delete მონაცმეის წასლა თარიღის მითითებით
date_to_delete = input("შეიყვანე თარიღი წასაშლელად: ")

cursor.execute("DELETE FROM Nvidia_stock WHERE Date = ?", (date_to_delete,))
conn.commit()

#6 Matpltlib - 3 ტიპის დიაგრამა
cursor.execute("SELECT Date, Close FROM Nvidia_stock ORDER BY Date DESC LIMIT 7")
data = cursor.fetchall()
dates = [row[0] for row in data]
closes = [row[1] for row in data]

plt.figure(figsize=(10,5))
plt.bar(dates, closes, color='teal')
plt.title("ბოლო 7 დღის Close ფასები")
plt.xlabel("თარიღი")
plt.ylabel("Close ფასი")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#7 Lince chart-ი ფასის ცვლილებისთვის დროში
cursor.execute("SELECT Date, High FROM Nvidia_stock ORDER BY Date ASC LIMIT 30")
data = cursor.fetchall()
dates = [row[0] for row in data]
highs = [row[1] for row in data]

plt.figure(figsize=(10,5))
plt.plot(dates, highs, color='orange', marker='o')
plt.title("High ფასების ცვლილება (30 დღე)")
plt.xlabel("თარიღი")
plt.ylabel("High ფასი")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

#8 pie chart-ის განაწილება
cursor.execute("""
SELECT 
  CASE 
    WHEN Close >= 900 THEN 'ძალიან მაღალი'
    WHEN Close >= 700 THEN 'მაღალი'
    WHEN Close >= 500 THEN 'საშუალო'
    ELSE 'დაბალი'
  END AS category,
  COUNT(*) 
FROM Nvidia_stock
GROUP BY category
""")
data = cursor.fetchall()
labels = [row[0] for row in data]
counts = [row[1] for row in data]

plt.figure(figsize=(6,6))
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title("Close ფასების კატეგორიების განაწილება")
plt.show()

#9 ბაზის დახურვა
conn.close()

