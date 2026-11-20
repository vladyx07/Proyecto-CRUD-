import tkinter as tk
from tkinter import ttk, messagebox

from logica import GestorEstudiantes


class App:
    """Ventana principal. Usa GestorEstudiantes para los datos."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Registro de estudiantes IEST")
        self.gestor = GestorEstudiantes()

        self.crear_formulario()
        self.crear_botones()
        self.crear_tabla()
        self.mostrar_estudiantes()

    # ---------- Construcción de la interfaz ----------
    def crear_formulario(self):
        formulario = tk.Frame(self.ventana)
        formulario.pack(padx=20, pady=10)

        etiquetas = ["Nombre:", "ID IEST:", "Carrera:", "Semestre:", "Correo:"]
        self.entradas = []
        for fila, texto in enumerate(etiquetas):
            tk.Label(formulario, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
            entrada = tk.Entry(formulario, width=30)
            entrada.grid(row=fila, column=1, padx=5, pady=5)
            self.entradas.append(entrada)

        (self.entrada_nombre, self.entrada_id, self.entrada_carrera,
         self.entrada_semestre, self.entrada_correo) = self.entradas

    def crear_botones(self):
        botones = tk.Frame(self.ventana)
        botones.pack(pady=10)
        tk.Button(botones, text="Guardar", width=12, command=self.guardar).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Buscar", width=12, command=self.buscar).grid(row=0, column=1, padx=5)
        tk.Button(botones, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)
        tk.Button(botones, text="Imprimir", width=12, command=self.imprimir).grid(row=0, column=3, padx=5)
        tk.Button(botones, text="Limpiar", width=12, command=self.limpiar_campos).grid(row=0, column=4, padx=5)

    def crear_tabla(self):
        columnas = ("nombre", "id_iest", "carrera", "semestre", "correo")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=8)
        encabezados = ["Nombre", "ID IEST", "Carrera", "Semestre", "Correo"]
        anchos = [150, 80, 150, 70, 180]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho)
        self.tabla.pack(padx=20, pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)

    # ---------- Funciones de apoyo ----------
    def leer_campos(self):
        """Lee y valida los campos. Regresa un diccionario o None."""
        datos = {
            "nombre": self.entrada_nombre.get().strip(),
            "id_iest": self.entrada_id.get().strip(),
            "carrera": self.entrada_carrera.get().strip(),
            "semestre": self.entrada_semestre.get().strip(),
            "correo": self.entrada_correo.get().strip(),
        }
        if "" in datos.values():
            messagebox.showwarning("Datos incompletos", "Llena todos los campos.")
            return None
        if not datos["semestre"].isdigit():
            messagebox.showwarning("Dato inválido", "El semestre debe ser un número.")
            return None
        if "@" not in datos["correo"]:
            messagebox.showwarning("Dato inválido", "El correo no es válido.")
            return None
        return datos

    def llenar_campos(self, estudiante):
        self.limpiar_campos()
        self.entrada_nombre.insert(0, estudiante["nombre"])
        self.entrada_id.insert(0, estudiante["id_iest"])
        self.entrada_carrera.insert(0, estudiante["carrera"])
        self.entrada_semestre.insert(0, estudiante["semestre"])
        self.entrada_correo.insert(0, estudiante["correo"])

    def limpiar_campos(self):
        for entrada in self.entradas:
            entrada.delete(0, tk.END)
        self.entrada_nombre.focus()

    def mostrar_estudiantes(self):
        """Leer: refresca la tabla con los datos actuales."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for e in self.gestor.estudiantes:
            self.tabla.insert("", tk.END, values=(e["nombre"], e["id_iest"], e["carrera"],
                                                  e["semestre"], e["correo"]))

    # ---------- Acciones de los botones ----------
    def guardar(self):
        datos = self.leer_campos()
        if datos is None:
            return
        accion = self.gestor.guardar(datos)
        self.mostrar_estudiantes()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", f"Estudiante {accion} correctamente.")

    def buscar(self):
        id_iest = self.entrada_id.get().strip()
        if id_iest == "":
            messagebox.showwarning("Sin ID", "Escribe el ID IEST a buscar.")
            return
        estudiante = self.gestor.buscar(id_iest)
        if estudiante is None:
            messagebox.showerror("No encontrado", "No existe un estudiante con ese ID IEST.")
        else:
            self.llenar_campos(estudiante)

    def eliminar(self):
        id_iest = self.entrada_id.get().strip()
        if id_iest == "":
            messagebox.showwarning("Sin ID", "Escribe o selecciona el ID IEST a eliminar.")
            return
        if self.gestor.buscar(id_iest) is None:
            messagebox.showerror("No encontrado", "No existe un estudiante con ese ID IEST.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar al estudiante?"):
            self.gestor.eliminar(id_iest)
            self.mostrar_estudiantes()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Estudiante eliminado.")

    def imprimir(self):
        if not self.gestor.estudiantes:
            messagebox.showwarning("Sin datos", "No hay estudiantes para imprimir.")
            return
        ruta = self.gestor.imprimir()
        messagebox.showinfo("Impreso", f"Archivo generado:\n{ruta}")

    def al_seleccionar(self, evento):
        """Al hacer clic en la tabla, pasa los datos al formulario."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        estudiante = self.gestor.buscar(str(valores[1]))
        if estudiante:
            self.llenar_campos(estudiante)
