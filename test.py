import os; os.system("cls")

def solicita_campos():
    campos_escolhidos = {
        1: "id_veiculo",
        2: "tipo",
        3: "marca",
        4: "modelo",
        5: "ano_fabricacao",
        6: "placa",
        7: "cor",
        8: "combustivel",
        9: "quilometragem",
        10: "status",
        11: "valor_diaria",
        12: "data_aquisicao"
    }

    print(""""Escolha os campo
    1. Id do veículo
    2. Tipo
    3. Marca
    4. Modelo
    5. Ano de fabricação
    6. Placa
    7. Cor
    8. Combustível
    9. Quilometragem
    10. Status
    11. Valor da diária
    12. Data de aquisição do veículo""")

    campos = []
    escolha = True
    while escolha:  
        escolha = int(input("\nESCOLHA (0 para sair): "))

        if escolha == 0:
            escolha = False
        else:
            if escolha in campos_escolhidos:
                campos.append(campos_escolhidos[escolha])

    campos = ', '.join(campos)

    return campos


flag = True
while flag:
    campos = solicita_campos()
    if not campos:
    

print(f"\nCampos selecionados:\n{campos}")

