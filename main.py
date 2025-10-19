import json
import os

# -------------------- SUBALGORITMOS --------------------


# -------------------- APRESENTAÇÃO --------------------

def limpa_tela():
    # Limpa o terinal
    os.system("cls" if os.name == "nt" else "clear")

def imprime_linha_separadora(simbolo: str, quantidade: int):
    # Imprime uma simbolo separador.
    print(f"{simbolo * quantidade}")

def imprime_titulo_centralizado(titulo: str, largura: int):
    # Imprime um título centralizado com bordas.
    print("=-" * largura)
    print(titulo.center(largura * 2))
    print("=-" * largura)


# -------------------- VALIDAÇÃO E ENTRADA DE DADOS --------------------

def pede_numero_inteiro(mensagem: str) -> int:
    # Solicita e retorna um número inteiro válido.
    while True:
        entrada = str(input(mensagem)).strip()
        if not entrada:
            print("Entrada vazia. Tente novamente.")
            continue
        try:
            return int(entrada)
        except ValueError:
            print("Digite apenas números inteiros.")

def pede_texto_obrigatorio(mensagem: str) -> str:
    # Solicita e retorna um texto (string) não vazio.
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        
def obtem_confirmacao_sim_nao(mensagem: str) -> bool:
    # Solicita 'S' ou 'N' e retorna True ou False.
    while True:
        entrada = input(f"{mensagem}").strip().upper()
        if entrada[0] in ["S", "N"]:
            return entrada[0] == "S" # se for "N" retorna false
        print("Responda com 'S' para sim ou 'N' para não.")

def pede_opcao_intervalo(mensagem: str, minimo: int, maximo: int) -> int:
    #Solicita um número dentro de um intervalo (minimo, maximo).
    while True:
        entrada = str(input(mensagem)).strip()
        if not entrada:
            print("Entrada vazia. Tente novamente.")
            continue
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Erro! digite {minimo} à {maximo}.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")


# ----------------- COLETA DE DADOS ESPECÍFICOS -----------------

def coleta_sexo() -> str:
    # Retorna o sexo ('M' ou 'F').
    while True:
        entrada = input("\nSexo: (M/F) ").strip().upper()
        if entrada[0] in ["M", "F"]:
            return entrada[0]
        print("Responda com 'M' para Masculino ou 'F' para Feminino.")

def coleta_tipo_login() -> str:
    # Retorna o tipo de login ('gov' ou 'etiqueta')
    mensagem = """
Tipo login:
1 -> Gov
2 -> Etiqueta
Escolha: """
    escolha = pede_opcao_intervalo(mensagem, 1, 2)
    if escolha == 1:
        return "gov"
    elif escolha == 2:
        return "etiqueta"

def coleta_dados_ajuda() -> dict:
    #Retorna dados sobre necessidade, momento e problema de ajuda.
    if obtem_confirmacao_sim_nao("\nPrecisou de ajuda? [S/N] "):
        momento_opc = pede_opcao_intervalo("1 -> Antes do login\n2 -> Depois do login\nEscolha: ", 1, 2)
        momento = "antes login" if momento_opc == 1 else "depois login"

        mensagem_problema = """
Onde ocorreu o problema?
1 -> Login
2 -> Consulta
3 -> Agenda
4 -> Outros
Escolha: """
        problema_opc = pede_opcao_intervalo(mensagem_problema, 1, 4)
        problemas_tipo = {1: "login", 2: "consulta", 3: "agenda", 4: "outros"}

        return {"precisou": True, "momento": momento, "problema": problemas_tipo[problema_opc]}
    else:
        return {"precisou": False}


def coleta_especialidade() -> str:
    # Retorna a especialidade escolhida pelo usuário.
    mensagem = """
Escolha a especialidade:
1 -> Cardiologia
2 -> Neurologia
3 -> Oncologia
4 -> Ortopedia
Escolha: """
    opcao = pede_opcao_intervalo(mensagem, 1, 4)
    especialidade = {1: "cardiologia", 2: "neurologia", 3: "oncologia", 4: "ortopedia"}
    return especialidade[opcao]


def coleta_sucesso() -> bool:
    #Retorna True/False se houve sucesso na marcação.
    return obtem_confirmacao_sim_nao("\nTeve sucesso? [S/N]: ")


# ----------------- CENTRAL DE COLETA DE DADOS GERAIS -----------------

def coleta_dados_de_usuario(nome_arquivo: str) -> dict:
    # Coleta todos os dados do usuário para o Dashboard.
    id_usuario = gera_id_usuario(nome_arquivo)
    print(f"ID: {id_usuario}")

    # Coleta de dados
    nome = pede_texto_obrigatorio("\nNome do usuário: ")
    idade = pede_numero_inteiro("\nIdade do usuário: ")
    sexo = coleta_sexo()
    tipo_login = coleta_tipo_login()
    ajuda = coleta_dados_ajuda()
    especialidade = coleta_especialidade()
    sucesso = coleta_sucesso()
    satisfacao = pede_opcao_intervalo("\nSatisfação do usuário 1-5: ", 1, 5)
    tempo_uso = pede_numero_inteiro("\nTempo de uso no app (minutos): ")
    tempo_login = pede_numero_inteiro("\nTempo de login no app (minutos): ")
    absenteismo = obtem_confirmacao_sim_nao("\nAbsenteísmo? [S/N]: ")

    return {
        "id_usuario": id_usuario,
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "tipo_login": tipo_login,
        "ajuda": ajuda,
        "especialidade": {
            "especialidade": especialidade,
            "sucesso": sucesso
        },

        "satisfacao": satisfacao,
        "tempo_uso": tempo_uso,
        "tempo_login": tempo_login,
        "absenteismo": absenteismo
    }


def formata_dados_para_salvar(nome_arquivo: str) -> dict:
    # Formata os coleta_dados_de_usuario com o ID do usuário sendo a chave principal.
    dados_coletados = coleta_dados_de_usuario(nome_arquivo)
    id_str = str(dados_coletados["id_usuario"])
    return {id_str: dados_coletados}

# ----------------- GERENCIAMENTO JSON -----------------

def gera_id_usuario(nome_arquivo: str) -> int:
    # Retorna o próximo ID disponível no arquivo JSON.
    dados = carrega_dados_json(nome_arquivo)
    if not dados:
        return 1

    """ids = []
    for chave in dados.keys():
        ids.append(int(chave))"""
    
    ids = [int(chave) for chave in dados.keys()]
    return max(ids) + 1  # pega o maior número e adiciona 1.

def carrega_dados_json(nome_arquivo: str) -> dict:
    # Lê um arquivo JSON e retorna seu conteúdo. Retorna {} se não existir ou inválido.
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salva_dados_json(nome_arquivo: str, novo_dado: dict):
    # Adiciona / atualiza o novo dado no JSON e salva o arquivo.
    dados_atuais = carrega_dados_json(nome_arquivo)
    dados_atuais.update(novo_dado)
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_atuais, f, indent=4, ensure_ascii=False)
    input("\nDados Registrados com sucesso!!\nEnter Para voltar pro menu...")

# ----------------- CÁLCULO DE MÉTRICAS -----------------

def calcula_metricas(dados: dict) -> dict:
    #Calcula todas as métricas percentuais, médias e totais. Retorna valores numéricos.
    total_usuarios = len(dados)
    if total_usuarios == 0:
        return {}

    # Contadores e somas
    soma_satisfacao = 0
    soma_tempo_uso = 0
    soma_tempo_login = 0
    total_sucesso = 0
    total_absenteismo = 0
    ajuda_total = 0
    ajuda_antes = 0
    ajuda_depois = 0
    genero = {"M": 0, "F": 0}
    login = {"gov": 0, "etiqueta": 0}
    problemas = {"login": 0, "consulta": 0, "agenda": 0, "outros": 0}
    

    for usuario in dados.values():
        # Somas
        soma_satisfacao += usuario.get("satisfacao", 0)
        soma_tempo_uso += usuario.get("tempo_uso", 0)
        soma_tempo_login += usuario.get("tempo_login", 0)
        # Soma os valores de cada usuário, usando 0 como padrão caso o dado não exista.
        
        # Sucesso
        esp_data = usuario.get("especialidade", {})
        if isinstance(esp_data, dict) and esp_data.get("sucesso", False):
            total_sucesso += 1

        # Absenteísmo
        if usuario.get("absenteismo", False):
            total_absenteismo += 1

        # Gênero e Login
        sexo = usuario.get("sexo", "").upper()
        if sexo in genero:
            genero[sexo] += 1
        tipo_login = usuario.get("tipo_login", "").lower()
        if tipo_login in login:
            login[tipo_login] += 1

        # Ajuda e Problemas
        ajuda = usuario.get("ajuda", {})
        if ajuda.get("precisou", False) and "problema" in ajuda:
            ajuda_total += 1
            momento = ajuda.get("momento")
            if momento == "antes login":
                ajuda_antes += 1
            elif momento == "depois login":
                ajuda_depois += 1
            problema = ajuda.get("problema")
            if problema in problemas:
                problemas[problema] += 1

    # Cálculos finais de percentuais e médias
    metricas = {
    "total_usuarios": total_usuarios,
    "taxa_sucesso": round((total_sucesso / total_usuarios) * 100, 1),
    "satisfacao_media": round(soma_satisfacao / total_usuarios, 1), 
    "taxa_absenteismo": round((total_absenteismo / total_usuarios) * 100, 1),
    "tempo_medio_login": round(soma_tempo_login / total_usuarios, 1),
    "tempo_medio_uso": round(soma_tempo_uso / total_usuarios, 1),
    
    "genero_m_pct": round((genero["M"] / total_usuarios) * 100),
    "genero_f_pct": round((genero["F"] / total_usuarios) * 100),
    "login_gov_pct": round((login["gov"] / total_usuarios) * 100),
    "login_etiqueta_pct": round((login["etiqueta"] / total_usuarios) * 100),
    
    "taxa_ajuda": round((ajuda_total / total_usuarios) * 100, 1),  
    "ajuda_antes_pct": round((ajuda_antes / ajuda_total) * 100) if ajuda_total else 0,  
    "ajuda_depois_pct": round((ajuda_depois / ajuda_total) * 100) if ajuda_total else 0,
    
    "problemas_pct": {k: round((v / ajuda_total) * 100) for k, v in problemas.items()},
    }
    
    return metricas


# ----------------- FORMATAÇÃO (PREPARAÇÃO DE EXIBIÇÃO) -----------------

def formata_metricas_para_dashboard(metricas: dict, dados_brutos: dict) -> dict:
    # Formata os valores numéricos das metricas em strings para impressão.
    
    # Formata problemas
    problemas_formatados = {
        k.capitalize(): f"[ {v}% ]" 
        for k, v in metricas.get("problemas_pct", {}).items()
    }

    # Monta especialidades formatadas para exibição
    especialidades_formatadas = {}
    for usuario in dados_brutos.values():
        esp_data = usuario.get("especialidade")
        # Corrige registros antigos
        if isinstance(esp_data, str):
            esp_data = {"especialidade": esp_data, "sucesso": False}
        elif esp_data is None:
            esp_data = {"especialidade": None, "sucesso": False}

        esp = esp_data.get("especialidade")
        sucesso = esp_data.get("sucesso", False)
        if not esp:
            continue
        if esp not in especialidades_formatadas:
            especialidades_formatadas[esp] = {"volume": 0, "taxa": 0}
        especialidades_formatadas[esp]["volume"] += 1
        if sucesso:
            especialidades_formatadas[esp]["taxa"] += 1

    # Converte taxa em percentual
    for esp in especialidades_formatadas:
        vol = especialidades_formatadas[esp]["volume"]
        suc = especialidades_formatadas[esp]["taxa"]
        especialidades_formatadas[esp]["taxa"] = f"[ {round((suc/vol)*100)}% ]"

    return {
        # Metricas gerais
        "sucesso": f"[ {metricas['taxa_sucesso']}% ]",
        "satisfacao": f"[ {metricas['satisfacao_media']} / 5.0 ]",
        "tempo_login": f"[ {metricas['tempo_medio_login']} min ]",
        "tempo_uso": f" [ {metricas['tempo_medio_uso']} min ]",
        "total_usuarios": f"[ {metricas['total_usuarios']} ]",
        "absenteismo": f" [ {metricas['taxa_absenteismo']}% ]",
        
        # Demografia e Login
        "genero_f": f"[ {metricas['genero_f_pct']}% ]",
        "genero_m": f"[ {metricas['genero_m_pct']}% ]",
        "login_gov": f"[ {metricas['login_gov_pct']}% ]",
        "login_etiqueta": f" [ {metricas['login_etiqueta_pct']}% ]",
        
        # Ajuda e Erros
        "ajuda_pct": f"[ {metricas['taxa_ajuda']}% ]",
        "ajuda_antes": f"[ {metricas['ajuda_antes_pct']}% ]",
        "ajuda_depois": f"[ {metricas['ajuda_depois_pct']}% ]",
        "problemas": problemas_formatados,
        
        # Especialidade 
        "especialidades": especialidades_formatadas
    }


# ----------------- IMPRESSÃO (EXIBIÇÃO) -----------------

def imprime_par_alinhado(
    rotulo_esquerdo: str,
    valor_esquerdo: str,
    largura_rotulo: int,
    largura_valor: int,
    rotulo_direito: str = "",
    valor_direito: str = "") -> None:

    #Imprime uma ou duas métricas lado a lado com alinhamento fixo.
    linha = f"{rotulo_esquerdo:<{largura_rotulo}} {valor_esquerdo:<{largura_valor}}"
    
    # Se rotulo_direito e valor_direito forem informados, adiciona o segundo par na mesma linha
    if rotulo_direito and valor_direito:
        linha += f"| {rotulo_direito:<{largura_rotulo}} {valor_direito}"
    print(linha)

def imprime_dashboard(metricas_formatadas: dict) -> None:
    #Imprime o dashboard formatado no terminal com alinhamento corrigido.
    
    # larguras fixas para alinhamento
    largura_campo = 20
    largura_valor = 15

    imprime_titulo_centralizado("Dashboard de Dados Registrados", 40)

    print("\n\n\n----- Métricas Gerais -----")
    imprime_par_alinhado("\nTaxa de Sucesso", metricas_formatadas['sucesso'], largura_campo+1, largura_valor, 
                         "Satisfação Média", metricas_formatadas['satisfacao'])
    imprime_par_alinhado("Tempo Médio Login", metricas_formatadas['tempo_login'], largura_campo, largura_valor, 
                         "Tempo Médio Uso", metricas_formatadas['tempo_uso'])
    imprime_par_alinhado("Total de Usuários", metricas_formatadas['total_usuarios'], largura_campo, largura_valor, 
                         "Taxa de Absenteísmo", metricas_formatadas['absenteismo'])

    print("\n\n\n----- Demografia e Login -----")
    imprime_par_alinhado("\nGênero Feminino (F)", metricas_formatadas['genero_f'], largura_campo + 1, largura_valor, 
                         "Gênero Masculino (M)", metricas_formatadas['genero_m'])
    imprime_par_alinhado("Login Gov", metricas_formatadas['login_gov'], largura_campo, largura_valor, 
                         "Login Etiqueta", metricas_formatadas['login_etiqueta'])

    print("\n\n\n----- Ajuda e Erros -----")
    print(f"\n{'Necessidade de Ajuda':<{largura_campo}} {metricas_formatadas['ajuda_pct']}")
    imprime_par_alinhado("Ajuda Antes Login", metricas_formatadas['ajuda_antes'], largura_campo, largura_valor, 
                         "Ajuda Depois Login", metricas_formatadas['ajuda_depois'])
    
    print("\nDistribuição dos Problemas:")
    problemas_list = list(metricas_formatadas["problemas"].items())
    
    # imprime dois problemas por linha
    largura_problema = 20
    for i in range(0, len(problemas_list), 2):
        p1, v1 = problemas_list[i]
        linha = f"   - {p1:<{largura_problema}} {v1:<9}"
        
        if i + 1 < len(problemas_list):
            p2, v2 = problemas_list[i+1]
            linha += f" |    - {p2:<{largura_problema}} {v2:<9}"
        print(linha)

    print("\n\n\n----- Desempenho por Especialidade -----\n")
    
    # tabela de especialidades
    largura_col_esp = 25
    largura_col_vol = 10
    largura_col_suc = 16
    
    print(f"{'Especialidade':<{largura_col_esp}} | {'Volume':<{largura_col_vol}} | {'Taxa de Sucesso':<{largura_col_suc}}")
    print("-" * (largura_col_esp+1) + "|" + "-" * (largura_col_vol+2) + "|" + "-" * (largura_col_suc+1))
    
    for esp, data in metricas_formatadas["especialidades"].items():
        print(f"{esp:<{largura_col_esp}} | {data['volume']:<{largura_col_vol}} | {data['taxa']:<{largura_col_suc}}")
    
    print()
    imprime_linha_separadora("=-", 45)
    input("\nPressione Enter para voltar ao menu...")


def mostra_dashboard(nome_arquivo: str) -> None:
    # Comanda o cálculo, a formatação e a impressão do Dashboard.
    dados_brutos = carrega_dados_json(nome_arquivo)
    
    if not dados_brutos:
        imprime_titulo_centralizado("Dashboard de Dados Registrados", 40)
        print("\nNenhum dado encontrado. Adicione registros primeiro.\n")
        input("Pressione Enter para voltar ao menu...")
        return

    # 1. CÁLCULO
    metricas_numericos = calcula_metricas(dados_brutos)
    
    if not metricas_numericos:
        print("Nenhum dado para calcular indicadores.")
        return
        
    # 2. FORMATAÇÃO
    metricas_formatados = formata_metricas_para_dashboard(metricas_numericos, dados_brutos)
    
    # 3. IMPRESSÃO
    imprime_dashboard(metricas_formatados)


# ----------------- REMOÇÃO E ADIÇÃO -----------------

def exibe_registro_detalhado(id_usuario: str, dados_usuario: dict, numerado: bool = False)-> None:
    # Exibe os dados detalhados de um único usuário.
    largura = 20
    linhas = []

    linhas.append(("ID:", id_usuario))
    linhas.append(("Nome:", dados_usuario["nome"].title()))
    linhas.append(("Idade:", dados_usuario["idade"]))
    linhas.append(("Sexo:", dados_usuario["sexo"].upper()))
    linhas.append(("Tipo do Login:", dados_usuario["tipo_login"].capitalize()))

    # Seção Ajuda
    linhas.append(("--- Ajuda ---", ""))
    ajuda = dados_usuario.get("ajuda", {})
    linhas.append(("Precisou:", str(ajuda.get("precisou", False)).capitalize()))
    
    if ajuda.get("precisou", False):
        linhas.append(("Momento:", ajuda.get("momento", "-").capitalize()))
        linhas.append(("Problema:", ajuda.get("problema", "-").capitalize()))

    # Especialidade
    linhas.append(("--- Especialidade ---", ""))
    especialidade = dados_usuario.get("especialidade", {})

    if isinstance(especialidade, str):
        especialidade = {"especialidade": especialidade, "sucesso": False}
    linhas.append(("Especialidade:", especialidade.get("especialidade", "-").capitalize()))
    linhas.append(("Sucesso:", str(especialidade.get("sucesso", False)).capitalize()))

    # Outros campos
    linhas.append(("--- Outros ---", ""))
    linhas.append(("Satisfação:", dados_usuario["satisfacao"]))
    linhas.append(("Tempo de Uso:", f"{dados_usuario['tempo_uso']} minutos"))
    linhas.append(("Tempo de Login:", f"{dados_usuario['tempo_login']} minutos"))
    linhas.append(("Absenteísmo:", str(dados_usuario["absenteismo"]).capitalize()))

    # Impressão formatada
    numero = 1
    for campo, valor in linhas:
        if campo.startswith("---"):
            print(f"\n{'':<4}{campo.replace('-', '').strip()}")
        else:
            if numerado:
                print(f"{numero:2} - {campo:<{largura}} {valor}")
                numero += 1
            else:
                print(f"{campo:<{largura}} {valor}")

def remove_registro(nome_arquivo: str):
    dados = carrega_dados_json(nome_arquivo)

    if not dados:
        input("Não há registros para excluir.\nPressione Enter para continuar...")
        return

    print("Registros disponíveis:\n")
    print("ID           | NOME")
    imprime_linha_separadora("=-", 26)
    for k, v in dados.items():
        print(f"{k:12} | {v.get('nome','')}")

    print("\n0. Cancelar e sair.")
    id_para_excluir = str(pede_numero_inteiro("\nDigite o ID do usuário a ser excluído: "))

    if id_para_excluir == "0":
        return

    if id_para_excluir in dados:
        limpa_tela()
        print("\n--- REGISTRO A SER EXCLUÍDO ---\n")

        usuario_para_excluir = dados[id_para_excluir]
        exibe_registro_detalhado(id_para_excluir, usuario_para_excluir, numerado=True)
        print("\n" + "-" * 40 + "\n")

        confirmacao = obtem_confirmacao_sim_nao(
            f"\nDeseja excluir cadastro do usuário {usuario_para_excluir.get('nome')}? [S/N]: "
        )
        if confirmacao:
            del dados[id_para_excluir]
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            input("Registro excluído com sucesso!\nPressione Enter para continuar...")
        else:
            input("Exclusão cancelada.\nPressione Enter para continuar...")
    else:
        input("\nID não encontrado.\nPressione Enter para continuar...")

def edita_registro(nome_arquivo: str)-> None:
    #Permite editar campos de um registro existente.
    dados = carrega_dados_json(nome_arquivo)

    if not dados:
        input("Não há registros para editar.\n\nPressione Enter para continuar...")
        return

    print("Registros disponíveis:\n")
    print("ID            | NOME")
    imprime_linha_separadora("=-", 26)
    for k, v in dados.items():
        print(f"{k:12} | {v.get('nome','')}")
    print("\n0. Cancelar e sair.")
    
    id_escolhido = str(pede_numero_inteiro("\nDigite o ID do usuário a ser editado: "))
    if id_escolhido == "0":
        return

    if id_escolhido not in dados:
        input("\nID não encontrado.\n\nPressione Enter para continuar...")
        return

    usuario = dados[id_escolhido]

    while True:
        limpa_tela()
        print(f"\n--- EDITANDO REGISTRO: {usuario.get('nome','')} ---\n")
        exibe_registro_detalhado(id_escolhido, usuario, numerado=True)

        print("\n0 - Voltar")
        escolha = pede_opcao_intervalo("\nEscolha o número do campo para editar: ", 0, 14)

        if escolha == 0:
            break

        match escolha:
            case 1:  # ID
                print("ID não pode ser alterado!")
            case 2:  # Nome
                usuario["nome"] = pede_texto_obrigatorio("Novo Nome: ")
            case 3:  # Idade
                usuario["idade"] = pede_numero_inteiro("Nova Idade: ")
            case 4:  # Sexo
                usuario["sexo"] = coleta_sexo()
            case 5:  # Tipo do Login
                usuario["tipo_login"] = coleta_tipo_login()
            case 6:  # Precisou de ajuda
                usuario["ajuda"]["precisou"] = obtem_confirmacao_sim_nao("Precisou de ajuda? [S/N]: ")
            case 7:  # Momento da ajuda
                if usuario["ajuda"].get("precisou", False):
                    mensagem = " 1 -> Antes do login\n 2 -> Depois do login\nEscolha: "
                    opc = pede_opcao_intervalo(mensagem, 1, 2)
                    usuario["ajuda"]["momento"] = "antes login" if opc == 1 else "depois login"
            case 8:  # Problema
                if usuario["ajuda"].get("precisou", False):
                    mensagem = " 1 -> Login\n 2 -> Consulta\n 3 -> Agenda\n 4 -> Outros\nEscolha: "
                    opc = pede_opcao_intervalo(mensagem, 1, 4)
                    usuario["ajuda"]["problema"] = {1:"login",2:"consulta",3:"agenda",4:"outros"}[opc]
                else:
                    input("O usuário não precisou de ajuda. Pressione Enter para continuar...")
            case 9:  # Especialidade
                mensagem = " 1 -> Cardiologia\n 2 -> Neurologia\n 3 -> Oncologia\n 4 -> Ortopedia\nEscolha: "
                opc = pede_opcao_intervalo(mensagem, 1, 4)
                usuario.setdefault("especialidade", {}) # Cria chave com valor padrão se não existir
                usuario["especialidade"]["especialidade"] = {1:"cardiologia",2:"neurologia",3:"oncologia",4:"ortopedia"}[opc]
            case 10:  # Sucesso da especialidade
                usuario.setdefault("especialidade", {}) # Cria chave com valor padrão se não existir
                usuario["especialidade"]["sucesso"] = obtem_confirmacao_sim_nao("Sucesso? [S/N]: ")
            case 11:  # Satisfação
                usuario["satisfacao"] = pede_opcao_intervalo("Nova Satisfação 1-5: ", 1, 5)
            case 12:  # Tempo de Uso
                usuario["tempo_uso"] = pede_numero_inteiro("Novo Tempo de Uso (minutos): ")
            case 13:  # Tempo de Login
                usuario["tempo_login"] = pede_numero_inteiro("Novo Tempo de Login (minutos): ")
            case 14:  # Absenteísmo
                usuario["absenteismo"] = obtem_confirmacao_sim_nao("Absenteísmo? [S/N]: ")
            case _:
                input("Opção inválida. Pressione Enter para continuar...")

        # Atualiza e salva o JSON
        dados[id_escolhido] = usuario
        salva_dados_json(nome_arquivo, {id_escolhido: usuario})


# ----------------- PROGRAMA PRINCIPAL -----------------

dados_usuario = {}
arquivo = "dados_usuario.json"
while True:
    limpa_tela()
    imprime_titulo_centralizado("AXCESS TECH", 30)
    print()

    print("1. Adicionar Novo Registro")
    print("2. Visualizar Dashboard")
    print("3. Editar dados")
    print("4. Excluir registros")
    print("0. Sair do Sistema")
    print()
    escolha = pede_opcao_intervalo("Escolha: ",0,4)

    match escolha:
        case 1:
            limpa_tela()
            dados_usuario = formata_dados_para_salvar(arquivo)
            salva_dados_json(arquivo, dados_usuario)

        case 2:
            limpa_tela()
            mostra_dashboard(arquivo)
            
        case 3:
            limpa_tela()
            edita_registro(arquivo)
        case 4:
            limpa_tela()
            remove_registro(arquivo)
        case 0:
            print("\nEncerrando programa...")
            break
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
def alterar_dados(_conexao: oracledb.Connection, _dados: dict, _id: int) -> bool:
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
        WHERE id_veiculo = :=_id
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
                    # sair naturalmente do loop
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
            limpa_tela()
            print("\nEm manutenção\n")
            input("\nPrecione ENTER para continuar...")
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