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
        return e 
    
    # formatar onde vai ser usado, se retornar um erro faça oq quiser com ele, se retornar a conexão continar o codigo