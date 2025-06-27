import sys

# Parâmetros para utilizar:
# Memória Cache
# Política de escrita: 0 - write-through e 1 - write-back;
# Tamanho da linha: deve ser potência de 2, em bytes;
# Número de linhas: deve ser potência de 2;
# Associatividade (número de linhas) por conjunto: deve ser potência de 2 (mínimo 1 e máximo igual ao número de linhas);
# Tempo de acesso quando encontra (hit time): em nanossegundos;
# Política de Substituição: LRU (Least Recently Used) ou Aleatória;
# Memória Principal
# Tempos de leitura/escrita: em nanossegundos.


def executa_script(parametros):
    endereco_operacoes = []
    with open(dic_parametros['arquivo'], 'r') as f:
        for linha in f:
            print(str(linha))

            linha = linha.strip()
            if not linha:
                continue
            endereco, operacao = linha.split()
            endereco_operacoes.append( (endereco, operacao) )
    
    print(f"Total de endereços lidos: {len(endereco_operacoes)}")




if __name__ == "__main__":
    parametros = sys.argv
    dic_parametros = {
        'arquivo': parametros[1],
        'politica_escrita': parametros[2],
        'tamanho_linha': parametros[3],
        'numero_linhas': parametros[4],
        'linhas_conjunto': parametros[5],
        'tempo_acesso': parametros[6],
        'politica_substituicao': parametros[7],
        'tempos_leitura': parametros[8] 
    }

    executa_script(dic_parametros)