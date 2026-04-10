from database import criar_tabelas
from operacoes import inserir_produto, listar_produtos, atualizar_quantidade, excluir_produto

def main():
    criar_tabelas()
    
    inserir_produto("Leite Meio Gordo", "Laticínios", 40, "2024-05-15", "2024-05-01")
    inserir_produto("Iogurte Natural", "Laticínios", 120, "2024-05-20", "2024-05-01")
    inserir_produto("Maçã Fuji", "Frutas", 300, "2024-06-10", "2024-05-01")
    
    atualizar_quantidade(1, 35)
    
    excluir_produto(2)
    
    produtos = listar_produtos()
    
    print(f"{'ID':<5} | {'NOME':<20} | {'CATEGORIA':<15} | {'QTD':<5} | {'VALIDADE':<10} | {'ENTRADA':<10}")
    print("-" * 80)
    
    for p in produtos:
        print(f"{p[0]:<5} | {p[1]:<20} | {p[2]:<15} | {p[3]:<5} | {p[4]:<10} | {p[5]:<10}")

if __name__ == "__main__":
    main()