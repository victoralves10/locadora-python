# Victor Alves Lopes RM561833

import os
import oracledb
import pandas as pd
from datetime import datetime
from tabulate import tabulate

# ==================== ORIENTAÇÕES PARA QUE O CÓDIGO FUNCIONE ====================

# 1. Copie o comando SQL e execute no seu banco de dados.
# 2. Faça o download das bibliotecas necessárias para que o código funcione no seu terminal:
#    pip install oracledb
#    pip install pandas
#    pip install tabulate

# ==================== COMANDO SQL PARA ORACLE ====================
"""
CREATE TABLE T_VEICULOS (
    id_veiculo INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo VARCHAR2(50),
    marca VARCHAR2(100),
    modelo VARCHAR2(100),
    ano_fabricacao INT,
    placa VARCHAR2(10),
    cor VARCHAR2(30),
    combustivel VARCHAR2(20),
    quilometragem INT,
    status VARCHAR2(20),
    valor_diaria FLOAT,
    data_aquisicao DATE
);
"""

# ==================== SUBALGORITMOS ====================

# ==================== APRESENTAÇÃO ====================

# limpa a tela do terminal dependendo do sistema.
def limpar_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# mostra um título centralizado com linhas decorativas em cima e embaixo.
def exibir_titulo_centralizado(_texto: str, _largura_caracteres: int) -> None:
    print("=-" * (_largura_caracteres // 2))
    print(_texto.center(_largura_caracteres))
    print("=-" * (_largura_caracteres // 2), "\n")

# imprime uma linha repetindo o símbolo que passar.
def imprimir_linha_separadora(simbolo: str, quantidade: int) -> None:
    print(f"{simbolo * quantidade}")

# ==================== VALIDAÇÃO E ENTRADA DE DADOS ====================

# pede um texto pro usuário até ele digitar algo que não seja vazio.
def obter_texto(_mensagem: str) -> str:
    texto_entrada = None
    while not texto_entrada:
        texto_entrada = str(input(_mensagem)).strip()
        if not texto_entrada:
            print("\nErro! Digite novamente.\n")
    return texto_entrada

# pede um número inteiro até o usuário digitar certo.
def obter_inteiro(_mensagem: str) -> int:
    numero_inteiro = None
    while numero_inteiro is None:
        try:
            numero_inteiro = int(input(_mensagem).strip())
        except ValueError:
            print("\nErro! Digite um número válido.\n")
    return numero_inteiro

# pede um número decimal até digitar certo.
def obter_float(_mensagem: str) -> float:
    valor_float = None
    while valor_float is None:
        try:
            valor_float = float(input(_mensagem).strip())
        except ValueError:
            print("\nErro! Digite um número válido.\n")
    return valor_float

# pede uma data no formato DD/MM/AAAA e só aceita se for válida.
def obter_data(_mensagem: str) -> str:
    data_valida = None
    while data_valida is None:
        data_str = str(input(_mensagem)).strip()
        if not data_str:
            print("\nErro! Digite novamente.\n")
            continue
        try:
            data_valida = datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            print("\nErro! Digite uma data válida no formato DD/MM/AAAA.\n")
            data_valida = None
    return data_valida.strftime("%d/%m/%Y")

# pede S ou N e devolve True ou False.
def obter_sim_ou_nao(_mensagem: str) -> bool:
    resposta_sim_nao = ""
    while resposta_sim_nao not in ["S", "N"]:
        resposta_sim_nao = str(input(_mensagem)).strip().upper()
        if resposta_sim_nao in ["S", "N"]:
            return resposta_sim_nao[0] == "S"
        print("\nErro! Digite apenas S ou N.\n")
        continue

# pede um inteiro só aceitando se estiver entre os limites que você passar.
def obter_inteiro_em_intervalo(_mensagem: str, _minimo: int, _maximo: int) -> int:
    entrada_valida = False
    while not entrada_valida:
        entrada_numero = obter_inteiro(_mensagem)
        if _minimo <= entrada_numero <= _maximo:
            entrada_valida = True
        else:
            print(f"\nErro! Digite um número entre {_minimo} e {_maximo}.\n")
    return entrada_numero

# ==================== BANCO DE DADOS ====================

# tenta conectar ao banco Oracle e devolve a conexão ou None se der erro.
def conectar_oracledb(_usuario: str, _senha: str, _dsn_conexao: str) -> oracledb.Connection:
    try:
        conexao_bd = oracledb.connect(
            user=_usuario,
            password=_senha,
            dsn=_dsn_conexao
        )
        return conexao_bd
    except Exception as e:
        print(f"Erro ao conectar com banco.\n\n{e}")
        return None

# pede todos os dados do veículo pro usuário e devolve num dicionário.
def solicitar_dados_cadastro_veiculo() -> dict:
    tipo = obter_texto("\nTipo do veículo: ")
    marca = obter_texto("\nMarca: ")
    modelo = obter_texto("\nModelo: ")
    ano_fabricacao = obter_inteiro("\nAno de fabricação: ")
    placa = obter_texto("\nPlaca ex(ABC1D23): ")
    cor = obter_texto("\nCor: ")

    mensagem_combustivel = """\nCombustível (escolha uma opção):
1. Gasolina
2. Etanol
3. Flex
4. Diesel
5. Elétrico
Escolha: """
    tipos_combustivel = {
        1: "Gasolina",
        2: "Etanol",
        3: "Flex",
        4: "Diesel",
        5: "Elétrico"
    }
    opcao_combustivel = obter_inteiro_em_intervalo(mensagem_combustivel, 1, 5)
    combustivel = tipos_combustivel[opcao_combustivel]

    quilometragem = obter_inteiro("\nQuilometragem: ")

    mensagem_status = """\nStatus (escolha uma opção):
1. Disponível
2. Alugado
3. Manutenção
Escolha: """
    tipos_status = {
        1: "Disponível",
        2: "Alugado",
        3: "Manutenção"
    }
    opcao_status = obter_inteiro_em_intervalo(mensagem_status, 1, 3)
    status = tipos_status[opcao_status]

    valor_diaria = obter_float("\nValor da diária: ")
    data_aquisicao = obter_data("\nData de aquisição do veículo (DD/MM/YYYY): ")

    dados_veiculo = {
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "ano_fabricacao": ano_fabricacao,
        "placa": placa,
        "cor": cor,
        "combustivel": combustivel,
        "quilometragem": quilometragem,
        "status": status,
        "valor_diaria": valor_diaria,
        "data_aquisicao": data_aquisicao
    }

    return dados_veiculo

# tenta salvar os dados do veículo no banco e retorna True se deu certo, False se deu erro.
def inserir_novo_veiculo(_conexao: oracledb.Connection, _dados_veiculo: dict) -> bool:
    try:
        comando_sql = """
INSERT INTO T_VEICULOS (
    tipo, marca, modelo, ano_fabricacao, placa, cor,
    combustivel, quilometragem, status, valor_diaria, data_aquisicao
)
VALUES (
    :tipo, :marca, :modelo, :ano_fabricacao, :placa, :cor,
    :combustivel, :quilometragem, :status, :valor_diaria, TO_DATE(:data_aquisicao, 'DD/MM/YYYY')
)
"""
        cur = _conexao.cursor()
        cur.execute(comando_sql, _dados_veiculo)
        _conexao.commit()
        cur.close()

        sucesso_cadastro = True

    except Exception as e:
        print(f"\nErro no cadastro.\n\n{e}")
        sucesso_cadastro = False

    return sucesso_cadastro

# pega todos os veículos do banco e mostra uma tabela resumida com ID, modelo, placa e status.
def buscar_resumo_veiculos(_conexao: oracledb.Connection) -> str:
    cur = _conexao.cursor()
    cur.execute("""SELECT id_veiculo, modelo, placa, status FROM T_VEICULOS""")
    resultados = cur.fetchall()
    cur.close()

    if not resultados:
        print("Nenhum veículo encontrado.")
        return None

    resultados_ordenados = sorted(resultados, key=lambda x: x[0])
    colunas = ["ID", "Modelo", "Placa", "Status"]

    tabela_resumo = tabulate(
        resultados_ordenados,
        headers=colunas,
        tablefmt="fancy_grid",
        numalign="right",
        stralign="right"
    )
    return tabela_resumo

# pega todos os detalhes de um veículo específico pelo ID e mostra em tabela.
def buscar_detalhes_veiculo_por_id(_conexao: oracledb.Connection, _id_veiculo: int) -> str:
    cur = _conexao.cursor()
    comando_sql = """SELECT * FROM T_VEICULOS WHERE id_veiculo = :id_veiculo"""
    cur.execute(comando_sql, {"id_veiculo": _id_veiculo})
    dados_detalhados = cur.fetchall()
    cur.close()

    if not dados_detalhados:
        print("Nenhum veículo encontrado.")
        return None

    colunas = [
        "ID", "Tipo", "Marca", "Modelo", "Ano Fab.", "Placa", "Cor",
        "Combustível", "Km", "Status", "Valor Diária", "Data Aquisição"
    ]

    tabela_detalhada = tabulate(
        dados_detalhados,
        headers=colunas,
        tablefmt="fancy_grid",
        numalign="right",
        stralign="right"
    )
    return tabela_detalhada

# busca todos os veículos do banco e retorna uma lista de dicionários
def buscar_todos_veiculos_como_dicionario(_conexao: oracledb.Connection) -> list:
    cur = _conexao.cursor()
    cur.execute("""
        SELECT id_veiculo, tipo, marca, modelo, ano_fabricacao, placa, cor,
               combustivel, quilometragem, status, valor_diaria, data_aquisicao
        FROM T_VEICULOS
    """)

    # nomes das colunas
    nomes_colunas = []
    for col in cur.description:
        nomes_colunas.append(col[0].upper())
    
    resultados_db = cur.fetchall()
    cur.close()

    if not resultados_db:
        return None

    # converte cada linha em dicionário
    lista_de_veiculos = []
    for linha in resultados_db:
        registro = {}
        for i in range(len(nomes_colunas)):
            registro[nomes_colunas[i]] = linha[i]
        lista_de_veiculos.append(registro)

    return lista_de_veiculos


# formata uma lista de veículos em tabela (tabulate)
def formatar_lista_veiculos_em_tabela(_lista_dados_veiculos: list) -> str:
    if not _lista_dados_veiculos:
        print("Nenhum veículo encontrado.")
        return None

    chaves_colunas_db = [
        "ID_VEICULO", "TIPO", "MARCA", "MODELO", "ANO_FABRICACAO",
        "PLACA", "COR", "COMBUSTIVEL", "QUILOMETRAGEM",
        "STATUS", "VALOR_DIARIA", "DATA_AQUISICAO"
    ]

    headers_tabela = [
        "ID", "Tipo", "Marca", "Modelo", "Ano Fab.", "Placa", "Cor",
        "Combustível", "Km", "Status", "Valor Diária", "Data Aquisição"
    ]

    # Cria a lista de listas para o tabulate, usando as chaves dos dicionários
    dados_para_tabela = []
    for veiculo in _lista_dados_veiculos:
        linha_tabela = []
        for chave in chaves_colunas_db:
            valor = veiculo.get(chave, "")
            linha_tabela.append(valor)
        dados_para_tabela.append(linha_tabela)

    tabela_formatada = tabulate(
        dados_para_tabela,
        headers=headers_tabela,
        tablefmt="fancy_grid",
        numalign="right",
        stralign="right"
    )
    return tabela_formatada

# tenta atualizar os dados de um veículo no banco pelo ID e retorna True se deu certo, False se deu erro.
def atualizar_dados_veiculo(_conexao: oracledb.Connection, _novos_dados: dict, _id_veiculo_alvo: int) -> bool:
    try:
        comando_sql = """
        UPDATE T_VEICULOS
        SET tipo = :tipo,
            marca = :marca,
            modelo = :modelo,
            ano_fabricacao = :ano_fabricacao,
            placa = :placa,
            cor = :cor,
            combustivel = :combustivel,
            quilometragem = :quilometragem,
            status = :status,
            valor_diaria = :valor_diaria,
            data_aquisicao = TO_DATE(:data_aquisicao, 'DD/MM/YYYY')
        WHERE id_veiculo = :id_veiculo
        """

        dados_para_bind = _novos_dados.copy()
        dados_para_bind["id_veiculo"] = _id_veiculo_alvo

        cur = _conexao.cursor()
        cur.execute(comando_sql, dados_para_bind)
        _conexao.commit()
        cur.close()

        sucesso_atualizacao = True

    except Exception as e:
        print(f"\nErro no cadastro.\n\n{e}")
        sucesso_atualizacao = False

    return sucesso_atualizacao

# tenta excluir um veículo da tabela do banco de dados pelo id e retorna True se deu certo, False se deu erro.
def excluir_veiculo_por_id(_conexao: oracledb.Connection, _id_veiculo: int) -> bool:
    try:
        comando_sql = f"""DELETE FROM T_VEICULOS  WHERE id_veiculo = :id_veiculo"""
        cur = _conexao.cursor()
        cur.execute(comando_sql, {"id_veiculo": _id_veiculo})
        _conexao.commit()
        cur.close()

        sucesso_remocao = True

    except Exception as e:
        print(f"\nErro na remoção.\n\n{e}")
        sucesso_remocao = False

    return sucesso_remocao

def excluir_todos_veiculos(_conexao: oracledb.Connection) -> None:
    try:
        comando_sql = f"""DELETE FROM T_VEICULOS"""
        cur = _conexao.cursor()
        cur.execute(comando_sql)
        _conexao.commit()
        cur.close()
        
        sucesso_exclusao = True

    except Exception as e:
        print(f"\nErro na operação.\n\n{e}")
        sucesso_exclusao = False

    return sucesso_exclusao       


# ==================== GERENCIAMENTO JSON ====================



# ==================== PROGRAMA PRINCIPAL ====================

try:
    user = "rm561833" # retirar dps *
    password = "070406" # retirar dps *
    dsn = "oracle.fiap.com.br:1521/ORCL" # retirar dps *
    conn = conectar_oracledb(user, password, dsn)
    conectado = bool(conn)
except Exception as e:
    conectado = False

while conectado:
    limpar_terminal()
    exibir_titulo_centralizado("LOCADORA DE VEÍCULOS", 60)
    print("""
1. Registrar novo veículo
2. Consultar registros
3. Atualizar informações
4. Remover veículo
5. Limpar todos os registros

0. Sair
          """)
    escolha_menu = obter_inteiro_em_intervalo("Escolha: ", 0, 9)

    match escolha_menu:
        case 0:
            limpar_terminal()
            print("\nPrograma encerrado. Até logo!\n")
            conectado = False

        case 1:
            limpar_terminal()
            exibir_titulo_centralizado("FICHA DE CADASTRO", 60)
            dados_do_registro = solicitar_dados_cadastro_veiculo()
            sucesso = inserir_novo_veiculo(conn, dados_do_registro)
            if sucesso:
                print("\nVeículo registrado com sucesso!")
            input("\nPrecione ENTER para continuar...")

# ---------------------- AULA 21/10/2025

        case 2:
            todos_veiculos = buscar_todos_veiculos_como_dicionario(conn)

            if not todos_veiculos:
                limpar_terminal()
                exibir_titulo_centralizado("CONSULTA / LISTA DE VEÍCULOS", 60)
                print("\nNenhum veículo encontrado.\n")
                input("\nPrecione ENTER para continuar...")
            else:
                escolha_menu = -1
                while escolha_menu != 0:
                    limpar_terminal()
                    exibir_titulo_centralizado("CONSULTA / LISTA DE VEÍCULOS", 60)

                    print("""1. Listar todos os veículos
2. Consultar veículo por ID
3. Pesquisar por texto
4. Pesquisar por número

0. Voltar ao menu principal
""")

                    escolha_menu = obter_inteiro_em_intervalo("Escolha: ", 0, 4)

                    if escolha_menu == 0:
                        break

                    match escolha_menu:
                        case 1:
                            limpar_terminal()
                            exibir_titulo_centralizado("LISTA DE TODOS OS VEÍCULOS", 170)
                            tabela_formatada = formatar_lista_veiculos_em_tabela(todos_veiculos)
                            if tabela_formatada:
                                print(tabela_formatada)
                            else:
                                print("\nNenhum veículo encontrado.\n")
                            input("\nPrecione ENTER para continuar...")

                        case 2:
                            id_veiculo_consulta = -1
                            while id_veiculo_consulta != 0:
                                limpar_terminal()
                                exibir_titulo_centralizado("CONSULTA DE VEÍCULO POR ID", 170)
                                tabela_previa = buscar_resumo_veiculos(conn)

                                if tabela_previa:
                                    print("\nESCOLHA O ID DO VEÍCULO QUE DESEJA CONSULTAR:\n")
                                    print(tabela_previa)
                                    print("\nDIGITE '0' PARA VOLTAR AO MENU PRINCIPAL\n")
                                    id_veiculo_consulta = obter_inteiro("\nDigite o ID do veículo: ")
                                else:
                                    id_veiculo_consulta = 0
                                    continue

                                if id_veiculo_consulta == 0:
                                    break

                                tabela_detalhes = buscar_detalhes_veiculo_por_id(conn, id_veiculo_consulta)
                                limpar_terminal()
                                exibir_titulo_centralizado("CONSULTA DE VEÍCULO POR ID", 170)

                                if tabela_detalhes:
                                    print(tabela_detalhes)
                                else:
                                    print("\nNenhum veículo encontrado com esse ID.\n")

                                input("\nPrecione ENTER para continuar...")

                        case 3:
                            limpar_terminal()
                            exibir_titulo_centralizado("CONSULTA DE VEÍCULO POR TEXTO", 170)
                            print("\nEm manutenção\n")
                            input("\nPrecione ENTER para continuar...")

                        case 4:
                            limpar_terminal()
                            exibir_titulo_centralizado("CONSULTA DE VEÍCULO POR NÚMERO", 170)
                            print("\nEm manutenção\n")
                            input("\nPrecione ENTER para continuar...")

# ---------------------- AULA 21/10/2025
        case 3:
            id_veiculo_atualizar = -1

            while id_veiculo_atualizar != 0:
                limpar_terminal()
                exibir_titulo_centralizado("ATUALIZAR VEÍCULO", 170)
                tabela_previa = buscar_resumo_veiculos(conn)
                
                if tabela_previa:
                    print("\nESCOLHA O ID DO VEÍCULO QUE DESEJA ATUALIZAR:\n")
                    print(tabela_previa)
                    print("\nDIGITE '0' PARA VOLTAR AO MENU PRINCIPAL\n")
                    id_veiculo_atualizar = obter_inteiro("\nDigite o ID do veículo: ")
                else:
                    id_veiculo_atualizar = 0
                    continue

                if id_veiculo_atualizar == 0:
                    break

                tabela_detalhes = buscar_detalhes_veiculo_por_id(conn, id_veiculo_atualizar)
                limpar_terminal()
                exibir_titulo_centralizado("ATUALIZAR VEÍCULO", 170)

                if tabela_detalhes:
                    print("DADOS ATUAIS")
                    print(tabela_detalhes)
                    print("\nDigite os novos dados do veículo:\n")
                    novos_dados = solicitar_dados_cadastro_veiculo()
                    sucesso_atualizacao = atualizar_dados_veiculo(conn, novos_dados, id_veiculo_atualizar)
                    if sucesso_atualizacao:
                        print("\nVeículo atualizado com sucesso!")
                    else:
                        print("\nErro ao atualizar o veículo.\n")
                else:
                    print("\nNenhum veículo encontrado com esse ID.\n")

                input("\nPrecione ENTER para continuar...")

            input("\nPrecione ENTER para continuar...")

        case 4:
            id_veiculo_remover = -1

            while id_veiculo_remover != 0:
                limpar_terminal()
                exibir_titulo_centralizado("REMOVER VEÍCULO", 170)
                tabela_previa = buscar_resumo_veiculos(conn)
                
                if tabela_previa:
                    print("\nESCOLHA O ID DO VEÍCULO QUE DESEJA REMOVER:\n")
                    print(tabela_previa)
                    print("\nDIGITE '0' PARA VOLTAR AO MENU PRINCIPAL\n")
                    id_veiculo_remover = obter_inteiro("\nDigite o ID do veículo: ")
                else:
                    id_veiculo_remover = 0
                    continue

                if id_veiculo_remover == 0:
                    break

                tabela_detalhes = buscar_detalhes_veiculo_por_id(conn, id_veiculo_remover)
                limpar_terminal()
                exibir_titulo_centralizado("REMOVER VEÍCULO", 170)

                if tabela_detalhes:
                    print("DADOS ATUAIS")
                    print(tabela_detalhes)
                    escolha = obter_sim_ou_nao("\nDESEJA EXCLUIR ESSE REGISTRO? (S/N): ")

                    if escolha:
                        sucesso = excluir_veiculo_por_id(conn, id_veiculo_remover)
                        if sucesso:
                            print("\nVeículo removido com sucesso!")
                        else:
                            print("\nErro ao remover o veículo.\n")
                    else:
                        print("\nRemoção cancelada pelo usuário.\n")
                else:
                    print("\nNenhum veículo encontrado com esse ID.\n")

                input("\nPrecione ENTER para continuar...")

            input("\nPrecione ENTER para continuar...")


        case 5:
            limpar_terminal()
            exibir_titulo_centralizado("REMOVER TODOS OS REGISTROS", 170)
            tabela_previa = buscar_resumo_veiculos(conn)
            if tabela_previa:
                print("\nREGISTSROS ATUAIS\n")
                print(tabela_previa)

                confirmacao = obter_sim_ou_nao("\nCONFIRMA A EXCLUSÃO DE TODOS OS VEÍCULOS? [S]im ou [N]ÃO? ")
                if confirmacao:
                    sucesso = excluir_todos_veiculos(conn)
                    if sucesso:
                        print("\nTODOS OS REGISTROS FORAM REMOVIDOS\n")
                else:
                    print("\nOperação cancelada...")


            input("\nPrecione ENTER para continuar...")

        case 7:
            limpar_terminal()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")

        case 8:
            limpar_terminal()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")

        case 9:
            limpar_terminal()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")