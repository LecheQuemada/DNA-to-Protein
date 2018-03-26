#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Dependencias y variables:
import re
import sys
import gettext
import locale

lugar = locale.getdefaultlocale()

en = gettext.translation('en', localedir='locale', languages=['en'])


if len(sys.argv) > 1:
   if sys.argv[1] == "es":
       _ = lambda s: s
   if sys.argv[1] == "en":
       en.install()
else:
   if "es" in lugar[0]:
       _ = lambda s: s
   else:
       en.install()

def main():
    #Paso 1. Input de la cadena:
    cadena = input(_("Escriba la cadena de ADN a convertir:  "))
    tipo_c = input(_("¿La cadena es molde [escriba 't'] (3'5) o complementaria [escriba 'n'] (5'3)?  "))
    intrones = input(_("Escriba los intrones ARN o ADN a usar separados por un espacio (e.g. TCA AAC CGC GAT):  "))
    tipo_i = input(_("¿Intrones tipo ARN [escriba 'R'] o ADN [escriba 'D']? (ARN por defecto) "))
    print("\n")

    try:
        paso_uno = preconversion(cadena, tipo_c, intrones, tipo_i)
        #Imprimir cadena molde
        print(paso_uno[0])

        paso_dos = transcripcion(paso_uno[0], paso_uno[1])
        #Cadena dividida en inicio, tripletes, final
        print(paso_dos[0][0] + ' '.join(paso_dos[0][1]) + paso_dos[0][2] + "\n")
        #ARN Inmaduro y Maduro
        print(' '.join(paso_dos[1]) + "\n" + ' '.join(paso_dos[2]) + "\n")
        
        paso_tres = traduccion(paso_dos[2])
        #Imprimir lista de proteínas
        print(' '.join(paso_tres) + "\n")

        try:
            while True:
                paso_dos = transcripcion(paso_dos[0][2], paso_uno[1])
                #Cadena dividida en inicio, tripletes, final
                print(paso_dos[0][0] + ' '.join(paso_dos[0][1]) + paso_dos[0][2] + "\n")
                #ARN Inmaduro y Maduro
                print(' '.join(paso_dos[1]) + "\n" + ' '.join(paso_dos[2]) + "\n")
                
                paso_tres = traduccion(paso_dos[2])
                #Imprimir lista de proteínas
                print(' '.join(paso_tres) + "\n")

        except ValueError:
            print (_("Conversión completa"))


    except ValueError as ve:
        print (ve)
    


def preconversion(gen, gtipo, intrones, itipo):
    #Primera función, toma una cadena de ADN, su tipo (Molde [t] o Complementaria [n])
    #una cadena de intrones separados por un espacio, su tipo (ADN [D] o ARN [R])
    #Convertir Intrones ADN -> ARN
    if itipo == "D":
        intrones = intrones.replace("G", "P").replace("C", "G").replace("P", "C")
        intrones = intrones.replace("A", "H").replace("T", "A").replace("H", "U")
    #Hacer lista de intrones
    intrones = intrones.split(" ")
    
    #Crear cadena molde a partir de la complementaria
    if gtipo == "n":
        #Reemplazar C's por G's y G's por C's de forma astuta
        gen = gen.replace("G", "P").replace("C", "G").replace("P", "C")
        #Reemplazar A's por T's y T's por A's de forma astuta
        gen = gen.replace("A", "H").replace("T", "A").replace("H", "T")
    
    #La función regresa la cadena molde y los intrones en el lenguaje correcto {Tupla(Str, Lista)}
    return (gen,intrones)

def transcripcion(gen, intrones):
    #Segunda función, toma una cadena molde de ADN e intrones en una lista
    #en ARN, lo convierte a un ARN Maduro, con pasos intermedios
    #con propósito de comprensión del proceso, devuelve en total Tupla(Str, Lista, Tupla(Str, Str), Lista, Lista)

    
    #Definimos la señal de inicio y las de alto
    s_inicio = ['TAC']
    s_alto = ['ATC','ACT','ATT']

    #Si la cadena contiene la señal de inicio...
    if s_inicio[0] in gen:
        #Partir desde señal de inicio
        val_uno = gen.split(s_inicio[0], 1)
        #Crear lista de tripletes
        tripletes_uno = re.findall('..?.?', val_uno[1])

        #Buscar señal de alto en tripletes
        if any(triplete in s_alto for triplete in tripletes_uno):
            #Hacer lista de señales de alto encontradas
            altos_uno = [triplete for triplete in tripletes_uno if triplete in s_alto]
            #Buscar el índice de la primera en tripletes
            s_alto_uno = tripletes_uno.index(altos_uno[0])
            #Crear tripletes dos hasta la señal de alto
            tripletes_dos = tripletes_uno[0:s_alto_uno]
            gen_2 = ''.join(tripletes_uno[s_alto_uno+1:])
            final_cadena = (altos_uno[0], gen_2)
            #val_uno[0] + tripletes_dos + final_cadena[n]

        else:
            tripletes_dos = tripletes_uno
            final_cadena = ("...", "")

        #Aunar a lista el inicio
        tripletes_dos.insert(0, s_inicio[0])
        #Aunar a lista el final
        tripletes_dos.append(final_cadena[0])
        #Crear tupla con información del gen final
        cadena_des = (val_uno[0], tripletes_dos, final_cadena[1])
        #Reemplazar de forma astuta, se obtiene ADN Inmaduro
        tripletes_tres = [triplete.replace("G", "P").replace("C", "G").replace("P", "C") for triplete in tripletes_dos]
        tripletes_tres = [triplete.replace("A", "H").replace("T", "A").replace("H", "U") for triplete in tripletes_tres]
        #Remover intrones, se obtiene ADN Maduro
        tripletes_cuatro = [x for x in tripletes_tres if x not in intrones]
        #Regresamos la cadena partida en inicio, gen, final {Tupla(Str, Lista, Str)}
        #              ARN Inmaduro {Lista}
        #              ARN Maduro   {Lista}
        # {Tupla(Tupla(Str, Lista, Tupla(Str, Str)), Lista, Lista))}
        return (cadena_des, tripletes_tres, tripletes_cuatro)

    #Si la señal no contiene la señal de inicio...
    else:
        raise ValueError(_("La cadena proporcionada no contiene un gen."))


def traduccion(arn):
    #Tercera función, toma una cadena de ADN Maduro en forma de lista
    #Regresa una tupla con las abreviaturas de las proteínas en ella
    #Tuplas Definidas
    Met = ("AUG",)
    Ile = ("AUA", "AUC", "AUU")
    Arg = ("AGG", "AGA", "CGG", "CGA", "CGC", "CGU")
    Ser = ("AGC", "AGU", "UCG", "UCA", "UCC", "UCU")
    Thr = ("ACG", "ACA", "ACC", "ACU")
    Lys = ("AAG", "AAA")
    Asn = ("AAC", "AAU")
    Leu = ("UUG", "UUA", "CUG", "CUA", "CUC", "CUU")
    Phe = ("UUC", "UUU")
    Trp = ("UGG",)
    STP = ("UGA", "UAG", "UAA")
    Cys = ("UGC", "UGU")
    Tyr = ("UAC", "UAU")
    Val = ("GUG", "GUA", "GUC", "GUU")
    Gly = ("GGG", "GGA", "GGC", "GGU")
    Ala = ("GCG", "GCA", "GCC", "GCU")
    Glu = ("GAA", "GAG")
    Asp = ("GAU", "GAC")
    Pro = ("CCG", "CCA", "CCC", "CCU")
    Gln = ("CAA", "CAG")
    His = ("CAU", "CAC")

    #Proteinas enlistadas
    aminoacids = (Met,Ile,Arg,Ser,Thr,Lys,Asn,Leu,Phe,Trp,STP,Cys,Tyr,Val,Gly,Ala,Glu,Asp,Pro,Gln,His)
    aminocopy = ("Met","Ile","Arg","Ser","Thr","Lys","Asn","Leu","Phe","Trp","STP","Cys","Tyr","Val","Gly","Ala","Glu","Asp","Pro","Gln","His")

    protein = []
    for triplete in arn:
        for amino, amcopy in zip(aminoacids, aminocopy):
            for value in amino:
                if value == triplete:
                    protein.append(amcopy)
    #Regresa lista
    return protein

if __name__ == "__main__":
    main()


                    



