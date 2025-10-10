# Victor Alves Lopes RM561833
import os
import oracledb
import pandas as pd
import datetime

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

#def conexao_oracledb() -> oracledb.Connection:
    

def cadastrar_veiculo():
    print("=-=-=-=-= Cadastrar Veículo =-=-=-=-=")
    id = int(input("Id: "))
    modelo = str(input("Modelo: "))
    marca = str(input("Marca: "))
    ano_fabricacao = int(input("Ano de frabricação: "))
    valor_diaria = float(input("Valor da diária: "))
    data_aquisicao = datetime(input("Data de aquisição: "))

    instrucao_sql = f""" INSERT INTO T_VEICULOS (modelo, marca, ano_fabricacao, valor_diaria,data_aquisicao)VALUES ('{id}', '{modelo}', {marca}), '{ano_fabricacao}', '{valor_diaria}', '{data_aquisicao}' """



while True:
    limpa_tela()
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                LOCADORA 
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

0 - Sair 
1 - Cadastrar Veículo 
2 - Pesquisar Veículo
3 - Listar Todos os Veículos
""")
    escolha = input("\tEscolha: _ ")

    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 6
    
    match escolha:
        case 1:
            ... 
        case 2:
            ...
        case 3:
            ...