# Importamos las bibliotecas.. nescesarias
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk 
import sqlite3 

# Desarrollo de la interfaz gráfica.. 
root = Tk()
root.title("Sistema de Facturación..")
root.geometry("600x350") # Dimensiones de la ventana..

# Asignamos las respectivas variables a nuestro sistema..

idproduct = StringVar()
nombreProduct = StringVar()
cantidadProduct = StringVar()
valorProducto = StringVar()

# Conexion con la base de Datos..

def conexionBBDD():
    miConex=sqlite3.connect("base") # Aqui nombramos el nombre de la base de datos..
    miCursor=miConex.cursor()# creamos variable tipo cursor..

    try:
        miCursor.execute('''
            CREATE TABLE sistema (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBREPRODUCT VARCHAR(50) NOT NULL,
            CANTIDADPRODUCT INT NOT NULL,
            VALORPRODUCT INT NOT NULL)
        ''')
        messagebox.showinfo("CONEXION","Base de Datos Creada Correctamente..")
    except: # Creamos una exepcion para captar un error..
        messagebox.showinfo("CONEXION","Conexion Exitosa con la Base de Datos")

def eliminarBBDD():
    miConex=sqlite3.connect("base")
    miCursor=miConex.cursor()
    if messagebox.askyesno(message="Los Datos se Perderán definitivamente, Desea Continuar?", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE sistema")# Si el usuario dice que si eliminamos la base de datos
    else:
        pass
    limpiarCampos()
    mostrar()
    

def salirAplicacion():
    valor=messagebox.askquestion("Salir", "Estas Seguro que deseas Salir  de la Aplicación?")
    if valor=="yes":
       root.destroy()# Cerramos la ventana con el Método Destroy..

def limpiarCampos():
    idproduct.set("")
    nombreProduct.set("")
    cantidadProduct.set("")
    valorProducto.set("")

def mensaje(): # Agregamos información de la aplicación..
    acerca='''
    SISTEMA DE FACTURACIÓN CRUD 
    Version 1.0
    Create by The Geek
    Tecnología Usada Python Tkinter
    '''
    messagebox.showinfo(title="información", message=acerca)

    # Definimos los Metodos para el Crud..

def crear():
    miConex=sqlite3.connect("base")# Nos conectamos a nuestra base de datos..
    miCursor=miConex.cursor()
    try:
        datos=nombreProduct.get(),cantidadProduct.get(),valorProducto.get()
        miCursor.execute("INSERT INTO sistema VALUES(NULL,?,?,?)", (datos))
        miConex.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrio un error al crear registro,verifique Conexion")
        pass # Con la siguiente palabra pass salimos de la excepcion..
    limpiarCampos()
    mostrar()
def mostrar():
    miConex=sqlite3.connect("base")
    miCursor=miConex.cursor()
    registros=tree.get_children() # Almacenamos todos los elementos de nuestra tabla con get_children
    for elemento in registros:
        tree.delete(elemento)

    try:
        miCursor.execute("SELECT * FROM sistema")
        for row in miCursor:
            tree.insert('',0,text=row[0],values=(row[1],row[2],row[3])) # Dentro de el objeto insert insertamos los datos..
    except:
        pass

# TABLA..

tree=ttk.Treeview(height=10, columns=('#0','#1','#2')) # creamos la tabla con sus respectivas columnas para los valores
tree.place(x=0, y=130)# Le damos la posicion donde queremos que se ubique

# Colocamos la cabecera

tree.column('#0',width=100)#Dimensiones..
tree.heading('#0',text="ID", anchor=CENTER)#Creamos un encabezado
tree.heading('#1',text="Nombre del Producto", anchor=CENTER)
tree.heading('#2',text="Cantidad", anchor=CENTER)
tree.column('#3',width=100)
tree.heading('#3',text="Valor", anchor=CENTER)

def seleccionarUsandoClick(event):
    item=tree.identify('item',event.x,event.y) # Tomamos los elementos dentro de la posicion..
    idproduct.set(tree.item(item,"text"))
    nombreProduct.set(tree.item(item,"values")[0])
    cantidadProduct.set(tree.item(item,"values")[1])
    valorProducto.set(tree.item(item,"values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick)


def actualizar():
    miConex=sqlite3.connect("base")
    miCursor=miConex.cursor()
    try:
        datos=nombreProduct.get(),cantidadProduct.get(),valorProducto.get()
        miCursor.execute("UPDATE  sistema SET NOMBREPRODUCT=?, CANTIDADPRODUCT=?, VALORPRODUCT=? WHERE ID="+idproduct.get(), (datos))
        miConex.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrio un error al actualizar el  registro")
        pass
    limpiarCampos()
    mostrar()

def borrar():
    miConex=sqlite3.connect("base")
    miCursor=miConex.cursor()
    try:
        if messagebox.askyesno(message="Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM sistema WHERE ID="+idproduct.get())
            miConex.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
        pass
    limpiarCampos()
    mostrar()

# Colocamos los Menus en las Ventanas...

menubar=Menu(root)
menubasedat=Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar a la base de datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

# Creando Menu Ayuda..

ayudamenu=Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda",menu=ayudamenu)

# Creando etiquetas y cajas de texto..

e1=Entry(root, textvariable=idproduct)

l2=Label(root, text="Nombre")
l2.place(x=50,y=10)
e2=Entry(root, textvariable=nombreProduct, width=50)
e2.place(x=100, y=10)


l3=Label(root, text="Cant")
l3.place(x=50,y=40)
e3=Entry(root, textvariable=cantidadProduct)
e3.place(x=100, y=40)

l4=Label(root, text="Valor")
l4.place(x=280,y=40)
e4=Entry(root, textvariable=valorProducto,width=10)
e4.place(x=320, y=40)

l5=Label(root, text="USD")
l5.place(x=380, y=40)

# Creando los Botones..

b1=Button(root, text="Crear Registro", command=crear)
b1.place(x=50, y=90)

b2=Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=180, y=90)

b3=Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=320, y=90)

b4=Button(root, text="Eliminar Registro", bg="red", command=borrar)
b4.place(x=450, y=90)

root.config(menu=menubar)

root.mainloop()






