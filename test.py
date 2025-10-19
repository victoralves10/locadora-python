# Victor Alves Lopes RM561833

import os
import oracledb
import pandas as pd
from datetime import datetime
from tabulate import tabulate

# ORIENTAÇÕES PARA QUE O CÓDIGO FUNCIONE:
    # 1. Copie o comando SQL e execute no seu banco de dados.
    # 2. Faça o download das bibliotecas necessárias para que o código funcione no seu terminal:
        # pip install oracledb
        # pip install pandas
        # pip install tabulate

# COMANDO SQL PARA ORACLE:
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

# -------------------- SUBALGORITMOS


# -------------------- APRESENTAÇÃO

# Limpa o terinal.
def limpa_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# Exibe um título centralizado entre duas linhas decorativas "=-".
def titulo_centralizado(_texto: str, _qtd_caracteres: int) -> None:
    print("=-" * (_qtd_caracteres // 2))
    print(_texto.center(_qtd_caracteres))
    print("=-" * (_qtd_caracteres // 2), "\n")

# Imprime uma simbolo separador.
def imprime_linha_separadora(simbolo: str, quantidade: int):
    print(f"{simbolo * quantidade}")


# -------------------- VALIDAÇÃO E ENTRADA DE DADOS

# Solicita um texto, retornando-o e exibindo uma mensagem personalizada.
def solicita_texto(_mensagem: str) -> str:
    texto = None
    while not texto:
        texto = str(input(_mensagem)).strip()
        if not texto:
            print("\nErro! Digite novamente.\n")
    return texto

# Solicita um número inteiro, retornando-o e exibindo uma mensagem personalizada.
def solicita_inteiro(_mensagem: str) -> int:
    inteiro = None
    while inteiro is None:
        try:
            inteiro = int(input(_mensagem).strip())
        except ValueError:
            print("\nErro! Digite um número válido.\n")
    return inteiro

# Solicita um número float, retornando-o e exibindo uma mensagem personalizada.
def solicita_float(_mensagem: str) -> float:
    valor = None
    while valor is None:
        try:
            valor = float(input(_mensagem).strip())
        except ValueError:
            print("\nErro! Digite um número válido.\n")
    return valor

# Solicita uma data, retornando-a e exibindo uma mensagem personalizada.
def solicita_data(_mensagem: str) -> str:
    data = None
    while data is None:
        data_str = str(input(_mensagem)).strip()
        if not data_str:
            print("\nErro! Digite novamente.\n")
            continue
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            print("\nErro! Digite uma data válida no formato DD/MM/AAAA.\n")
            data = None
    return data.strftime("%d/%m/%Y")

# Solicita 'S' ou 'N' e retorna True ou False e exibindo uma mensagem personalizada.
def solicita_sim_nao(_mensagem: str) -> bool:
    resp = ""
    while resp not in ["S", "N"]:
        resp = str(input(_mensagem)).strip().upper()
        if resp in ["S", "N"]:
            return resp[0] == "S"
        print("\nErro! Digite apenas S ou N.\n")
        continue

# Solicita um número inteiro que deve estar dentro de um intervalo específico e exibindo uma mensagem personalizada.
def solicita_inteiro_intervalo(_mensagem: str, _minimo: int, _maximo: int) -> int:
    valido = False
    while not valido:
        entrada = solicita_inteiro(_mensagem)
        if _minimo <= entrada <= _maximo:
            valido = True
        else:
            print(f"\nErro! Digite um número entre {_minimo} e {_maximo}.\n")
    return entrada


# -------------------- BANCO DE DADOS 

# Tenta criar uma conexão com o Oracle Database e retorna a conexão se bem-sucedida ou None se ocorrer algum erro.
def conexao_oracledb(_user: str, _password: str, _dsn: str) -> oracledb.Connection:
    try:
        conexao = oracledb.connect(
            user=_user,
            password=_password,
            dsn=_dsn
        )
        return conexao
    except Exception as e:
        print(f"Erro ao conectar com banco.\n\n{e}")
        return None

# Solicita os dados do veículo ao usuário e retorna um dicionário com todas as informações.
def solicita_dados_veiculos() -> dict:
    # Todos os dados
    tipo = solicita_texto("\nTipo do veículo: ")
    marca = solicita_texto("\nMarca: ")
    modelo = solicita_texto("\nModelo: ")
    ano_fabricacao = solicita_inteiro("\nAno de fabricação: ")
    placa = solicita_texto("\nPlaca ex(ABC1D23): ")
    cor = solicita_texto("\nCor: ")

    # Combustível
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
    opcao_combustivel = solicita_inteiro_intervalo(mensagem_combustivel, 1, 5)
    combustivel = tipos_combustivel[opcao_combustivel]

    # Quilometragem
    quilometragem = solicita_inteiro("\nQuilometragem: ")

    # Status
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
    opcao_status = solicita_inteiro_intervalo(mensagem_status, 1, 3)
    status = tipos_status[opcao_status]

    # Outros dados
    valor_diaria = solicita_float("\nValor da diária: ")
    data_aquisicao = solicita_data("\nData de aquisição do veículo (DD/MM/YYYY): ")

    # Cria o dicionário final
    dados = {
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

    return dados

# Insere um novo registro de veículo e retorna True se o cadastro for bem sucedido ou False em caso de erro.
def cadastrar_veiculo(_conexao: oracledb.Connection, _dados: dict) -> bool:
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
        cur.execute(comando_sql, _dados)
        _conexao.commit()
        cur.close()

        sucesso = True

    except Exception as e:
        print(f"\nErro no cadastro.\n\n{e}")

        sucesso = False
    
    return sucesso

# Busca e exibe uma lista resumida de veículos cadastrados no banco de dados.
def previa_dados_veiculo(_conexao: oracledb.Connection) -> str:
    cur = _conexao.cursor()
    cur.execute("""SELECT id_veiculo, modelo, placa, status FROM T_VEICULOS""")
    dados = cur.fetchall()
    cur.close()


    if not dados:
        print("Nenhum veículo encontrado.")
        return None
    
    dados = sorted(dados, key=lambda x: x[0])

    # Cabeçalhos das colunas
    colunas = ["ID", "Modelo", "Placa", "Status"]

    # Exibição formatada com tabulate
    tabela = tabulate(
    dados,
    headers=colunas,
    tablefmt="fancy_grid", # plain, grid, fancy_grid, github, psql, pipe, simple_outline
    numalign="right", # left, center, right
    stralign="right" # left, center, right
    )
    return tabela

# Retorna os dados completos de um veículo específico pelo ID formatados em tabela.
def dados_unicos(_conexao: oracledb.Connection, _id: int) -> str:
    cur = _conexao.cursor()
    comando_sql = """SELECT * FROM T_VEICULOS WHERE id_veiculo = :id_veiculo"""
    cur.execute(comando_sql, {"id_veiculo": _id})
    dados = cur.fetchall()
    cur.close()

    tabela = None

    if not dados:
        print("Nenhum veículo encontrado.")
        return tabela

    colunas = [
        "ID", "Tipo", "Marca", "Modelo", "Ano Fab.", "Placa", "Cor",
        "Combustível", "Km", "Status", "Valor Diária", "Data Aquisição"
    ]

    tabela = tabulate(
    dados,
    headers=colunas,
    tablefmt="fancy_grid", # plain, grid, fancy_grid, github, psql, pipe, simple_outline
    numalign="right", # left, center, right
    stralign="right" # left, center, right
    )
    return tabela

# Retorna todos os registros de veículos formatados em tabela.
def dados_inteiros(_conexao: oracledb.Connection, ) -> str:
    cur = _conexao.cursor()
    cur.execute("SELECT * FROM T_VEICULOS")
    dados = cur.fetchall()
    cur.close()

    tabela = None

    if not dados:
        print("Nenhum veículo encontrado.")
        return tabela

    colunas = [
        "ID", "Tipo", "Marca", "Modelo", "Ano Fab.", "Placa", "Cor",
        "Combustível", "Km", "Status", "Valor Diária", "Data Aquisição"
    ]

    tabela = tabulate(
    dados,
    headers=colunas,
    tablefmt="fancy_grid", # plain, grid, fancy_grid, github, psql, pipe, simple_outline
    numalign="right", # left, center, right
    stralign="right" # left, center, right
    )
    return tabela

# 
def alterar_dados(_conexao: oracledb.Connection, _dados: dict, _id_veiculo: int) -> bool:
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

        dados_bind = _dados.copy()
        dados_bind["id_veiculo"] = _id_veiculo

        cur = _conexao.cursor()
        cur.execute(comando_sql, dados_bind)
        _conexao.commit()
        cur.close()

        sucesso = True

    except Exception as e:
        print(f"\nErro no cadastro.\n\n{e}")
        sucesso = False
    
    return sucesso

# -------------------- PROGRAMA PRINCIPAL
try:
    user = "rm561833"
    password = "070406"
    dsn = "oracle.fiap.com.br:1521/ORCL"
    conn = conexao_oracledb(user, password, dsn)
    conectado = bool(conn)
except Exception as e:
    conectado = False

while conectado:
    limpa_tela()
    titulo_centralizado("LOCADORA DE VEÍCULOS",60)
    print("""
1. Registrar novo veículo
2. Consultar veículo
3. Listar todos os veículos
4. Atualizar informações
5. Remover veículo
6. Limpar todos os registros

7. Exportar para JSON
8. Exportar para CSV
9. Exportar para Excel

0. Sair
          """)
    escolha = solicita_inteiro_intervalo("Escolha: ", 0, 9)
    
    match escolha:
        case 0:
            limpa_tela()
            print("\nPrograma encerrado. Até logo!\n")
            conectado = False
        case 1:
            limpa_tela()
            titulo_centralizado("FICHA DE CADASTRO DE VEÍCULO LOCADORA", 60)
            dados_registros = solicita_dados_veiculos()
            sucesso = cadastrar_veiculo(conn, dados_registros)
            if sucesso:
                print("\nVeículo registrado com sucesso!")
                input("\nPrecione ENTER para continuar...")
            else:
                input("\nPrecione ENTER para continuar...")
        case 2:
            id_veiculo = -1  # inicializa com valor diferente de 0

            while id_veiculo != 0:
                limpa_tela()
                titulo_centralizado("CONSULTA DE VEÍCULO LOCADORA", 60)

                print("\nESCOLHA O ID DO VEÍCULO QUE DESEJA CONSULTAR:\n")

                previa_dados = previa_dados_veiculo(conn)

                if previa_dados:
                    print(previa_dados)
                print("\nDIGITE '0' PARA VOLTAR AO MENU PRINCIPAL\n")
                id_veiculo = solicita_inteiro("\nDigite o ID do veículo: ")
                
                if id_veiculo == 0:
                    continue
                
                todos_dados = dados_unicos(conn, id_veiculo)

                limpa_tela()
                titulo_centralizado("CONSULTA DE VEÍCULO LOCADORA", 60)

                if todos_dados:
                    print(todos_dados)
                else:
                    print("\nNenhum veículo encontrado com esse ID.\n")
                
                input("\nPrecione ENTER para continuar...")

        case 3:
            limpa_tela()
            titulo_centralizado("LISTA DE TODOS OS VEÍCULOS", 60)
            dados = dados_inteiros(conn)
            print(dados)
            input("\nPrecione ENTER para continuar...")
        case 4:
            id_veiculo = -1  # inicializa com valor diferente de 0

            while id_veiculo != 0:
                limpa_tela()
                titulo_centralizado("ATUALIZAR VEÍCULO LOCADORA", 60)

                print("\nESCOLHA O ID DO VEÍCULO QUE DESEJA CONSULTAR:\n")

                previa_dados = previa_dados_veiculo(conn)

                if previa_dados:
                    print(previa_dados)
                print("\nDIGITE '0' PARA VOLTAR AO MENU PRINCIPAL\n")
                id_veiculo = solicita_inteiro("\nDigite o ID do veículo: ")
                
                if id_veiculo == 0:
                    continue
                
                todos_dados = dados_unicos(conn, id_veiculo)

                limpa_tela()
                titulo_centralizado("ATUALIZAÇÃO DE VEÍCULO LOCADORA", 60)

                if todos_dados:
                    print("DADOS ATUAIS")
                    print(todos_dados)
                    print("\nDigite os novos dados do veículo:\n")
                    
                    # ✅ Aqui coleta os novos dados e passa o dicionário correto para a função
                    novos_dados = solicita_dados_veiculos()
                    alterar_dados(conn, novos_dados, id_veiculo)

                else:
                    print("\nNenhum veículo encontrado com esse ID.\n")
                
                input("\nPressione ENTER para continuar...")




        case 5:
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")
        case 6:
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")
        case 7:
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")
        case 8:
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")
        case 9:
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")