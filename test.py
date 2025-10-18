# Victor Alves Lopes RM561833

# Orientação para que o código funcione:
    # 1. Copie o comando SQL e execute no seu banco de dados.
    # 2. Faça o download das bibliotecas necessárias para que o código funcione no seu terminal.
        # pip install oracledb
        # pip install pandas

import os
import oracledb
import pandas as pd
from datetime import datetime

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
            ...
        case 3:
            ...
        case 4:
            ...
        case 5:
            ...
        case 6:
            ...
        case 7:
            ...
        case 8:
            ...
        case 9:
            ...