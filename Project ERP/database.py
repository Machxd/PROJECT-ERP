import sqlite3

def conectar():
    return sqlite3.connect("inventario.db")

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        lote TEXT NOT NULL,
        quantidade REAL NOT NULL,
        data_validade TEXT NOT NULL,
        data_entrada TEXT NOT NULL
    );
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo_movimento TEXT NOT NULL,
        quantidade REAL NOT NULL,
        data_hora TEXT NOT NULL,
        motivo TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    );
    """)
    
    conn.commit()
    conn.close()