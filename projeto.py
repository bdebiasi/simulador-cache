import sys
import random

class LinhaCache:
    def __init__(self):
        self.tag = None
        self.valido = False
        self.dirty = False
        self.lru = 0

class ConjuntoCache:
    def __init__(self, linhas_por_conjunto):
        self.linhas = [LinhaCache() for _ in range(linhas_por_conjunto)]

class MemoriaCache:
    def __init__(self, params):
        self.num_linhas = int(params['numero_linhas'])
        self.associatividade = int(params['linhas_conjunto'])
        self.num_conjuntos = self.num_linhas // self.associatividade
        self.tamanho_linha = int(params['tamanho_linha'])
        self.hit_time = int(params['tempo_acesso'])
        self.politica_escrita = int(params['politica_escrita'])  
        self.politica_subs = params['politica_substituicao'].upper() 
        self.tempo_mp = int(params['tempos_leitura'])
        self.conjuntos = [ConjuntoCache(self.associatividade) for _ in range(self.num_conjuntos)]
        self.clock = 0

        self.total_lidas = 0
        self.total_escritas = 0
        self.hit_leituras = 0
        self.hit_escritas = 0
        self.miss_leituras = 0
        self.miss_escritas = 0
        self.escritas_mp = 0
        self.leituras_mp = 0

    def acessar_cache(self, endereco_hex, operacao):
        endereco = int(endereco_hex, 16)
        offset_bits = self.tamanho_linha.bit_length() - 1
        index_bits = self.num_conjuntos.bit_length() - 1

        index = (endereco >> offset_bits) & ((1 << index_bits) - 1)
        tag = endereco >> (offset_bits + index_bits)

        conjunto = self.conjuntos[index]

        for i, linha in enumerate(conjunto.linhas):
            if linha.valido and linha.tag == tag:
                linha.lru = self.clock
                if operacao == 'R':
                    self.total_lidas += 1
                    self.hit_leituras += 1
                else:
                    self.total_escritas += 1
                    self.hit_escritas += 1
                    if self.politica_escrita == 1: 
                        linha.dirty = True
                    else:  
                        self.escritas_mp += 1
                return True

        if operacao == 'R':
            self.total_lidas += 1
            self.miss_leituras += 1
            self.leituras_mp += 1
        else:
            self.total_escritas += 1
            self.miss_escritas += 1
            if self.politica_escrita == 0:
                self.escritas_mp += 1  
            else:
                self.leituras_mp += 1  

        linha_substituir = None
        if self.politica_subs == 'LRU':
            linha_substituir = min(conjunto.linhas, key=lambda l: l.lru if l.valido else -1)
        else:
            linha_substituir = random.choice(conjunto.linhas)

        if linha_substituir.valido and linha_substituir.dirty:
            self.escritas_mp += 1

        linha_substituir.tag = tag
        linha_substituir.valido = True
        linha_substituir.dirty = (operacao == 'W' and self.politica_escrita == 1)
        linha_substituir.lru = self.clock

        return False

    def simular(self, operacoes):
        for endereco, operacao in operacoes:
            self.clock += 1
            self.acessar_cache(endereco, operacao)

    def relatorio(self, params):
        total_acessos = self.total_lidas + self.total_escritas
        total_hits = self.hit_leituras + self.hit_escritas
        taxa_hit_leitura = self.hit_leituras / self.total_lidas if self.total_lidas else 0
        taxa_hit_escrita = self.hit_escritas / self.total_escritas if self.total_escritas else 0
        taxa_hit_global = total_hits / total_acessos if total_acessos else 0

        tempo_medio = ((total_hits * self.hit_time) + ((total_acessos - total_hits) * (self.tempo_mp + self.hit_time))) / total_acessos if total_acessos else 0

        print("RESULTADOS OBTIDOS:")
        for chave, valor in params.items():
            print(f"{chave}: {valor}")
        print(f"Total de leituras: {self.total_lidas}")
        print(f"Total de escritas: {self.total_escritas}")
        print(f"Total de acessos: {total_acessos}")
        print(f"Escritas na memória principal: {self.escritas_mp}")
        print(f"Leituras na memória principal: {self.leituras_mp}")
        print(f"Hit rate leitura: {taxa_hit_leitura:.4f} ({self.hit_leituras})")
        print(f"Hit rate escrita: {taxa_hit_escrita:.4f} ({self.hit_escritas})")
        print(f"Hit rate global: {taxa_hit_global:.4f} ({total_hits})")
        print(f"Tempo médio de acesso (ns): {tempo_medio:.4f}")


def executa_script(dic_parametros):
    endereco_operacoes = []
    with open(dic_parametros['arquivo'], 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            endereco, operacao = linha.split()
            endereco_operacoes.append((endereco, operacao))

    print(f"Total de endereços lidos: {len(endereco_operacoes)}")

    memoria = MemoriaCache(dic_parametros)
    memoria.simular(endereco_operacoes)
    memoria.relatorio(dic_parametros)


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
