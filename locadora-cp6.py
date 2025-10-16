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

def limpa_tela():
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

def solicita_data(_mensagem: str):
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

    cur = _conexao.cursor()

    modelo = solicita_texto("Digite o modelo do veículo: ")
    marca = solicita_texto("Digite a marca do veículo: ")
    ano_fabricacao = solicita_inteiro("Digite o ano do veículo: ")
    valor_diaria = solicita_inteiro("Digite o valor da diária do veículo: ")
    data_aquisicao = solicita_data("Digite a data de aquisição do veículo (DD/MM/YYYY): ")

    sql = """INSERT INTO T_VEICULOS (modelo, marca, ano_fabricacao, valor_diaria, data_aquisicao)
    VALUES (:modelo, :marca, :ano_fabricacao, :valor_diaria, :data_aquisicao)"""

    cur.execute(sql, {
        "modelo": modelo,
        "marca": marca,
        "ano_fabricacao": ano_fabricacao,
        "valor_diaria": valor_diaria,
        "data_aquisicao": data_aquisicao
    })

    _conexao.commit() 

def pesquisar_veiculo(_conexao: oracledb.Connection):
    cur = _conexao.cursor()
    lista_dados = []

    previa_pesquisa(_conexao)
    
    print()
    id_veiculo = solicita_inteiro("Digite o id do veículo: ")
    print()

    sql = f"""SELECT * FROM T_VEICULOS WHERE id_veiculo = :id_veiculo"""

    cur.execute(sql, {"id_veiculo": id_veiculo})
    data = cur.fetchall()

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
    cur = _conexao.cursor()
    lista_dados = []

    sql = f"""SELECT id_veiculo, modelo FROM T_VEICULOS"""

    cur.execute(sql)
    data = cur.fetchall()

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

def alterar_dados(_conexao: oracledb.Connection):
    try:
        cur = _conexao.cursor()

        lista_dados = []

        previa_pesquisa(_conexao)

        print()
        id_veiculo = solicita_inteiro("Digite o id do veículo: ")
        print()

        comando_sql = f"""SELECT * FROM T_VEICULOS WHERE id_veiculo = :id_veiculo"""

        cur.execute(comando_sql, {"id_veiculo": id_veiculo})
        data = cur.fetchall()

        for dt in data:
            lista_dados.append(dt)

        lista_dados = sorted(lista_dados)

        if len(lista_dados) == 0:
            print(f"Não há vaículo cadastrado com o ID = {id_veiculo}")
            input("Pressione ENTER")
        else:
            novo_modelo = solicita_texto("Digite o modelo do veículo: ")
            novo_marca = solicita_texto("Digite a marca do veículo: ")
            novo_ano_fabricacao = solicita_inteiro("Digite o ano do veículo: ")
            novo_valor_diaria = solicita_inteiro("Digite o valor da diária do veículo: ")
            novo_data_aquisicao = solicita_data("Digite a data de aquisição do veículo (DD/MM/YYYY): ")
        
        alteracao = f"""UPDATE T_VEICULOS 
                SET modelo = :modelo, 
                    marca = :marca, 
                    ano_fabricacao = :ano_fabricacao, 
                    valor_diaria = :valor_diaria, 
                    data_aquisicao = TO_DATE( :data_aquisicao, 'DD/MM/YYYY') 
                WHERE id_veiculo= :id_veiculo"""

        cur.execute(alteracao, {
            "modelo": novo_modelo,
            "marca": novo_marca,
            "ano_fabricacao": novo_ano_fabricacao,
            "valor_diaria": novo_valor_diaria,
            "data_aquisicao": novo_data_aquisicao,
            "id_veiculo": id_veiculo
        })

        _conexao.commit()
        print("\nRegistro ALTERADO!")
    except:
        print("\nErro na transação do BD")

def excluir_registros(_conexao: oracledb.Connection):
    try:
        cur = _conexao.cursor()

        lista_dados = []


        previa_pesquisa(_conexao)

        print()
        id_veiculo = solicita_inteiro("Digite o id do veículo: ")
        print()

        comando_sql = f"""SELECT * FROM T_VEICULOS WHERE id_veiculo = :id_veiculo"""

        cur.execute(comando_sql, {"id_veiculo": id_veiculo})
        data = cur.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados) == 0:
            print(f"Não há um veículo cadastrado com ID = {id_veiculo}")
        else:
            comando_sql_delete = f"""DELETE FROM t_veiculos WHERE id_veiculo= :id_veiculo"""

            cur.execute(comando_sql_delete, {"id_veiculo": id_veiculo})
            _conexao.commit()
            print("Registro APAGADO!")
    except: 
        print("\nErro na transação do BD")

#-------------- MENU --------------

user = "rm561833"
password = "070406"
dsn = "oracle.fiap.com.br:1521/ORCL"

conn = conexao_oracledb(user, password, dsn)
conectado = bool(conn)

while conectado:
    limpa_tela()
    titulo_centralizado("LOCADORA",50)
    print("""1 - Cadastrar Veículo 
2 - Pesquisar Veículo
3 - Listar Todos os Veículos
4 - Alterar Dados
5 - Excluir um Registro
6 - Excluir Todos os Dados 
          
0 - Sair 
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
                print("\nNão foi possível completar a operação no banco de dados.")
                print(f"\nDetalhas do erro: {e}")
                input("\nPrecione ENTER para voltar. ")
            else:
                print("\nCadastro feito com sucesso.\n")
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
        case 4:
            limpa_tela()
            titulo_centralizado("ALTERAR DADOS",50)
            alterar_dados(conn)
            input("\nPrecione ENTER para voltar. ")
        case 5:
            limpa_tela()
            titulo_centralizado("EXCLUIR REGISTROS",50)
            excluir_registros(conn)
            input("\nPrecione ENTER para voltar. ")
        case 6:
            limpa_tela()
            titulo_centralizado("EXCLUIR TODOS OS DADOS",50)
            print("Em manutenção...")
            input("\nPrecione ENTER para voltar. ")
