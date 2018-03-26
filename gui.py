#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Paquetes y Variables Necesarias
from dnatoprotein import *
import gettext
import locale
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

lugar = locale.getdefaultlocale()

try:
    en = gettext.translation('gui_en', localedir='locale', languages=['en'])
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

except FileNotFoundError as FNF:
    _ = lambda s: s


#Se crea la Ventana
class ADNaProteina(Gtk.Window):

    #Auto Función
    def __init__(self):
        #Título de la Ventana
        Gtk.Window.__init__(self, title=_("ADN a Proteína"))
        #Borde de la Ventana
        self.set_border_width(20)
        #Caja Maestra
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        #Añadiendo Caja Maestra
        self.add(box_outer)
        #Creando ListBox, modo de selección y añadiéndola
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)
        
        ##########Empieza Primer Fila##########
        #Declaramos Fila
        row_one = Gtk.ListBoxRow()
        #Declaramos 1ra caja vertical, la añadimos
        vbox_one = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        row_one.add(vbox_one)
        #Declaramos 1ra caja horizontal, la añadimos a caja v.
        hbox_one = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        vbox_one.pack_start(hbox_one, True, True, 0)
        #Ventana -> Caja Maestra -> ListBox -> 1ra Fila -> Caja V -> Caja H
        #Creamos entrada uno, con placeholder, y preferentemente mayusculas
        entry1 = Gtk.Entry()
        entry1.set_placeholder_text(_("Ingrese la cadena y seleccione tipo"))
        hint = Gtk.InputHints(16)
        entry1.set_input_hints(hint)
        #Creamos lista de opciones para tipos de cadena e intrones
        chtipos=[_("Molde (3'5)"), _("Complementaria (5'3)")]
        acids=["ARN", "ADN"]
        #Creamos primer combo, añadimos opciones
        acid_combo = Gtk.ComboBoxText()
        for chtipo in chtipos:
            acid_combo.append_text(chtipo)
        #Por defecto seleccionamos ADN
        acid_combo.set_active(0)
        #Añadimos a la caja la entrada y el combo
        hbox_one.pack_start(entry1, True, True, 0)
        hbox_one.pack_start(acid_combo, False, True, 0)
        #Declaramos la 2nda caja horizontal, la añadimos a caja v.
        hbox_two = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        vbox_one.pack_start(hbox_two, True, True, 0)
        #Declaramos 2nda entrada, con placeholder y hints
        entry2 = Gtk.Entry()
        entry2.set_placeholder_text(_("Ingrese los intrones separados por un espacio"))
        entry1.set_input_hints(hint)
        #Creamos segundo combo, añadimos opciones
        intron_combo = Gtk.ComboBoxText()
        for acid in acids:
            intron_combo.append_text(acid)
        #Por defecto seleccionamos ADN
        intron_combo.set_active(0)
        #Añadimos a la caja el combo y la entrada
        hbox_two.pack_start(entry2, True, True, 0)
        hbox_two.pack_start(intron_combo, False, True, 0)
        #Declaramos el botón principal
        button_one = Gtk.Button.new_with_mnemonic(_("_Convert"))
        #Declaramos texto final por llamado a función
        label = Gtk.Label()
        #Al presionar, función luego descrita
        button_one.connect("clicked", self.on_button_clicked, entry1, entry2, acid_combo, intron_combo, label)
        #Añadir botón a la caja vertical
        vbox_one.pack_start(button_one, True, True, 0)
        #Añadir fila a ListBox
        listbox.add(row_one)
        ##########Termina Primer Fila##########

        ##########Empieza Segunda Fila##########
        #Creamos segunda fila
        row_two = Gtk.ListBoxRow()
        #Y creamos caja vertical dos, ponemos borde
        vbox_two = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, border_width=15)
        #Añadimos a la fila la caja v.2
        row_two.add(vbox_two)
        #Ponemos placeholder
        label.set_text(_("Aquí se mostrarán los resultados"))
        #Lo hacemos seleccionable, con line-wrap
        label.set_selectable(True)
        #label.set_line_wrap(True)
        #Añadimos el texto a la caja v.2
        vbox_two.pack_start(label, True, True, 0)
        #Añadimos la fila a ListBox
        listbox.add(row_two)

    #Función usada al presionar botón
    def on_button_clicked(self, button, entry1, entry2, combo1, combo2, label):
        label.set_text(_("Empezando conversión"))
        if combo1.get_active() == 0:
            tipo_c = "t"
        else:
            tipo_c = "n"
        cadena = entry1.get_text()
        intrones = entry2.get_text()
        if combo2.get_active() == 0:
            tipo_i = "R"
        else:
            tipo_i = "N"

        try:
            paso_uno = preconversion(cadena, tipo_c, intrones, tipo_i)
            paso_dos = transcripcion(paso_uno[0], paso_uno[1])
            paso_tres = traduccion(paso_dos[2])
            #Imprimir
            chain = (paso_dos[0][0] + " " + ' '.join(paso_dos[0][1]) + " " + paso_dos[0][2])
            label.set_text(_("{}\n{}\n{}\n{}\n{}").format(paso_uno[0], chain, ' '.join(paso_dos[1]), ' '.join(paso_dos[2]), ' '.join(paso_tres)))        


            try:
                while True:
                    paso_dos = transcripcion(paso_dos[0][2], paso_uno[1])                  
                    paso_tres = traduccion(paso_dos[2])
                    #Imprimir
                    label.set_text(_("{}\n{}\n{}\n{}\n{}\n{}").format(label.get_text(), paso_uno[0], chain, ' '.join(paso_dos[1]), ' '.join(paso_dos[2]), ' '.join(paso_tres)))        


            except ValueError:
                print (_("Conversión completa"))


        except ValueError as ve:
            label.set_text(_(""))

     


win = ADNaProteina()
win.connect("delete-event", Gtk.main_quit)
win.resize(1200, 300)
win.show_all()
Gtk.main()
