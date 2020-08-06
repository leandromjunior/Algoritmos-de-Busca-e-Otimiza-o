#import sys
#sys.path.append('C:\\Users\\lemot\\anaconda3\\lib\\site-packages')
import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt # Biblioteca para acesso aos gráficos

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
lista_produtos = []
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))

#Criando listas separadas(individuais) para espaços, valores e nomes
espacos = []
valores = []
nomes = []

for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)
limite = 3 #equivale a metragem máxima que pode ser transportada (3m³)

toolbox = base.Toolbox()
#O FitnessMax indica que quanto maior o valor, mehor a resposta
creator.create("FitnessMax", base.Fitness, weights=(1.0, )) #Quanto mais próximo de 1, melhor o resultado
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_bool", random.randint, 0, 1) # Ao fazer esse registro, será gerado aleatoriamente o valor 0 ou 1. Se 0, o produto não será carregado
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 
                 n=len(espacos))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def avaliacao(individual): #Essa função receberá os cromossomos com 0 e 1 de toolbox.register("individual)
    nota = 0
    soma_espacos = 0
    
    for i in range(len(individual)): #Percorre cada um dos genes com 0 e 1
        if individual[i] == 1:
            nota = nota + valores[i]
            soma_espacos += espacos[i]
            
    if soma_espacos > limite: #Se soma_espacos for maior que limite(3), nota = 1, que é um valor/solução 'ruim'
        nota = 1
    return nota / 100000,

toolbox.register("evaluate", avaliacao)
toolbox.register("mate", tools.cxOnePoint) #O "mate" fará o crossover de ponto único que se caracteriza pelo "cxOnePoint"
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01) #mutFlipBit fará uma inversão, ou seja, onde é 0 vira 1 e vice-versa, representando a ideia da mutação
toolbox.register("select", tools.selRoulette) #Método da roleta, quanto maior o valor da carga, mais chance de utilizá-lo para as próximas gerações/combinações

if __name__ == "__main__":
    #random.seed(1) #Dará o mesmo resultado em todas as gerações, isto é definido pelo número 1,, se alterar este valor, ele dará resultados diferentes nas proximas gerações
    populacao = toolbox.population(n = 20) #20 individuos dentro da população em cada uma das gerações
    probabilidade_crossover = 1.0 #probabilidade de fazer o crossover é 1, ou seja, 100%
    probabilidade_mutacao = 0.01 #probabilidade de mutação é 1%
    numero_geracoes = 100 # Em cada uma das 100 gerações terá 20 indivíduos que apresentarão as soluções

    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max) #Na compilação esse valor aparecerá como 0.21135, por exemplo, ao multiplicar por 100, será encontrado o valor total da carga
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean) #média
    estatisticas.register("std", numpy.std) #desvio-padrão

#Essa linha vai rodar o algoritmo. População recebe o pacote algorithms./eaSimple é um algoritmo genético simples. Entre parêntes estão a passagem dos parâmetros declarados acima
    populacao, info = algorithms.eaSimple(populacao, toolbox,
                                          probabilidade_crossover,
                                          probabilidade_mutacao,
                                          numero_geracoes, estatisticas)

    melhores = tools.selBest(populacao, 1) #Selecionará apenas o melhor individuo da geração, isto é definido pelo número 1
    
    for individuo in melhores:
        print(individuo) #printa o individuo
        print(individuo.fitness) #printa a função de avaliação
        #print(individuo[1])
        soma = 0
        for i in range(len(lista_produtos)) : #Este loop indica quais produtos (pelo nome) serão carregados 
            if individuo[i] == 1:
                soma += valores[i]
                print("Nome: %s R$ %s" % (lista_produtos[i].nome,
                                          lista_produtos[i].valor))
        print("Melhor solução: %s" % soma)
        
    valores_grafico = info.select("max") #parâmetro max da linha 79
    plt.plot(valores_grafico)
    plt.title("Acompanhamento dos valores")
    plt.show()
    
#biblioteca deap é utilizada para mexer com algoritmos genéticos