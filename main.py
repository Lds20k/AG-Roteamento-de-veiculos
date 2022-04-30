import random
import math
import copy

def create_data_model():
    data = {}
    data["matriz_disntancia"] = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],        # 0
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],     # 1
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],    # 2    
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],     # 3 
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],     # 4
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],       # 5
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],      # 6
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],        # 7
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],       # 8
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],        # 9
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],    # 10    
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],      # 11
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],       # 12
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],       # 13
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],     # 14
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],   # 15    
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],     # 16
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data

# hiperparâmetros
tamanho_populacao = 200
tx_mutacao = 0.6
tx_crossover = 0.4
tx_tragedia = 0.2
geracoes_max = 1000
geracoes_tragedia = 100


def calcula_distancia(matriz_distancia, inicio, destino):
    return matriz_distancia[inicio][destino]

# utilidade
# quando menor melhor
def fitness(individuo):
    score = 0
    for caminho_van in individuo:
        for i in range(len(caminho_van) - 1):
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
    qtd = math.ceil(tx_mutacao * len(populacao))
    populacao_escolhida = random.choices(populacao, k=qtd)
    populacao_mutacao = []
    
    for individuo in populacao_escolhida:
        mutacao_escolhida = str(random.choices(["flip", "robin_hood", "swap","interval"], weights = [0, 0.4, 0.3, 0.3], k = 1)[0])
        if mutacao_escolhida == "flip":
            populacao_mutacao.append(mutacao_flip(individuo))
        elif mutacao_escolhida == "robin_hood":
            populacao_mutacao.append(mutacao_robin_hood(individuo))
        elif mutacao_escolhida == "swap":
            populacao_mutacao.append(mutacao_swap(individuo))
        else:
            populacao_mutacao.append(mutacao_interval(individuo))

    return populacao_mutacao

# tira um caminho da van com mais caminhos e coloca em uma van com menos
def mutacao_robin_hood(individuo):
    novo_individuo = copy.deepcopy(individuo)

    
    caminhos_van: list = []
    index_van_maior_caminho = 0
    index_van_menor_caminho = 0

    for van_index in range(len(novo_individuo)):
        tamanho_caminho = len(novo_individuo[van_index])

        if tamanho_caminho > 1:
            caminho = list(range(1, tamanho_caminho - 1))
            caminhos_van.append(caminho)
        else:
            caminhos_van.append([1])
        
        if tamanho_caminho > len(novo_individuo[index_van_maior_caminho]):
            index_van_maior_caminho = van_index 
        elif tamanho_caminho < len(novo_individuo[index_van_menor_caminho]):
            index_van_menor_caminho = van_index 
        
    indice_caminho_maior = random.choice(caminhos_van[index_van_maior_caminho])
    indice_caminho_menor = random.choice(caminhos_van[index_van_menor_caminho])
    caminho_excluido = novo_individuo[index_van_maior_caminho].pop(indice_caminho_maior)
    novo_individuo[index_van_menor_caminho].insert(indice_caminho_menor, caminho_excluido) 
        

    return novo_individuo

# seleciona duas vans e pega indices aleatorios (exceto o começo e o fim que sao depositos) e troca eles
def mutacao_swap(individuo):
    novo_individuo = copy.deepcopy(individuo)

    
    caminhos_van: list = []
    for van in novo_individuo:
        tamanho_caminho = len(van) - 1 
        if tamanho_caminho > 1:
            caminho = list(range(1, tamanho_caminho))
            caminhos_van.append(caminho)
        else:
            caminhos_van.append([1])

    for index in range(len(novo_individuo)):
        indice_van1 = index
        indice_van2 = index - 1
        
        indiceCaminho1 = random.choice(caminhos_van[indice_van1])
        indiceCaminho2 = random.choice(caminhos_van[indice_van2])
        novo_individuo[indice_van1][indiceCaminho1], novo_individuo[indice_van2][indiceCaminho2] = novo_individuo[indice_van2][indiceCaminho2], novo_individuo[indice_van1][indiceCaminho1] 
        

    return novo_individuo


# seleciona um intervalo e inverte a ordem ou embaralha
def mutacao_interval(individuo):
    novo_individuo = copy.deepcopy(individuo)
    
    caminhos_van: list = []
    for van in novo_individuo:
        tamanho_caminho = len(van) - 2 
        if tamanho_caminho > 1:
            caminho = list(range(1, tamanho_caminho))
            caminhos_van.append(caminho)
        else:
            caminhos_van.append([1])

    for index, van in enumerate(novo_individuo):
        if len(caminhos_van[index]) > 1:
            intervalo = sorted(random.sample(caminhos_van[index], 2))
            mutacao_escolhida = random.choices(["scramble","inversion"], weights = [0.5, 0.5], k = 1)[0]
            mutacao = []
            if mutacao_escolhida == "scramble":
                mutacao = van[intervalo[0]:(intervalo[1] + 1)]
                random.shuffle(mutacao)
            else:    
                mutacao = van[intervalo[0]:(intervalo[1] + 1)][::-1]
            
            novo_individuo[index] = van[0:intervalo[0]] + mutacao + van[ (intervalo[1] + 1) :]

    return novo_individuo

# flip de valor de gene de um gene aleatório
def mutacao_flip(individuo):
    novo_individuo = copy.deepcopy(individuo)
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
    
    return novo_individuo

def crossover(populacao, geracao):
    funcao_decaimento_crossover = math.exp(-geracao / 200)
    qtd = funcao_decaimento_crossover*tx_crossover*len(populacao)
    populacao_crossover = []
    populacao_escolhida = random.choices(populacao, k=math.ceil(qtd))
    
    if len(populacao_escolhida) < data_model["num_vehicles"]:
        return populacao

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

# escolhe os mais aptos e quando chega no ano de sangue escolhe aleatoriamente os individuos que vao morrer por tragédia
def selecao_com_tragedia(populacao, geracao):
    if (geracao % geracoes_tragedia == 0):
        tamanho_tragedia = math.ceil(tamanho_populacao*tx_tragedia)
        novos_individuos = [gerar_individuo(data_model) for _ in range(
            0, tamanho_populacao - tamanho_tragedia)]
        return sorted(populacao[0:tamanho_tragedia] + novos_individuos, key=fitness)
    else:
        nova_populacao = sorted(populacao, key=fitness)
        return nova_populacao[0:tamanho_populacao]

data_model = create_data_model()
populacao = [gerar_individuo(data_model) for _ in range(0, tamanho_populacao)]
populacao = sorted(populacao, key=fitness)
geracao = 0

while geracao < geracoes_max:

    geracao += 1
    populacao_mutada = mutacao(populacao)
    populacao_crossover = crossover(populacao, geracao)
    populacao = selecao_com_tragedia(populacao_mutada + populacao +
                        populacao_crossover, geracao)
    if geracao % 100 == 0 or (geracao % 10 == 0 and geracao < 100):
        print("---------------- Geração: " + str(geracao) + " ----------------")
        print(populacao[0])
        print("Distância percorrida com todas as vans: " + str(fitness(populacao[0])))

# output desejável
melhor_individuo = populacao[0]
for index, caminho_van in enumerate(melhor_individuo):
    print(f'Van {index + 1}')
    caminho_sem_deposito = [str(numero) for numero in caminho_van]
    caminho_sem_deposito = caminho_sem_deposito[1:len(caminho_sem_deposito)-1]
    print(' -> '.join(caminho_sem_deposito),end='\n')
    score = 0
    for i in range(len(caminho_van) - 1):
            score += calcula_distancia(data_model["matriz_disntancia"], caminho_van[i], caminho_van[i+1])
    print(f'Distância de cada van: {score}',end='\n\n')
    
print("Distância percorrida com todas as vans: " + str(fitness(populacao[0])))
