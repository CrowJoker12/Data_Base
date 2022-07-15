import Ex1_Defs as ed

dados = ed.Dados()
print('=-=' * 10)

while True:
    def escolher():
        print('''\033[96mBem Vindo! Selecione as opções que desejar!\033[0m
        [1] \033[32mCadastrar Cliente\033[0m   [2] \033[35mEditar Cliente\033[0m   [3] \033[31mDeletar Cliente\033[0m
        [4] \033[32mCadastrar Produto\033[0m   [5] \033[35mEditar Produto\033[0m   [6] \033[31mDeletar Produto\033[0m
        [7] \033[32mCadastrar Venda\033[0m     [8] \033[35mEditar Venda\033[0m     [9] \033[31mDeletar Venda\033[0m
        [10] Terminar Algoritmo''')
        opcao = int(input('Opção: '))
        return opcao


    def op1():
        dados.cadastro_cliente()
        print('=-='*10)


    def op2():
        dados.editar_cliente()
        print('=-=' * 10)


    def op3():
        dados.deletar_cliente()
        print('=-=' * 10)


    def op4():
        dados.cadastro_produto()
        print('=-=' * 10)


    def op5():
        dados.editar_produto()
        print('=-=' * 10)


    def op6():
        dados.deletar_produto()
        print('=-=' * 10)


    def op7():
        dados.cadastro_venda()
        print('=-=' * 10)


    def op8():
        dados.editar_venda()
        print('=-=' * 10)


    def op9():
        dados.deletar_venda()
        print('=-=' * 10)


    def op10():
        print('Terminando...')


    dic = {1: op1, 2: op2, 3: op3, 4: op4, 5: op5, 6: op6, 7: op7, 8: op8, 9: op9, 10: op10}

    opcao_escolhida = escolher()
    dic[opcao_escolhida]()
    if opcao_escolhida == 10:
        break
