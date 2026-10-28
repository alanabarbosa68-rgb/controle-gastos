import sqlite3

conexao = sqlite3.connect("data/gastos.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    local TEXT,
    categoria TEXT,
    valor REAL
)
""")

conexao.commit()
conexao.close()

print("Banco criado!")