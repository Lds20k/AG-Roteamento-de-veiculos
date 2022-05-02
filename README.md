# AG: O problema de roteamento de veículos

## Coma executar

É necessário ter Python3 instalado e executar em modo depuração(Debug), a branch principal (main) terá um resultado com o tamanho dos caminhos de cada van padronizado e fixado de acordo com o número de entregas existente e o número de vans disponíveis porém a branch "feat/sem-restriao-tamanho" contém um código para pegar a menor quilometragem possivel de todas as vans não se importando com o número de entregas de cada van. Já na branch "feat/quilometragem-tamanho-parecido" tenta selecionar os indivíduos com número de vans parecido e focando na quilometragem geral.

Além de algumas mudanças na branch main as principais diferenças entre as branches são:

| Nome da branch                      | Mutação Flip | Mutação Robin Hood | Geração de indivíduos                               |
|-------------------------------------|--------------|--------------------|-----------------------------------------------------|
| main                                | Não possui   | Não possui         | Deixa padronizado o tamanho dos caminho de cada van |
| feat/sem-restriao-tamanho           | Possui       | Possui             | Tamanho dos caminhos randomizado entre as vans      |
| feat/quilometragem-tamanho-parecido | Não possui   | Possui             | Tamanho dos caminhos randomizado entre as vans      |

## Descrição do problema

Alunos do curso de Gastronomia do SENAC decidiram se juntar e montar uma padaria chamada ***Bolos da Patroa*** focada em bolos e doces para eventos e reuniões. Para fazer esta entrega, a padaria comprou um conjunto de pequenas vans para fazer a entrega.

Os pedidos são feitos durante a madrugada para que estejam prontos para entrega no dia seguinte pela amanhã.

A necessidade para a equipe de transporte é que as vans fizessem aproximadamente a mesma quilometragem por dia e pudessem carregar aproximadamente a mesma quantidade carga entre elas para quem nenhuma equipe ficasse sobrecarregada.

Desta forma, a padaria precisa da ajudar dos alunos do Bacharelado de Ciência da Computação para resolver este problema.

### Introdução Teórica

Este problema é um caso especial do problema do Caixeiro-Viajante que é chamado do Problema de Roteamento de Veículos ou Vehicle Routing Problem (VRP). 

Este é um problema clássico para entregas em que vários veículos precisam fazer entregas ou captações em pontos específicos e precisam fazer a menor rota possível, evitar que rotas se sobreponham e saiam e voltem de depósitos.

![Grafo](https://crivelaro.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F9de9527d-d25c-49cd-874d-c7bb87debaa2%2FUntitled.png?table=block&id=af58b1d2-fd6e-47d9-b066-e81de5bd4346&spaceId=946856ea-5862-45c3-837c-7f93cf5cea98&width=880&userId=&cache=v2)

### Output

Para o nosso problema, vamos considerar o número de vans variáveis, mas podemos testar com 4 vans.

Possível saída com 4 vans (número da van, caminho e distâncias):

![image](https://user-images.githubusercontent.com/52457167/166172911-f9c6db53-8f8f-4022-86d3-52cde3f647cb.png)
