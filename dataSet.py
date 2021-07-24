# Importazione delle librerie
import json
import random
import sys
sys.setrecursionlimit(10**6)

# Configurazione dell'applicativo

P1 = 0.999  #probabilità di biforcazione
P2 = 0.02  #probabilità di tagliare la biforcazione

bif = 0  #numero di biforcazioni
ID = 0

#funzione che dato il blocco precedente e la relativa altezza genera un blocco figlio
def creaBlocco(b_pred, h_pred):
	global ID
	if h_pred>=0:  #se non è il nodo radice
		hash_pred = b_pred.get('hash')
	else:  #se è il nodo radice
		hash_pred = ""
	height = h_pred+1
	hash_val = hash("block"+str(height)+str(hash_pred)+str(ID))
	block = {"hash":hash_val,"prev_block":hash_pred,"height":height, "height_pred":h_pred, "id":ID}
	ID = ID+1
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

	lista = []
	radice = creaBlocco({}, -1)
	lista.append(radice)
	creaFigli(radice, lista, n)
	newList = sorted(lista, key=lambda k: k['height'])

	data_set = {"blocks": newList}
	with open("blockchain.json", "w") as blockchain:
		json.dump(data_set, blockchain)
	

creaJson(1100)