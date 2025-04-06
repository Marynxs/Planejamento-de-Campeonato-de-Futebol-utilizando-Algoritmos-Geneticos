# ⚽ Gerador de Tabela de Campeonato com Restrições (Algoritmo Genético)

Este projeto implementa um **algoritmo genético** para organizar uma tabela de 182 jogos entre 14 times ao longo de 26 rodadas, respeitando restrições rígidas relacionadas a:

- Repetição de times por rodada
- Conflito de cidades por rodada
- Controle de clássicos entre os 5 maiores clubes

---

## 🎯 Objetivo

Distribuir todos os jogos (ida e volta entre 14 times) em 26 rodadas com 7 jogos cada, garantindo que:

- Nenhum time jogue mais de uma vez por rodada
- Nenhuma cidade tenha mais de um jogo por rodada
- Máximo de 1 clássico por rodada
- Todos os 182 jogos ocorram **exatamente uma vez**

---

## 🧠 Tecnologias e Estratégias

- **Python 3**
- Algoritmo Genético com:
  - Seleção por Torneio
  - Crossover com verificação de duplicatas
  - Mutação com troca de jogos
  - Elitismo (manutenção dos melhores)
  - Injeção de diversidade após estagnação

---

## 🚀 Como executar

```Python
pop = Populacao()
pop.evoluir(geracoes=*numero desejado de gerações*)
```

```Saida
Geração x₀: Fitness = y₀
...
Geração xₙ: Fitness = yₙ

🔚 Melhor solução após todas as gerações:
Rodada 1:
  Campos FC x Simba EC - Campos
  ...
Rodada 26:
  ...


❌ Rodada 4: cidade Porto com mais de um jogo
❌ Número de jogos únicos = 179; esperado = 182
```

