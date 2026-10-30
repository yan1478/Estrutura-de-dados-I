# Grafos, BFS e DFS — Simulação de conectividade entre aeroportos (siglas IATA)

**Disciplina:** Estrutura de Dados II — Ciência da Computação
**Motivação:** pane relacionada ao GPS e impactos em voos no Aeroporto de Brasília (G1 DF, 22 set. 2026).
**Referência:** GOMES, P. C. R. *Grafos: conceitos fundamentais, algoritmos e aplicações*. Blumenau: Editora IFC, 2022.

> **Aviso:** simulação computacional didática, **não** é modelo de navegação aeronáutica. Cidades, conexões e bloqueios são fictícios; o resultado não pode orientar voo real.

## 1. Problema e objetivo
Uma indisponibilidade de recursos pode exigir replanejamento. Aqui, representamos conexões hipotéticas entre cidades como um grafo para estudar **conectividade** e comparar **BFS** e **DFS**.

**Pergunta de pesquisa:** na rede simulada, quantas conexões podem ser bloqueadas antes que BSB deixe de alcançar CWB, e como BFS e DFS se comportam em cada cenário?

## 2. Estrutura do grafo
**Vértices (aeroportos):** BSB = Brasília, GYN = Goiânia, CNF = Belo Horizonte (Confins), GRU = São Paulo (Guarulhos), GIG = Rio de Janeiro (Galeão), CGB = Cuiabá, CGR = Campo Grande, CWB = Curitiba, POA = Porto Alegre. (Os slides usam BHZ, código da cidade de Belo Horizonte; aqui uso CNF, a sigla do aeroporto.)

G = (V, E), **não dirigido** e **não ponderado**, com |V| = 9 e |E| = 14, em lista de adjacência (`dict` de listas, cada aresta nas duas listas). Diagrama: `diagrama_grafo.png`.

| Aresta | Justificativa (fictícia) |
|---|---|
| BSB–GYN, BSB–CNF | BSB é a origem, com duas ligações regionais |
| GYN–GRU, GYN–CGB, GYN–CGR | GYN como hub do Centro-Oeste |
| CNF–GIG, CNF–GRU, GRU–GIG | Triângulo do Sudeste (cria ciclos) |
| GRU–CWB, GIG–CWB, CGB–CWB, CGR–CWB | Quatro entradas em CWB (destino) |
| CGR–POA, CWB–POA | Vértice extra, cria mais um ciclo |

Em relação ao grafo-base da aula, acrescentei **CGR** e **POA** e mais ciclos, o que gera rotas alternativas além da ordem de listagem.

## 3. Como executar
```bash
python solucao_grafos.py            # interativo: origem, destino e bloqueios
python solucao_grafos.py --testes   # 17 testes automáticos + análise de conectividade
```
Funcionalidades: siglas validadas (aceita também o nome da cidade, ignora maiúsculas/acentos, lista as opções se inválido); bloqueio feito em **cópia** (rede original intacta); mostra caminho e nº de arestas; casos sem caminho tratados (`None` → mensagem clara); origem = destino devolve 0 arestas.

## 4. Resultados (BSB → CWB)
Saídas completas em `evidencias_testes.txt` e `evidencia_interativa.txt`.

| Cenário | BFS | DFS |
|---|---|---|
| A. Rede normal | BSB → GYN → GRU → CWB (**3**) | BSB → GYN → GRU → CNF → GIG → CWB (**5**) |
| B. Bloqueio GYN–GRU | BSB → GYN → CGB → CWB (**3**) | BSB → GYN → CGB → CWB (**3**) |
| C. Bloqueio GYN–GRU + GYN–CGB | BSB → GYN → CGR → CWB (**3**) | idem (**3**) |
| D. Bloqueio BSB–GYN + BSB–CNF | sem caminho | sem caminho |
| E. DFS com vizinhos de BSB invertidos | (BFS continua com 3 arestas) | BSB → CNF → GIG → GRU → GYN → CGB → CWB (**6**) |

**Conectividade (resposta à pergunta de pesquisa):** nenhum bloqueio de 1 conexão desconecta BSB de CWB; dos pares de conexões, **somente** {BSB–GYN, BSB–CNF} desconecta. Como BSB tem grau 2, são necessários 2 bloqueios, ou seja, a rede tem 2 caminhos independentes em arestas entre origem e destino, e o gargalo é a própria origem.

**Relação com os experimentos da aula:** A = linha A da tabela; B = linha B (o bloqueio é hipótese didática, não consequência comprovada da pane); C = linha C (ainda há caminho porque restam rotas alternativas, via CGR); D = linha E (o resultado do DFS muda sem que o grafo mude, só a ordem dos vizinhos).

## 5. Comparação BFS × DFS
- **BFS** (fila FIFO) explora por níveis e, em grafo não ponderado, devolve o caminho com **menos arestas**. Custo O(V+E).
- **DFS** (pilha LIFO) aprofunda um ramo antes de voltar. Acha *um* caminho se existir, mas pode ser mais longo (5 contra 3 arestas no cenário A) e **depende da ordem dos vizinhos** (cenário E). Custo O(V+E).
- Ambos usam `visitados` e terminam em grafos com ciclos.

## 6. Limitações
- Grafo não ponderado: "menor" = menos arestas, não menor tempo, distância, custo ou combustível (para isso, Dijkstra, cap. 7 de Gomes).
- Conexões fictícias, sem horários, capacidade, regras aeronáuticas, clima ou escalas.
- Arestas bidirecionais, sem direção de voo; bloqueios de arestas, não de vértices (aeroportos).
- Só devolve um caminho; não enumera todas as alternativas.

## 7. Questões para reflexão
1. **Grafo × árvore binária:** a árvore tem hierarquia, um único caminho entre dois nós, sem ciclos e no máximo 2 filhos. A rede de conexões tem ciclos, múltiplos caminhos e grau arbitrário.
2. **Menor caminho com BFS:** quando o grafo é **não ponderado** (ou todas as arestas têm o mesmo custo). "Menor" significa menor número de arestas, não de km ou de horas.
3. **DFS ≠ BFS:** DFS segue um ramo até o fim e retorna o primeiro caminho que encontra, conforme a ordem dos vizinhos; BFS varre por distância crescente.
4. **Sem `visitados`:** em grafos com ciclos, os algoritmos podem reentrar em vértices indefinidamente (laço infinito) e, mesmo sem laço, repetem trabalho exponencialmente.
5. **Para avaliar tempo/custo:** pesos nas arestas (duração, distância, tarifa), horários, capacidade, escalas e restrições operacionais; usar algoritmos de caminho mínimo ponderado.
6. **Não serve a voo real:** o modelo é fictício e simplificado; aviação real depende de regulação, segurança, meteorologia, combustível, tripulação e controle de tráfego aéreo.

## 8. Roteiro da apresentação (5 min)
1. **(0:30)** Motivação (notícia) e pergunta de pesquisa; aviso de que é simulação.
2. **(1:00)** Diagrama: 9 vértices, 14 arestas, lista de adjacência.
3. **(1:30)** Demo ao vivo: `--testes` e uma execução interativa com bloqueio e um nome inválido.
4. **(1:30)** BFS (3) × DFS (5), efeito da ordem dos vizinhos e cenário sem caminho.
5. **(0:30)** Limitações e extensão (pesos e Dijkstra).

## 9. Arquivos
`solucao_grafos.py` · `README.md` · `diagrama_grafo.png` · `evidencias_testes.txt` · `evidencia_interativa.txt`
