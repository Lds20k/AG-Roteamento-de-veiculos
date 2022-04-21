# AG: O problema de roteamento de veículos

Alunos do curso de Gastronomia do SENAC decidiram se juntar e montar uma padaria chamada ***Bolos da Patroa*** focada em bolos e doces para eventos e reuniões. Para fazer esta entrega, a padaria comprou um conjunto de pequenas vans para fazer a entrega.

Os pedidos são feitos durante a madrugada para que estejam prontos para entrega no dia seguinte pela amanhã.

A necessidade para a equipe de transporte é que as vans fizessem aproximadamente a mesma quilometragem por dia e pudessem carregar aproximadamente a mesma quantidade carga entre elas para quem nenhuma equipe ficasse sobrecarregada.

Desta forma, a padaria precisa da ajudar dos alunos do Bacharelado de Ciência da Computação para resolver este problema.

### Introdução Teórica

Este problema é um caso especial do problema do Caixeiro-Viajante que é chamado do Problema de Roteamento de Veículos ou Vehicle Routing Problem (VRP). 

Este é um problema clássico para entregas em que vários veículos precisam fazer entregas ou captações em pontos específicos e precisam fazer a menor rota possível, evitar que rotas se sobreponham e saiam e voltem de depósitos.

![Grafo](https://crivelaro.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F9de9527d-d25c-49cd-874d-c7bb87debaa2%2FUntitled.png?table=block&id=af58b1d2-fd6e-47d9-b066-e81de5bd4346&spaceId=946856ea-5862-45c3-837c-7f93cf5cea98&width=880&userId=&cache=v2)

Para o nosso problema, vamos considerar o número de vans variáveis, mas podemos testar com 4 vans.

### Os dados disponíveis

Neste problema, temos uma sequência de locais que podemos chamar de 0, 1, 2, 3, 4, ..., até N. O Local 0 (zero) é o local da padaria de onde as vans saem e chegam. 

Para a modelagem, iremos passar as distâncias entre os locais de pontos, por exemplo: entre 0 e 1, temos distância de 548.

Utilizar a seguinte matriz de distâncias:

[https://replit.com/@celsosenac/ep-geneticos#main.py](https://replit.com/@celsosenac/ep-geneticos#main.py)

### A modelagem

Devemos modelar um algoritmo genético que dada uma quantidade de N de vans e as distâncias entre os pontos de entrega, deve gerar:

- Genes e indivíduos: o que é um indivíduo neste problema
- Função de fitness: como saber a qualidade de um conjunto de rotas
- Função de mutação: como mudar a ordem das cidades e entre as vans
- Função de crossover: como trocar genes entre os indivíduos

Além disto, será necessário testar taxas de mutação, crossover e quantidade de indivíduos que sobrará em cada geração.

### Saída esperada

Para o número N de vans deve reproduzir a rota esperava de cada uma

Van 1:

2 → 5 → 3

Van 2: 

4 → 6 → 1
