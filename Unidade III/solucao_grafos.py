"""
solucao_grafos.py — Grafos, BFS e DFS (Estrutura de Dados II)

Simulação computacional DIDÁTICA de conectividade entre aeroportos (siglas IATA).
NÃO é um modelo de navegação aeronáutica: as conexões e bloqueios são fictícios.

Pergunta de pesquisa:
    Na rede simulada, quantas conexões podem ser bloqueadas antes que
    BSB deixe de alcançar CWB, e como BFS e DFS se comportam
    em cada cenário?

Uso:
    python solucao_grafos.py            # modo interativo
    python solucao_grafos.py --testes   # executa os testes automáticos
"""

import sys
import unicodedata
from collections import deque
from itertools import combinations

# ---------------------------------------------------------------------------
# 1. Modelagem: grafo NÃO dirigido, não ponderado, em lista de adjacência.
#    Cada conexão aparece nas listas dos dois extremos.
# ---------------------------------------------------------------------------
ARESTAS = [
    ("BSB", "GYN"),
    ("BSB", "CNF"),
    ("GYN", "GRU"),
    ("GYN", "CGB"),
    ("GYN", "CGR"),
    ("CNF", "GIG"),
    ("CNF", "GRU"),
    ("GRU", "GIG"),
    ("GRU", "CWB"),
    ("GIG", "CWB"),
    ("CGB", "CWB"),
    ("CGR", "CWB"),
    ("CGR", "POA"),
    ("CWB", "POA"),
]


def construir_grafo(arestas):
    """Constrói a lista de adjacência (dicionário de listas)."""
    rede = {}
    for a, b in arestas:
        rede.setdefault(a, []).append(b)
        rede.setdefault(b, []).append(a)
    return rede


GRAFO = construir_grafo(ARESTAS)

# Nomes dos aeroportos (apenas para exibição e para aceitar nomes na entrada)
NOMES = {
    "BSB": "Brasília", "GYN": "Goiânia", "CNF": "Belo Horizonte (Confins)",
    "GRU": "São Paulo (Guarulhos)", "GIG": "Rio de Janeiro (Galeão)",
    "CGB": "Cuiabá", "CGR": "Campo Grande", "CWB": "Curitiba",
    "POA": "Porto Alegre",
}


# ---------------------------------------------------------------------------
# 2. Algoritmos de busca
# ---------------------------------------------------------------------------
def bfs(rede, origem, destino):
    """Busca em largura (fila FIFO). Retorna lista de vértices ou None."""
    fila = deque([(origem, [origem])])
    visitados = {origem}
    while fila:
        atual, caminho = fila.popleft()
        if atual == destino:
            return caminho
        for vizinho in rede.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    return None


def dfs(rede, origem, destino):
    """Busca em profundidade (pilha LIFO). Retorna lista de vértices ou None."""
    pilha = [(origem, [origem])]
    visitados = set()
    while pilha:
        atual, caminho = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        if atual == destino:
            return caminho
        # reversed: o 1º vizinho da lista é o último empilhado => explorado primeiro
        for vizinho in reversed(rede.get(atual, [])):
            if vizinho not in visitados:
                pilha.append((vizinho, caminho + [vizinho]))
    return None


# ---------------------------------------------------------------------------
# 3. Contingência: bloqueio SEM alterar a rede original (trabalha em cópia)
# ---------------------------------------------------------------------------
def bloquear_conexoes(rede, conexoes):
    """Retorna uma cópia da rede sem as conexões indicadas (nos dois sentidos)."""
    copia = {no: viz.copy() for no, viz in rede.items()}
    for a, b in conexoes:
        if b in copia.get(a, []):
            copia[a].remove(b)
        if a in copia.get(b, []):
            copia[b].remove(a)
    return copia


def contar_arestas(caminho):
    """Número de arestas de um caminho (None se não houver caminho)."""
    return None if caminho is None else len(caminho) - 1


# ---------------------------------------------------------------------------
# 4. Entrada do usuário com validação (ignora maiúsculas e acentos)
# ---------------------------------------------------------------------------
def normalizar(texto):
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return " ".join(sem_acento.casefold().split())


def validar_vertice(rede, texto):
    """Retorna a sigla do vértice (aceita sigla ou nome da cidade) ou None."""
    mapa = {normalizar(v): v for v in rede}
    for sigla, nome in NOMES.items():
        if sigla in rede:
            mapa[normalizar(nome)] = sigla
            mapa.setdefault(normalizar(nome.split(" (")[0]), sigla)
    return mapa.get(normalizar(texto))


def pedir_vertice(rede, rotulo):
    while True:
        valor = input(f"{rotulo}: ").strip()
        vertice = validar_vertice(rede, valor)
        if vertice:
            return vertice
        print(f"  '{valor}' não existe na rede. Opções: {', '.join(sorted(rede))}")


def pedir_bloqueios(rede):
    """Lê conexões 'A - B' para bloquear; linha vazia encerra."""
    bloqueios = []
    print("Informe conexões a bloquear no formato 'SIGLA A - SIGLA B' "
          "(linha vazia para terminar).")
    while True:
        linha = input("  Bloquear: ").strip()
        if not linha:
            return bloqueios
        partes = [p.strip() for p in linha.replace("–", "-").split("-")]
        if len(partes) != 2:
            print("  Formato inválido. Exemplo: GYN - GRU")
            continue
        a, b = validar_vertice(rede, partes[0]), validar_vertice(rede, partes[1])
        if not a or not b:
            print("  Vértice inexistente.")
        elif b not in rede[a]:
            print("  Essa conexão não existe na rede.")
        else:
            bloqueios.append((a, b))
            print(f"  Bloqueio registrado: {a} – {b}")


# ---------------------------------------------------------------------------
# 5. Apresentação dos resultados
# ---------------------------------------------------------------------------
def formatar(caminho):
    if caminho is None:
        return "SEM CAMINHO (destino inalcançável neste cenário)"
    return f"{' → '.join(caminho)}  [{contar_arestas(caminho)} arestas]"


def executar_cenario(nome, rede, origem, destino):
    print(f"\nCenário: {nome}")
    print(f"  BFS: {formatar(bfs(rede, origem, destino))}")
    print(f"  DFS: {formatar(dfs(rede, origem, destino))}")


def analisar_conectividade(rede, origem, destino):
    """Responde à pergunta de pesquisa: testa bloqueios de 1 e 2 conexões."""
    arestas = sorted({tuple(sorted(par)) for par in ARESTAS})
    print(f"\nAnálise de conectividade {origem} → {destino}")
    for k in (1, 2):
        criticos = [c for c in combinations(arestas, k)
                    if bfs(bloquear_conexoes(rede, c), origem, destino) is None]
        print(f"  Conjuntos de {k} conexão(ões) que desconectam o destino: "
              f"{len(criticos)}")
        for c in criticos:
            print("    - " + " ; ".join(f"{a}–{b}" for a, b in c))


# ---------------------------------------------------------------------------
# 6. Testes automáticos
# ---------------------------------------------------------------------------
def testes():
    original = {no: viz.copy() for no, viz in GRAFO.items()}
    resultados = []

    def checar(descricao, condicao):
        resultados.append(condicao)
        print(f"[{'OK' if condicao else 'FALHOU'}] {descricao}")

    print("=== TESTES AUTOMÁTICOS ===")

    # Estrutura
    checar("grafo tem pelo menos 7 vértices", len(GRAFO) >= 7)
    checar("grafo é simétrico (não dirigido)",
           all(a in GRAFO[b] for a in GRAFO for b in GRAFO[a]))

    # T1 — rede normal
    c_bfs = bfs(GRAFO, "BSB", "CWB")
    c_dfs = dfs(GRAFO, "BSB", "CWB")
    print(f"  T1 BFS: {formatar(c_bfs)}")
    print(f"  T1 DFS: {formatar(c_dfs)}")
    checar("T1 BFS encontra caminho de 3 arestas", contar_arestas(c_bfs) == 3)
    checar("T1 DFS encontra caminho válido",
           c_dfs and c_dfs[0] == "BSB" and c_dfs[-1] == "CWB"
           and all(b in GRAFO[a] for a, b in zip(c_dfs, c_dfs[1:])))
    checar("T1 BFS <= DFS em número de arestas",
           contar_arestas(c_bfs) <= contar_arestas(c_dfs))

    # T2 — bloqueio GYN–GRU
    r2 = bloquear_conexoes(GRAFO, [("GYN", "GRU")])
    c2_bfs, c2_dfs = bfs(r2, "BSB", "CWB"), dfs(r2, "BSB", "CWB")
    print(f"  T2 BFS: {formatar(c2_bfs)}")
    print(f"  T2 DFS: {formatar(c2_dfs)}")
    checar("T2 ainda existe caminho", c2_bfs is not None and c2_dfs is not None)
    checar("T2 caminhos não usam a conexão bloqueada",
           all({"GYN", "GRU"} != {a, b}
               for p in (c2_bfs, c2_dfs) for a, b in zip(p, p[1:])))
    checar("rede original NÃO foi alterada", GRAFO == original)

    # T3 — bloqueio duplo que isola BSB
    r3 = bloquear_conexoes(GRAFO, [("BSB", "GYN"), ("BSB", "CNF")])
    checar("T3 sem caminho (BFS retorna None)", bfs(r3, "BSB", "CWB") is None)
    checar("T3 sem caminho (DFS retorna None)", dfs(r3, "BSB", "CWB") is None)
    checar("T3 contar_arestas(None) é None", contar_arestas(None) is None)

    # T4 — origem == destino
    checar("T4 origem = destino => caminho de 0 arestas",
           contar_arestas(bfs(GRAFO, "CWB", "CWB")) == 0)

    # T5 — validação de entrada
    checar("T5 aceita 'bsb' e 'brasilia' (sem acento/maiúscula)",
           validar_vertice(GRAFO, "bsb") == "BSB"
           and validar_vertice(GRAFO, "brasilia") == "BSB")
    checar("T5 rejeita vértice inexistente", validar_vertice(GRAFO, "Atlântida") is None)

    # T6 — DFS depende da ordem dos vizinhos (Experimento D)
    alterado = {no: viz.copy() for no, viz in GRAFO.items()}
    alterado["BSB"].reverse()
    d_antes, d_depois = dfs(GRAFO, "BSB", "CWB"), dfs(alterado, "BSB", "CWB")
    print(f"  T6 DFS ordem original: {formatar(d_antes)}")
    print(f"  T6 DFS ordem invertida: {formatar(d_depois)}")
    checar("T6 DFS muda com a ordem dos vizinhos", d_antes != d_depois)
    checar("T6 BFS mantém o nº de arestas com a ordem alterada",
           contar_arestas(bfs(GRAFO, "BSB", "CWB"))
           == contar_arestas(bfs(alterado, "BSB", "CWB")))

    # T7 — grafo com ciclo termina (visitados evita laço infinito)
    ciclo = {"A": ["B"], "B": ["A", "C"], "C": ["B", "A"], "D": []}
    checar("T7 ciclo + vértice isolado: BFS/DFS terminam com None",
           bfs(ciclo, "A", "D") is None and dfs(ciclo, "A", "D") is None)

    analisar_conectividade(GRAFO, "BSB", "CWB")

    print(f"\n{sum(resultados)}/{len(resultados)} testes passaram.")
    return all(resultados)


# ---------------------------------------------------------------------------
# 7. Programa interativo
# ---------------------------------------------------------------------------
def principal():
    print("=== Simulação de conectividade (BFS x DFS) — uso DIDÁTICO ===")
    print("Aeroportos (siglas):", ", ".join(f"{v} ({NOMES[v]})" for v in sorted(GRAFO)))
    origem = pedir_vertice(GRAFO, "Origem")
    destino = pedir_vertice(GRAFO, "Destino")

    executar_cenario("Rede normal", GRAFO, origem, destino)

    bloqueios = pedir_bloqueios(GRAFO)
    if bloqueios:
        rede_bloqueada = bloquear_conexoes(GRAFO, bloqueios)  # cópia
        nome = "Bloqueio: " + "; ".join(f"{a}–{b}" for a, b in bloqueios)
        executar_cenario(nome, rede_bloqueada, origem, destino)

    print("\nObservação: BFS minimiza o nº de arestas (grafo não ponderado); "
          "DFS encontra um caminho qualquer, que depende da ordem dos vizinhos. "
          "Nenhum considera tempo, distância ou custo, nem serve para voos reais.")


if __name__ == "__main__":
    if "--testes" in sys.argv:
        sys.exit(0 if testes() else 1)
    principal()
