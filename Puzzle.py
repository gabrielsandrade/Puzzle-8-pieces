import copy

def cima(estado):
	matriz = copy.deepcopy(estado.tab)
	auxiliar = copy.deepcopy(matriz[estado.linha_espaco - 1][estado.coluna_espaco])
	matriz[estado.linha_espaco - 1][estado.coluna_espaco] = 0
	matriz[estado.linha_espaco][estado.coluna_espaco] = auxiliar
	return matriz
def baixo(estado):
	matriz = copy.deepcopy(estado.tab)
	auxiliar = copy.deepcopy(matriz[estado.linha_espaco + 1][estado.coluna_espaco])
	matriz[estado.linha_espaco + 1][estado.coluna_espaco] = 0
	matriz[estado.linha_espaco][estado.coluna_espaco] = auxiliar
	return matriz
def direita(estado):
	matriz = copy.deepcopy(estado.tab)
	auxiliar = copy.deepcopy(matriz[estado.linha_espaco][estado.coluna_espaco + 1])
	matriz[estado.linha_espaco][estado.coluna_espaco + 1] = 0
	matriz[estado.linha_espaco][estado.coluna_espaco] = auxiliar
	return matriz
def esquerda(estado):
	matriz = copy.deepcopy(estado.tab)
	auxiliar = copy.deepcopy(matriz[estado.linha_espaco][estado.coluna_espaco - 1])
	matriz[estado.linha_espaco][estado.coluna_espaco - 1] = 0
	matriz[estado.linha_espaco][estado.coluna_espaco] = auxiliar
	return matriz

class State(object):

	def __init__(self):
		self.pai = 0
		self.tab = [[0,0,0],[0,0,0],[0,0,0]]
		self.profundidade = 0
		self.custo = 0
		self.acao ="acao"
		self.f = 0
		self.linha_espaco = 0
		self.coluna_espaco = 0
		self.movimentos = []

	def procuraEspaco(self):
		for i in range(3):
			for j in range(3):
				if (self.tab[i][j] == 0):
					self.linha_espaco = i
					self.coluna_espaco = j
					break

	def checaMovimentosPossiveis(self):
		listaDeMovimentos = []
		if (self.linha_espaco == 0):
			listaDeMovimentos.append("BAIXO")
		if (self.linha_espaco == 1):
			listaDeMovimentos.extend(("BAIXO", "CIMA"))
		if (self.linha_espaco == 2):
			listaDeMovimentos.append("CIMA")
		if (self.coluna_espaco == 0):
			listaDeMovimentos.append("DIREITA")
		if (self.coluna_espaco == 1):
			listaDeMovimentos.extend(("ESQUERDA", "DIREITA"))
		if (self.coluna_espaco == 2):
			listaDeMovimentos.append("ESQUERDA")
		self.movimentos = listaDeMovimentos

	def heuristica(self):
		distancia = 0
		for i in range(3):
			for j in range(3):
				valor = self.tab[i][j]
				if (valor == 0):
					continue
				posX = int(valor/3)
				posY = (valor%3)
				distancia += (abs(posX - i) + abs(posY - j)) 
		#print ("Resultado da função heurística : {}".format(distancia))
		self.f = distancia + self.profundidade


def fim(no):
	movimentos = no.profundidade
	while no.pai != 0 :
		print (no.acao)
		for linha in no.tab:
			print (linha)
		print ("")
		no = no.pai
	print ("Nó inicial")
	for linha in no.tab:
		print (linha)
	print ("Solução encontrada realizando {} movimentos".format(movimentos))
	#print ("{} nós visitados.".format(len(visitados)))
	#print ("{} nós encontrados".format(len(fronteira)))
	print ("fim")

def main():

	print ("=========================================================")
	print ("==              Quebra-cabeça de 8 peças               ==")
	print ("==                    Método A*                        ==")
	print ("=========================================================\n")

	estado = [[0,0,0],[0,0,0],[0,0,0]]
	objetivo = [[0,1,2],[3,4,5],[6,7,8]]
	print("Digite a configuracao do estado inicial, linha a linha:")
	print("Digite os valores da primeira linha:")
	estado[0][0] = int(input())
	estado[0][1] = int(input())
	estado[0][2] = int(input())
	print("Digite os valores da segunda linha:")
	estado[1][0] = int(input())
	estado[1][1] = int(input())
	estado[1][2] = int(input())
	print("Digite os valores da terceira linha:")
	estado[2][0] = int(input())
	estado[2][1] = int(input())
	estado[2][2] = int(input())

	"""for i in range(3):
		for j in range(3):
			print (estado[i][j], ' ', end = '')
		print('')"""

	noInicial = State()
	noInicial.tab = estado

	fronteira = [noInicial]
	visitados = []

	while(fronteira != []):
		menor = fronteira[0].f
		melhor = 0
		for indice in range(len(fronteira)):
			if (menor >= fronteira[indice].f):
				menor = fronteira[indice].f
				melhor = indice
		noAtual = fronteira.pop(melhor)
		visitados.append(noAtual)
		#print ("{} visitados.".format(len(visitados)))
		print ("Profundidade = {}".format(noAtual.profundidade))
		print ("Heurística = {}".format(noAtual.f))
		print ("{} visitados.".format(len(visitados)))
		for linha in noAtual.tab:
			print (linha)
		noAtual.procuraEspaco()
		noAtual.checaMovimentosPossiveis()
		if (noAtual.tab == objetivo):
			fim(noAtual)
			break
		
		for movimento in noAtual.movimentos:
			if (movimento == "ESQUERDA"):
				novaMatriz = esquerda(noAtual)
				novoNo = State()
				novoNo.pai = noAtual
				novoNo.tab = novaMatriz
				novoNo.profundidade = noAtual.profundidade + 1
				novoNo.heuristica()
				novoNo.acao = "esquerda"
				novoNo.procuraEspaco()
				insere = True
				for no in fronteira:
					if no.tab == novoNo.tab:
						if(no.profundidade == novoNo.profundidade):
							insere = False
							break
				if insere == True:
					fronteira.append(novoNo)
			elif (movimento == "DIREITA"):
				novaMatriz = direita(noAtual)
				novoNo = State()
				novoNo.pai = noAtual
				novoNo.tab = novaMatriz
				novoNo.profundidade = noAtual.profundidade + 1
				novoNo.heuristica()
				novoNo.acao = "direita"
				novoNo.procuraEspaco()
				insere = True
				for no in fronteira:
					if no.tab == novoNo.tab:
						if(no.profundidade == novoNo.profundidade):
							insere = False
							break
				if insere == True:
					fronteira.append(novoNo)
			elif (movimento == "CIMA"):
				novaMatriz = cima(noAtual)
				novoNo = State()
				novoNo.pai = noAtual
				novoNo.tab = novaMatriz
				novoNo.profundidade = noAtual.profundidade + 1
				novoNo.heuristica()
				novoNo.acao = "cima"
				novoNo.procuraEspaco()
				insere = True
				for no in fronteira:
					if no.tab == novoNo.tab:
						if(no.profundidade == novoNo.profundidade):
							insere = False
							break
				if insere == True:
					fronteira.append(novoNo)
			elif (movimento == "BAIXO"):
				novaMatriz = baixo(noAtual)
				novoNo = State()
				novoNo.pai = noAtual
				novoNo.tab = novaMatriz
				novoNo.profundidade = noAtual.profundidade + 1
				novoNo.heuristica()
				novoNo.acao = "baixo"
				novoNo.procuraEspaco()
				insere = True
				for no in fronteira:
					if no.tab == novoNo.tab:
						if(no.profundidade == novoNo.profundidade):
							insere = False
							break
				if insere == True:
					fronteira.append(novoNo)
				#if not novoNo in fronteira:
				#	fronteira.append(novoNo)

if __name__ == '__main__':
	main()