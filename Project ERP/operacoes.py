import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("inventario.db")

def inserir_produto(nome, categoria, lote, quantidade, data_validade, data_entrada):
    conn = conectar()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO produtos (nome, categoria, lote, quantidade, data_validade, data_entrada)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, categoria, lote, quantidade, data_validade, data_entrada))
    
    produto_id = cur.lastrowid
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
    INSERT INTO movimentacoes (produto_id, tipo_movimento, quantidade, data_hora, motivo)
    VALUES (?, 'entrada', ?, ?, 'Cadastro Inicial')
    """, (produto_id, quantidade, data_hora))
    
    conn.commit()
    conn.close()

def inserir_produtos_lote(lista_produtos):
    conn = conectar()
    cur = conn.cursor()
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for p in lista_produtos:
        lote_val = p[2] if len(p) > 5 else "Lote Padrão"
        qtd_val = p[3] if len(p) > 5 else p[2]
        val_val = p[4] if len(p) > 5 else p[3]
        ent_val = p[5] if len(p) > 5 else p[4]
        
        cur.execute("""
        INSERT INTO produtos (nome, categoria, lote, quantidade, data_validade, data_entrada)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (p[0], p[1], lote_val, qtd_val, val_val, ent_val))
        
        produto_id = cur.lastrowid
        cur.execute("""
        INSERT INTO movimentacoes (produto_id, tipo_movimento, quantidade, data_hora, motivo)
        VALUES (?, 'entrada', ?, ?, 'Importação CSV')
        """, (produto_id, qtd_val, data_hora))
        
    conn.commit()
    conn.close()

def editar_produto_completo(produto_id, nome, categoria, lote, quantidade, validade, entrada):
    conn = conectar()
    cur = conn.cursor()
    
    cur.execute("""
    UPDATE produtos
    SET nome = ?, categoria = ?, lote = ?, quantidade = ?, data_validade = ?, data_entrada = ?
    WHERE id = ?
    """, (nome, categoria, lote, quantidade, validade, entrada, produto_id))
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
    INSERT INTO movimentacoes (produto_id, tipo_movimento, quantidade, data_hora, motivo)
    VALUES (?, 'ajuste', ?, ?, 'Edição de Cadastro')
    """, (produto_id, quantidade, data_hora))
    
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM produtos")
    produtos = cur.fetchall()
    conn.close()
    return produtos

def excluir_produto(produto_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM movimentacoes WHERE produto_id = ?", (produto_id,))
    cur.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

def registrar_movimento(produto_id, tipo, quantidade, motivo):
    conn = conectar()
    cur = conn.cursor()
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cur.execute("""
    INSERT INTO movimentacoes (produto_id, tipo_movimento, quantidade, data_hora, motivo)
    VALUES (?, ?, ?, ?, ?)
    """, (produto_id, tipo, quantidade, data_hora, motivo))
    
    if tipo == 'entrada':
        cur.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
    elif tipo in ['saida', 'desperdicio']:
        cur.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))
        
    conn.commit()
    conn.close()

def listar_movimentacoes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
    SELECT m.id, p.nome, m.tipo_movimento, m.quantidade, m.data_hora, m.motivo 
    FROM movimentacoes m
    JOIN produtos p ON m.produto_id = p.id
    ORDER BY m.data_hora DESC
    """)
    movimentos = cur.fetchall()
    conn.close()
    return movimentos