# Victor Alves Lopes RM561833
import os
import oracledb
import pandas as pd
from datetime import datetime

"""
CREATE TABLE T_VEICULOS (
    id_veiculo INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    modelo VARCHAR2(100),
    marca VARCHAR2(100),
    ano_fabricacao INT,
    valor_diaria FLOAT,
    data_aquisicao DATE
);
"""

def limpa_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def titulo_centralizado(_texto: str, _qtd_caracteres: int):
    # Exibe um título centralizado entre duas linhas decorativas "=-".
    print("=-" * (_qtd_caracteres // 2))
    print(_texto.center(_qtd_caracteres))
    print("=-" * (_qtd_caracteres // 2), "\n")

def solicita_texto(_mensagem: str) -> str:
    texto = ""
    while not texto:
        texto = str(input(_mensagem)).strip()
        if not texto:
            print("\nErro! Digite novamente.\n")
    
    return texto

def solicita_inteiro(_mensagem: str) -> int:
    inteiro_str = ""
    while not inteiro_str:
        inteiro_str = str(input(_mensagem)).strip()
        if not inteiro_str or not inteiro_str.isdigit():
            print("\nErro! Digite novamente.\n")
            inteiro_str = ""

    return int(inteiro_str)

def solicita_data(_mensagem: str) -> datetime:
    data_str = ""
    while not data_str:
        data_str = str(input(_mensagem)).strip()
        if not data_str:
            print("\nErro! Digite novamente.\n")
            continue
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")

        except ValueError:
            print("\nErro! Digite novamente.\n")
            data_str = ""

    return data.strftime("%d/%m/%Y")

def solicita_float(_mensagem: str) -> float:
    float_str = ""
    while not float_str:
        float_str = str(input(_mensagem)).strip()
        if not float_str or not float_str.isdigit():
            print("\nErro! Digite novamente.\n")
            float_str = ""

    return float(float_str)

def conexao_oracledb(_user: str, _password: str, _dsn: str) -> oracledb.Connection:
    # Conexão com banco de dados Oracle.
    try:
        conexao = oracledb.connect(
            user = _user,
            password = _password,
            dsn = _dsn
        )
        return conexao
    except oracledb.Error:
        return None


def cadastrar_veiculo(_conexao: oracledb.Connection):

    modelo = solicita_texto("Digite o modelo do veículo: ")
    marca = solicita_texto("Digite a marca do veículo: ")
    ano_fabricacao = solicita_inteiro("Digite o ano do veículo: ")
    valor_diaria = solicita_inteiro("Digite o valor da diária do veículo: ")
    data_aquisicao = solicita_data("Digite a data de aquisição do veículo (DD/MM/YYYY): ")


    comando_sql = f"""
INSERT INTO T_VEICULOS 
(modelo, marca, ano_fabricacao, valor_diaria, data_aquisicao)
VALUES 
('{modelo}', '{marca}', {ano_fabricacao}, {valor_diaria}, TO_DATE('{data_aquisicao}', 'DD/MM/YYYY'))
"""

    inst_cadastro = _conexao.cursor()
    inst_cadastro.execute(comando_sql)
    _conexao.commit() 

def pesquisar_veiculo(_conexao: oracledb.Connection):
    inst_consulta = _conexao.cursor()
    lista_dados = []

    previa_pesquisa(_conexao)
    
    print()
    id_veiculo = solicita_inteiro("Digite o id do veículo: ")
    print()

    comando_sql = f"""SELECT * FROM T_VEICULOS WHERE id_veiculo = {id_veiculo}"""

    inst_consulta.execute(comando_sql)
    data = inst_consulta.fetchall()

    for dt in data:
        lista_dados.append(dt)
    
    lista_dados = sorted(lista_dados)

    dados_df = pd.DataFrame.from_records(
        lista_dados,
        columns=['ID', 'Modelo', 'Marca', 'Ano', 'Diaria', 'Aquisição'],
        index='ID'  # se quiser usar a coluna ID como índice
    )


    if dados_df.empty:
        print(f"Não há um veículos cadastrados!")
    else:
        print(dados_df)

def listar_veiculos(_conexao):
    inst_consulta = _conexao.cursor()
    lista_dados = []

    comando_sql = f"""SELECT * FROM T_VEICULOS"""

    inst_consulta.execute(comando_sql)
    data = inst_consulta.fetchall()

    for dt in data:
        lista_dados.append(dt)
    
    lista_dados = sorted(lista_dados)

    dados_df = pd.DataFrame.from_records(
        lista_dados,
        columns=['ID', 'Modelo', 'Marca', 'Ano', 'Diaria', 'Aquisição'],
        index='ID'
    )


    if dados_df.empty:
        print(f"Não há um veículos cadastrados!")
    else:
        print(dados_df)

def previa_pesquisa(_conexao):
    inst_consulta = _conexao.cursor()
    lista_dados = []

    comando_sql = f"""SELECT id_veiculo, modelo FROM T_VEICULOS"""

    inst_consulta.execute(comando_sql)
    data = inst_consulta.fetchall()

    for dt in data:
        lista_dados.append(dt)
    
    lista_dados = sorted(lista_dados)

    dados_df = pd.DataFrame.from_records(
        lista_dados,
        columns=['ID', 'Modelo'],
        index='ID'
    )

    if dados_df.empty:
        print(f"Não há um veículos cadastrados!")
    else:
        print(dados_df)
#------------------------------------------

user = "rm561833"
password = "070406"
dsn = "oracle.fiap.com.br:1521/ORCL"

conn = conexao_oracledb(user, password, dsn)
conectado = bool(conn)

while conectado:
    limpa_tela()
    titulo_centralizado("LOCADORA",50)
    print("""0 - Sair 
1 - Cadastrar Veículo 
2 - Pesquisar Veículo
3 - Listar Todos os Veículos
""")
    escolha = solicita_inteiro("Escolha: ")

    match escolha:
        case 0:
            conectado = False
        case 1:
            limpa_tela()
            titulo_centralizado("CADASTRAR VEÍCULO",50)
            try:
                cadastrar_veiculo(conn)
            except oracledb.Error as e:
                print("Não foi possível completar a operação no banco de dados.")
                print(f"Detalhas do erro: {e}\n")
                input("Precione ENTER para voltar. ")
            else:
                print("Cadastro feito com sucesso.\n")
                input("Precione ENTER para voltar. ")
        case 2:
            limpa_tela()
            titulo_centralizado("PESQUISAR VEÍCULO ",50)
            pesquisar_veiculo(conn)
            input("\nPrecione ENTER para voltar. ")
        case 3:
            limpa_tela()
            titulo_centralizado("LISTA TODOS OS VEÍCULOS",50)
            listar_veiculos(conn)
            input("\nPrecione ENTER para voltar. ")