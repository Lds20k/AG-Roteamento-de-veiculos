from asyncio.windows_events import INFINITE
import random
import math


def create_data_model():
    data = {}
    data["matriz_disntancia"] = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
    ]
    data["num_vehicles"] = 3
    data["depot"] = 0
    return data


# hiperparâmetros
tamanho_populacao = 100
tx_mutacao = 0.50
tx_crossover = 0.15
tx_tragedia = 0.05
geracoes_max = 100000
geracoes_tragedia = 100
#################
tx_variacao_fitness = 10


def calcula_distancia(matriz_distancia, inicio, destino):
    return matriz_distancia[inicio][destino]

# utilidade
# quando menor melhor (foi o que ela disse)
def fitness(individuo):
    score = 0
    for caminho_van in individuo:
        for i in range(len(caminho_van)):
            if i < len(caminho_van) - 1:
                score += calcula_distancia(data_model["matriz_disntancia"], caminho_van[i], caminho_van[i+1])
    return score


def gerar_individuo(data_model):
    individuo = []
    qtd_caminhos = len(data_model["matriz_disntancia"])

    caminho = list(range(qtd_caminhos))
    caminho.pop(data_model["depot"])
    random.shuffle(caminho)

    indices = list(range(len(caminho)))
    indices = indices[1:len(indices) - 1]

    tamanho = data_model["num_vehicles"] - 1
    sample = sorted(random.sample(indices, tamanho))

    inicio = 0
    for i in range(data_model["num_vehicles"]):
        van:list = []

        van.append(0)
        if i < len(sample):
            van.extend(caminho[inicio:sample[i]])
            inicio = sample[i]
        else:
            van.extend(caminho[inicio:])
        van.append(0)

        individuo.append(van)
    
    return individuo

def mutacao(populacao):
    """ Retorna uma populuação mutada

        populacao - Indivíduos da população a serem multados
    """
    qtd = math.ceil(tx_mutacao * len(populacao))
    populacao_escolhida = random.choices(populacao, k=qtd)
    return [ mutacao_flip(individuo) for individuo in populacao_escolhida]

# flip de valor de gene de um gene aleatório
def mutacao_flip(individuo):
    novo_individuo = individuo.copy()
    random.shuffle(novo_individuo)
    
    tamanho_caminho_van: list = []
    for van in novo_individuo:
        tamanho_caminho_van.append(len(van) - 2)

    for i in range(0, len(novo_individuo) - 1):
        taxa = (len(novo_individuo[i]) - 2)/ len(data_model["matriz_disntancia"])
        taxa = int(math.floor(taxa * 100))

        sorteio = random.randint(11, 100)
        if sorteio <= taxa:
            no_local = novo_individuo[i].pop(random.randint(1, tamanho_caminho_van[i]))
            novo_individuo[i + 1].insert(random.randint(1, tamanho_caminho_van[i + 1]), no_local)
            forcar = False
    
    return novo_individuo

def crossover(populacao, geracao):
    funcao_decaimento_crossover = math.exp(-geracao / 200)
    qtd = funcao_decaimento_crossover*tx_crossover*len(populacao)
    populacao_crossover = []
    populacao_escolhida = random.choices(populacao, k=math.ceil(qtd))
    for i in range(len(populacao_escolhida) - 1):
        for j in range(i+1, len(populacao_escolhida)):
            ind1 = populacao_escolhida[i]
            ind2 = populacao_escolhida[j]

            ind1_Mvans: list = []
            ind2_Mvans: list = []
            for i in range(data_model["num_vehicles"]):
                ind1_Mvans += ind1[i]
                ind1_Mvans.remove(0)
                ind1_Mvans.remove(0)

                ind2_Mvans += ind2[i]
                ind2_Mvans.remove(0)
                ind2_Mvans.remove(0)
            
            novo_individuo1:list = []
            novo_individuo2:list = []
            for i in range(data_model["num_vehicles"]):
                van:list = []
                van.append(0)
                for van_ind in range(len(ind1[i]) - 2):
                    van.append(ind2_Mvans.pop(0))
                van.append(0)
                novo_individuo2.append(van)

                van:list = []
                van.append(0)
                for van_ind in range(len(ind2[i]) - 2):
                    van.append(ind1_Mvans.pop(0))
                van.append(0)
                novo_individuo1.append(van)
            
            populacao_crossover.append(novo_individuo1)
            populacao_crossover.append(novo_individuo2)

    return populacao_crossover

# escolhe os indivíduos mais aptos


def selecao_com_tragedia(populacao, geracao):
    nova_populacao = sorted(populacao, key=fitness)
    if (geracao % geracoes_tragedia == 0):
        tamanho_tragedia = math.ceil(tamanho_populacao*tx_tragedia)
        novos_individuos = [gerar_individuo() for _ in range(
            0, tamanho_populacao - tamanho_tragedia)]
        return nova_populacao[0:tamanho_tragedia] + novos_individuos
    else:
        return nova_populacao[0:tamanho_populacao]


def selecao(populacao, geracao):
    nova_populacao = sorted(populacao, key=fitness)
    return nova_populacao[0:tamanho_populacao]


data_model = create_data_model()
print(calcula_distancia(data_model["matriz_disntancia"], 0, 5))

populacao = [gerar_individuo(data_model) for _ in range(0, tamanho_populacao)]
populacao = sorted(populacao, key=fitness)
geracao = 0

fitness0_atual = fitness(populacao[0])
menor_fitness = fitness0_atual
while fitness(populacao[-1]) - fitness0_atual >= tx_variacao_fitness and fitness0_atual < menor_fitness and geracao < geracoes_max:
    if fitness0_atual < menor_fitness:
        menor_fitness = fitness0_atual

    geracao += 1
    populacao_mutada = mutacao(populacao)
    populacao_crossover = crossover(populacao, geracao)
    populacao = selecao(populacao_mutada + populacao +
                        populacao_crossover, geracao)
    if geracao % 100 == 0 or (geracao % 10 == 0 and geracao < 100):
        print("---------------- Intermediário: " + str(geracao) + " ----------------")
        print(populacao[0])
        print("Taxa de Acerto: " + str(fitness(populacao[0])))
    
    fitness0_atual = fitness(populacao[0])

print("---------------- Final " + str(geracao) + " ----------------")
print(populacao[0])
print("Taxa de Acerto: " + str(fitness(populacao[0])))
