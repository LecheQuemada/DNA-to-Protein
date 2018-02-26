#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Paso 0. Dependencias y variables:
import re
import gettext
import locale

lugar = locale.getdefaultlocale()

continuar = True
liGEN=[]

en = gettext.translation('translate', localedir='locale', languages=['en'])

if not "es" in lugar[0]:
	en.install()
else:
	_ = lambda s: s

#Paso 1. Input de la cadena:
cadena0 = input(_("Escribe la cadena a transcribir:  "))
cadenat = input(_("¿Cadena molde [escriba 't'] (3'5) o complementaria [escriba 'n'] (5'3)?  "))
intrones = input(_("Escribe los intrones ARN o ADN a usar separados por un espacio (e.g. GGG AAT TTA UUA):  "))
intronet = input(_("¿Intrones tipo ARN [escriba 'R'] o ADN [escriba 'D']? (ARN por defecto) "))
if intronet == "D":
		intrones = intrones.replace("G", "P").replace("C", "G").replace("P", "C")
		intrones = intrones.replace("A", "H").replace("T", "A").replace("H", "U")
intrones = intrones.split(" ")



print("\n")

#Define funcion TRANSCRIPCION
def transcripcion( gen,tipo ):
	sinicio = ['TAC']
	salto = ['ATC','ACT','ATT']
	global cadena0
	global cadenat
	global continuar
	global liGEN


	#Crear cadena molde
	if tipo == "n":
		#Reemplazar C's por G's y G's por C's de forma astuta
		gen = gen.replace("G", "P").replace("C", "G").replace("P", "C")
		#Reemplazar A's por T's y T's por A's de forma astuta
		gen = gen.replace("A", "H").replace("T", "A").replace("H", "T")

		print(_("Se usará la cadena {} como molde").format(gen))
	#No crear cadena molde
	elif tipo == "t":
		print(_("Se usará la cadena {} como molde").format(gen))

	else: 
		print(_("Escriba el tipo de cadena correctamente"))
		quit()

	#Verificar señal de inicio
	if sinicio[0] in gen:
		#Partir desde señal de inicio
		liCAD = gen.split(sinicio[0], 1)
		preINI = liCAD[0]
		posINI = liCAD[1]
		#Crear lista de tripletes
		liPOS_INI = re.findall('..?.?', posINI)
		#Buscar s-alto en liPOS_INI
		if any(x in salto for x in liPOS_INI):
			#Hacer lista de s-altos encontrados
			salto_s = [i for i in liPOS_INI if i in salto]
			indSALTO = liPOS_INI.index(salto_s[0])
			liGEN = liPOS_INI[0:indSALTO]
			cadena0 = ''.join(liPOS_INI[indSALTO+1:])
			#Imprimir gen dividido
			print(_("Se encontró el gen {} {} {} {} {}").format(preINI, sinicio[0], ' '.join(liGEN), salto_s[0], cadena0))
			liGEN.append(salto_s[0])
			does_ends = ""


		else:
			liGEN = liPOS_INI
			#Imprimir gen incompleto
			does_ends = "..."
			print(_("Se encontró el gen {} {} {}{}").format(preINI, sinicio[0], ' '.join(liGEN), does_ends))
			cadena0 = ""

		#Aunar a lista el inicio
		liGEN.insert(0, sinicio[0])
		
		#Reemplazar de forma astuta
		liGEN = [i2.replace("G", "P").replace("C", "G").replace("P", "C") for i2 in liGEN]
		liGEN = [i3.replace("A", "H").replace("T", "A").replace("H", "U") for i3 in liGEN]
		
		print(_("El ARN Inmaduro es: {}{}").format(' '.join(liGEN), does_ends))
		
		#Remover intrones
		for i4 in intrones:
			liGEN[:] = [i5 for i5 in liGEN if i5 != i4]

		print(_("El ARN Maduro es: GTP + {}{} + PoliA").format(' '.join(liGEN), does_ends))

		if sinicio[0] in cadena0:
			continuar = True
			cadenat = "m"
		else:
			continuar = False



 





	else:
		print(_("La cadena molde no contiene un gen, revise la misma y su tipo"))
		quit()


def traduccion( arn ):
	#Tuples Definidas
	Met = ["AUG"]
	Ile = ["AUA", "AUC", "AUU"]
	Arg = ["AGG", "AGA", "CGG", "CGA", "CGC", "CGU"]
	Ser = ["AGC", "AGU", "UCG", "UCA", "UCC", "UCU"]
	Thr = ["ACG", "ACA", "ACC", "ACU"]
	Lys = ["AAG", "AAA"]
	Asn = ["AAC", "AAU"]
	Leu = ["UUG", "UUA", "CTG", "CTA", "CTC", "CTU"]
	Phe = ["UUC", "UUU"]
	Trp = ["UGG"]
	STP = ["UGA", "UAG", "UAA"]
	Cys = ["UGC", "UGU"]
	Tyr = ["UAC", "UAU"]
	Val = ["GUG", "GUA", "GUC", "GUU"]
	Gly = ["GGG", "GGA", "GGC", "GGU"]
	Ala = ["GCG", "GCA", "GCC", "GCU"]
	Glu = ["GAA", "GAG"]
	Asp = ["GAU", "GAC"]
	Pro = ["CCG", "CCA", "CCC", "CCU"]
	Gln = ["CAA", "CAG"]
	His = ["CAU", "CAC"]

	#Proteinas enlistadas
	aminoacids = [Met,Ile,Arg,Ser,Thr,Lys,Asn,Leu,Phe,Trp,STP,Cys,Tyr,Val,Gly,Ala,Glu,Asp,Pro,Gln,His]
	aminocopy = ["Met","Ile","Arg","Ser","Thr","Lys","Asn","Leu","Phe","Trp","STP","Cys","Tyr","Val","Gly","Ala","Glu","Asp","Pro","Gln","His"]

	protein = ""

	for amino,amicop in zip(aminoacids, aminocopy):
		for value in amino:
			for triplete in arn:
				if value == triplete:
					if amicop == "STP":
						protein = protein.rstrip(" - ")
						print(_("La proteína es: {} \n").format(protein))
						return
					else:
						protein += amicop + " - "


					


while continuar:
	transcripcion(cadena0, cadenat)
	traduccion(liGEN)


