# Importazione delle librerie
import json
import random

# Configurazione dell'applicativo

P1 = 0.5  #probabilità di biforcazione
P2 = 0.5  #probabilità di tagliare la biforcazione

bif = 0  #numero di biforcazioni

#funzione che dato il blocco precedente e la relativa altezza genera un blocco figlio
def creaBlocco(b_pred, h_pred):
	if h_pred>=0:  #se non è il nodo radice
		hash_pred = b_pred.get('hash')
	else:  #se è il nodo radice
		hash_pred = ""
	height = h_pred+1
	hash_val = hash("block"+str(height)+str(hash_pred))
	block = {"hash":hash_val,"prev_block":hash_pred,"height":height, "height_pred":h_pred}
	return block

#funzione che popola ricorsivamente la lista dei blocchi fino a profondità n
def creaFigli(block_pred, lista, n):
	height_pred = block_pred.get('height')
	global bif
	if height_pred < n-1:
		p_cut = random.uniform(0.0, 1.0)  #valore relativo alla probabilità di taglio della biforcazione
		if bif>0 and p_cut>=P2:
			bif = bif-1
		else:
			block = creaBlocco(block_pred, height_pred)
			lista.append(block)
			creaFigli(block, lista, n)
			p_bif = random.uniform(0.0, 1.0)  #valore relativo alla probabilità di creazione della biforcazione
			if p_bif>=P1:
				block2 = creaBlocco(block_pred, height_pred)
				bif = bif+1
				lista.append(block2)
				creaFigli(block2, lista, n)

#funzione che genera il file json della blockchain di profondità massima n
def creaJson(n):
	#data_set = {"key1": [1, 2, 3], "key2": [4, 5, 6]}
	#json_dump = json.dumps(data_set)
	#print(json_dump)

	lista = []
	radice = creaBlocco({}, -1)
	lista.append(radice)
	creaFigli(radice, lista, n)

	data_set = {"blocks": lista}
	with open("blockchain.json", "w") as blockchain:
		json.dump(data_set, blockchain)
	

creaJson(10)