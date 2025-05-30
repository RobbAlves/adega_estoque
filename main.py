import sqlite3

# Conexão com banco de dados SQLite
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criação da tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS bebidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
)
''')
conn.commit()

# Funções do sistema
def adicionar_bebida():
    nome = input("Nome da bebida: ")
    tipo = input("Tipo (vinho, cerveja, destilado...): ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço por unidade: "))
    cursor.execute("INSERT INTO bebidas (nome, tipo, quantidade, preco) VALUES (?, ?, ?, ?)",
                   (nome, tipo, quantidade, preco))
    conn.commit()
    print("✅ Bebida adicionada com sucesso!\n")

def listar_bebidas():
    cursor.execute("SELECT * FROM bebidas")
    bebidas = cursor.fetchall()
    print("\n📋 Estoque de Bebidas:")
    for bebida in bebidas:
        print(f"ID: {bebida[0]} | Nome: {bebida[1]} | Tipo: {bebida[2]} | Quantidade: {bebida[3]} | Preço: R${bebida[4]:.2f}")
    print("")

def atualizar_quantidade():
    id_bebida = int(input("ID da bebida para atualizar: "))
    nova_quantidade = int(input("Nova quantidade: "))
    cursor.execute("UPDATE bebidas SET quantidade = ? WHERE id = ?", (nova_quantidade, id_bebida))
    conn.commit()
    print("🔄 Quantidade atualizada!\n")

def remover_bebida():
    id_bebida = int(input("ID da bebida para remover: "))
    cursor.execute("DELETE FROM bebidas WHERE id = ?", (id_bebida,))
    conn.commit()
    print("🗑️ Bebida removida do estoque.\n")

def buscar_bebida():
    nome = input("Nome da bebida para buscar: ")
    cursor.execute("SELECT * FROM bebidas WHERE nome LIKE ?", ('%' + nome + '%',))
    resultados = cursor.fetchall()
    print("\n🔍 Resultado da busca:")
    for bebida in resultados:
        print(f"ID: {bebida[0]} | Nome: {bebida[1]} | Tipo: {bebida[2]} | Quantidade: {bebida[3]} | Preço: R${bebida[4]:.2f}")
    print("")

# Menu principal
def menu():
    while True:
        print("=== Sistema de Estoque da Adega ===")
        print("1. Adicionar bebida")
        print("2. Listar bebidas")
        print("3. Atualizar quantidade")
        print("4. Remover bebida")
        print("5. Buscar bebida")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_bebida()
        elif opcao == '2':
            listar_bebidas()
        elif opcao == '3':
            atualizar_quantidade()
        elif opcao == '4':
            remover_bebida()
        elif opcao == '5':
            buscar_bebida()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.\n")

    conn.close()

# Executar o menu
if __name__ == "__main__":
    menu()
