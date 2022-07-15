import sqlite3
import requests
import arrow

ar = arrow.now().format('DD/MM/YYYY')
conexao = sqlite3.connect('DataBase.db')
cursor = conexao.cursor()


def validar_cpf(numeros):
    cpf = [int(caracter) for caracter in numeros if caracter.isdigit()]
    if len(cpf) != 11 or cpf == cpf[::-1]:
        return False
    else:
        for i in range(9, 11):
            valor = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digito = ((valor * 10) % 11) % 10
            if digito != cpf[i]:
                return False
        return True

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
class Dados:
    def cadastro_cliente(self):
        nome_cliente = input('Nome do Cliente: ')
        CPF_cliente = input('CPF do Cliente: ')
        if not validar_cpf(CPF_cliente):
            print('\033[31mCPF Inválido\033[0m')
        else:
            CEP_cliente = input('CEP do Cliente: ')
            info = requests.get(f'https://cep.awesomeapi.com.br/json/{CEP_cliente}')
            info = info.json()
            CEP_cliente = f'{info["city"]} - {info["state"]} - {info["district"]} - {info["address"]}'
            numcasa_cliente = input('Número da Casa do Cliente: ')
            cursor.execute(f'INSERT INTO Clientes (NomeCliente, CPFCliente, CEPCliente, N°Casa)'
                           f'VALUES("{nome_cliente}", "{CPF_cliente}", "{CEP_cliente}", "{numcasa_cliente}")')
            conexao.commit()
            print('\033[35mCliente Cadastrado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def editar_cliente(self):
        cpf = input('Digite o CPF do cliente que deseja alterar: ')
        cursor.execute(f'SELECT * FROM Clientes WHERE CPFCliente ="{cpf}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mCliente não encontrado!\033[0m')
        else:
            print(f'{linha}')
            print('=-=' * 10)
            print('Qual campo que deseja alterar?')
            print('[1] Nome   [2] CPF   [3] CEP   [4] Numero da Casa')
            op = int(input('Digite a opção desejada: '))
            lista = ['', 'NomeCliente', 'CPFCliente', 'CEPCliente', 'N°Casa']
            if op == 2:
                CPF_cliente = input('Nova Informação: ')
                if not validar_cpf(CPF_cliente):
                    print('\033[31mCPF Inválido\033[0m')
                else:
                    cursor.execute(f'UPDATE Clientes SET CPFCliente="{CPF_cliente}" WHERE CPFCliente="{cpf}"')
                    conexao.commit()
                    print('\033[35mCliente Atualizado!\033[0m')
            elif op == 3:
                y = input('Nova Informação: ')
                info = requests.get(f'https://cep.awesomeapi.com.br/json/{y}')
                info = info.json()
                CEP_cliente = f'{info["city"]} - {info["state"]} - {info["district"]} - {info["address"]}'
                cursor.execute(f'UPDATE Clientes SET CEPCliente="{CEP_cliente}" WHERE CPFCliente="{cpf}"')
                conexao.commit()
                print('\033[35mCliente Atualizado!\033[0m')
            else:
                x = input('Nova Informação: ')
                cursor.execute(f'UPDATE Clientes SET {lista[op]}="{x}" WHERE CPFCliente="{cpf}"')
                conexao.commit()
                print('\033[35mCliente Atualizado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def deletar_cliente(self):
        cpf = input('Digite o CPF do cliente que deseja deletar: ')
        cursor.execute(f'SELECT * FROM Clientes WHERE CPFCliente ="{cpf}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mCliente não encontrado!\033[0m')
        else:
            print(f'{linha}')
            print('---' * 10)
            cursor.execute(f'DELETE FROM Clientes WHERE CPFCliente ="{cpf}"')
            conexao.commit()
            print('\033[35mCliente Deletado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def cadastro_produto(self):
        nome_produto = input('Nome do Produto: ')
        familia_produto = input('Família do Produto: ')
        codigo_barras = input('Código de Barras do Produto: ')
        cursor.execute(f'INSERT INTO Produtos (NomeProduto, FamíliaProduto, CódigoBarras)'
                       f'VALUES("{nome_produto}", "{familia_produto}", "{codigo_barras}")')
        conexao.commit()
        print('\033[35mProduto Cadastrado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def editar_produto(self):
        barra = input('Digite o Código de Barras do produto que deseja alterar: ')
        cursor.execute(f'SELECT * FROM Produtos WHERE CódigoBarras="{barra}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mProduto não encontrado!\033[0m')
        else:
            print(f'{linha}')
            print('=-=' * 10)
            print('Qual campo que deseja alterar?')
            print('[1] Nome   [2] Família   [3] Código')
            op = int(input('Digite a opção desejada: '))
            lista = ['', 'NomeProduto', 'FamíliaProduto', 'CódigoBarras']
            x = input('Nova Informação: ')
            cursor.execute(f'UPDATE Produtos SET {lista[op]}="{x}" WHERE CódigoBarras="{barra}"')
            conexao.commit()
            print('\033[35mProduto Atualizado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def deletar_produto(self):
        barra = input('Digite o Código de Barras do produto que deseja deletar: ')
        cursor.execute(f'SELECT * FROM Produtos WHERE CódigoBarras="{barra}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mProduto não encontrado!\033[0m')
        else:
            print(f'{linha}')
            print('---' * 10)
            cursor.execute(f'DELETE FROM Produtos WHERE CódigoBarras="{barra}"')
            conexao.commit()
            print('\033[35mProduto Deletado!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def cadastro_venda(self):
        lista = []
        cursor.execute(f'SELECT CódigoBarras FROM Produtos WHERE CódigoBarras="{input("Código do Produto: ")}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mCódigo não Cadastrado\033[0m')
        else:
            lista.append(linha[0])
            cursor.execute(f'SELECT CPFCliente FROM Clientes WHERE CPFCliente="{input("CPF do Cliente: ")}"')
            linha = cursor.fetchone()
            if linha is None:
                print('\033[31mCPF não Cadastrado\033[0m')
            else:
                lista.append(linha[0])
                quantidade_venda = float(input('Quantidade Comprada: '))
                valor_unitario = float(input('Valor Individual do Produto: '))
                valor_total = valor_unitario * quantidade_venda
                cursor.execute(
                    f'INSERT INTO Vendas (DataVenda, CódigoBarras, CPFCliente, Quantidade, ValorUnitário, ValorTotal)'
                    f'VALUES("{ar}", "{lista[0]}", "{lista[1]}", "{quantidade_venda}", "{valor_unitario}", "{valor_total}")')
                conexao.commit()
                print('\033[35mVenda Cadastrada!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def editar_venda(self):
        barra = input('Digite o Código de Barras do produto vendido: ')
        cursor.execute(f'SELECT * FROM Vendas WHERE CódigoBarras="{barra}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mCódigo não encontrado!\033[0m')
        else:
            cpf = input('Digite o CPF do Cliente para qual o produto foi vendido: ')
            cursor.execute(f'SELECT * FROM Vendas WHERE CPFCliente="{cpf}"')
            linha = cursor.fetchone()
            if linha is None:
                print('\033[31mCPF não encontrado!\033[0m')
            else:
                print(f'{linha}')
                print('=-=' * 10)
                print('Qual campo que deseja alterar?')
                print('[1] Data de Venda   [2] Código   [3] CPF   [4] Quantidade   '
                      '[5] Valor Unitário')
                op = int(input('Digite a opção desejada: '))
                lista = ['', 'DataVenda', 'CódigoBarras', 'CPFCliente', 'Quantidade', 'ValorUnitário']
                x = input('Nova Informação: ')
                cursor.execute(f'UPDATE Vendas SET {lista[op]}="{x}" WHERE CPFCliente="{cpf}"')
                conexao.commit()
                cursor.execute(f'SELECT Quantidade, ValorUnitário FROM Vendas WHERE CPFCliente="{cpf}"')
                linha = cursor.fetchmany(2)
                cursor.execute(f'UPDATE Vendas SET ValorTotal="{linha[0][0] * linha[0][1]}" WHERE CPFCliente="{cpf}"')
                conexao.commit()
                print('\033[35mVenda Atualizada!\033[0m')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def deletar_venda(self):
        barra = input('Digite o Código de Barras do produto vendido: ')
        cursor.execute(f'SELECT * FROM Vendas WHERE CódigoBarras="{barra}"')
        linha = cursor.fetchone()
        if linha is None:
            print('\033[31mCódigo não encontrada!\033[0m')
        else:
            cpf = input('Digite o CPF do Cliente para qual o produto foi vendido: ')
            cursor.execute(f'SELECT * FROM Vendas WHERE CPFCliente="{cpf}"')
            linha = cursor.fetchone()
            if linha is None:
                print('\033[31mCPF não encontrada!\033[0m')
            else:
                print(f'{linha}')
                print('---' * 10)
                cursor.execute(f'DELETE FROM Vendas WHERE CPFCliente="{cpf}"')
                conexao.commit()
                print('\033[35mVenda Deletada!\033[0m')
