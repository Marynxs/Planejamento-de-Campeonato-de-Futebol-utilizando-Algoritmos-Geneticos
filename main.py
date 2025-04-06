import random

times_info = [
    ("Campos FC", "Campos", 23000),
    ("Guardiões FC", "Guardião", 40000),
    ("CA Protetores", "Guardião", 20000),
    ("SE Leões", "Leão", 40000),
    ("Simba EC", "Leão", 15000),
    ("SE Granada", "Granada", 10000),
    ("CA Lagos", "Lagos", 20000),
    ("Solaris EC", "Ponte-do-Sol", 30000),
    ("Porto FC", "Porto", 45000),
    ("Ferroviária EC", "Campos", 38000),
    ("Portuários AA", "Porto", 12000),
    ("CA Azedos", "Limões", 18000),
    ("SE Escondidos", "Escondidos", 50000),
    ("Secretos FC", "Escondidos", 25000),
]

top_5_times = set([x[0] for x in sorted(times_info, key=lambda x: -x[2])[:5]])
cidades_por_time = {nome: cidade for nome, cidade, _ in times_info}

def gerar_jogos():
    jogos = []
    for i in range(len(times_info)):
        for j in range(i+1, len(times_info)):
            time1, time2 = times_info[i][0], times_info[j][0]
            jogos.append((time1, time2, cidades_por_time[time1]))
            jogos.append((time2, time1, cidades_por_time[time2]))
    return jogos

TODOS_JOGOS = gerar_jogos()
RODADAS = 26
JOGOS_POR_RODADA = 7

class Individuo:
    def __init__(self):
        random.shuffle(TODOS_JOGOS)
        self.jogos_por_rodada = [TODOS_JOGOS[i*JOGOS_POR_RODADA:(i+1)*JOGOS_POR_RODADA] for i in range(RODADAS)]
        self._fitness = None

    def fitness(self):
        if self._fitness is not None:
            return self._fitness

        penalidade = 0
        for rodada in self.jogos_por_rodada:
            times_na_rodada = set()
            cidades_na_rodada = set()
            classicos_na_rodada = 0
            for mandante, visitante, cidade in rodada:
                if mandante in times_na_rodada or visitante in times_na_rodada:
                    penalidade += 1
                else:
                    times_na_rodada.update([mandante, visitante])
                if cidade in cidades_na_rodada:
                    penalidade += 1
                else:
                    cidades_na_rodada.add(cidade)
                if mandante in top_5_times and visitante in top_5_times:
                    classicos_na_rodada += 1
            if classicos_na_rodada > 1:
                penalidade += (classicos_na_rodada - 1)

        self._fitness = 1 / (1 + penalidade)
        return self._fitness

    def mutacao(self):
        filho = Individuo()
        filho.jogos_por_rodada = [list(r) for r in self.jogos_por_rodada]
        r1, r2 = random.sample(range(RODADAS), 2)
        j1, j2 = random.randint(0,6), random.randint(0,6)
        filho.jogos_por_rodada[r1][j1], filho.jogos_por_rodada[r2][j2] = filho.jogos_por_rodada[r2][j2], filho.jogos_por_rodada[r1][j1]
        return filho

    def crossover(self, outro):
        filho = Individuo()
        todos_jogos = set(TODOS_JOGOS)
        usados = set()
        filho.jogos_por_rodada = [[] for _ in range(RODADAS)]

        for i in range(RODADAS):
            for j in range(JOGOS_POR_RODADA):
                jogo = self.jogos_por_rodada[i][j] if random.random() < 0.5 else outro.jogos_por_rodada[i][j]
                if jogo not in usados:
                    filho.jogos_por_rodada[i].append(jogo)
                    usados.add(jogo)

        restantes = list(todos_jogos - usados)
        random.shuffle(restantes)
        for i in range(RODADAS):
            while len(filho.jogos_por_rodada[i]) < JOGOS_POR_RODADA:
                filho.jogos_por_rodada[i].append(restantes.pop())

        return filho

    def imprime(self):
        for i, rodada in enumerate(self.jogos_por_rodada):
            print(f"\nRodada {i+1}:")
            for mandante, visitante, cidade in rodada:
                print(f"  {mandante} x {visitante} - {cidade}")
        print()

    def verificar_restricoes(self):
        print("\n🔍 Verificando restrições da solução final...")
        sucesso = True
        jogos_usados = set()

        for rodada_idx, rodada in enumerate(self.jogos_por_rodada):
            times_na_rodada = set()
            cidades_na_rodada = set()
            classicos_na_rodada = 0

            for jogo in rodada:
                mandante, visitante, cidade = jogo

                if jogo in jogos_usados:
                    print(f"❌ Rodada {rodada_idx+1}: Jogo repetido: {jogo}")
                    sucesso = False
                else:
                    jogos_usados.add(jogo)

                if mandante in times_na_rodada or visitante in times_na_rodada:
                    print(f"❌ Rodada {rodada_idx+1}: {mandante} ou {visitante} jogando mais de uma vez")
                    sucesso = False
                times_na_rodada.update([mandante, visitante])

                if cidade in cidades_na_rodada:
                    print(f"❌ Rodada {rodada_idx+1}: cidade {cidade} com mais de um jogo")
                    sucesso = False
                cidades_na_rodada.add(cidade)

                if mandante in top_5_times and visitante in top_5_times:
                    classicos_na_rodada += 1

            if classicos_na_rodada > 1:
                print(f"❌ Rodada {rodada_idx+1}: mais de um clássico ({classicos_na_rodada})")
                sucesso = False

        if len(jogos_usados) != len(TODOS_JOGOS):
            print(f"❌ Número de jogos únicos = {len(jogos_usados)}; esperado = {len(TODOS_JOGOS)}")
            sucesso = False

        if sucesso:
            print("✅ Todas as restrições foram respeitadas!")
        return sucesso

class Populacao:
    def __init__(self, tamanho=30):
        self.individuos = [Individuo() for _ in range(tamanho)]

    def torneio(self, k=3):
        competidores = random.sample(self.individuos, k)
        return max(competidores, key=lambda x: x.fitness())

    def evoluir(self, geracoes=5000):
        best_fitness_overall = 0
        stagnation_counter = 0  # Inicializa o contador de estagnação
        for geracao in range(geracoes):
            self.individuos.sort(key=lambda x: -x.fitness())
            melhor = self.individuos[0]
            print(f"Geração {geracao+1}: Fitness = {melhor.fitness():.4f}")

            if melhor.fitness() > best_fitness_overall:
                best_fitness_overall = melhor.fitness()
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Injeção de diversidade se houver estagnação prolongada
            if stagnation_counter > 500:
                print(f"Estagnação detectada na geração {geracao+1}; injetando diversidade.")
                num_replace = len(self.individuos) // 2
                for i in range(len(self.individuos) - num_replace, len(self.individuos)):
                    self.individuos[i] = Individuo()
                stagnation_counter = 0

            if melhor.fitness() == 1.0:
                print("\n🏆 Solução ótima encontrada!")
                melhor.imprime()
                melhor.verificar_restricoes()
                return melhor

            nova_geracao = self.individuos[:5]
            while len(nova_geracao) < len(self.individuos):
                pai1 = self.torneio()
                pai2 = self.torneio()
                filho = pai1.crossover(pai2)
                if random.random() < 0.3:
                    filho = filho.mutacao()
                nova_geracao.append(filho)

            self.individuos = nova_geracao

        print("\n🔚 Melhor solução após todas as gerações:")
        melhor = self.individuos[0]
        melhor.imprime()
        melhor.verificar_restricoes()
        return melhor


pop = Populacao()
pop.evoluir(geracoes=5000)
