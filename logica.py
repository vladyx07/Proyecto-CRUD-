"""Lógica del.

sistema crud.
"""

import json
import os

# Los archivos se guardan junto a los .py del proyecto
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_JSON = os.path.join(CARPETA, "estudiantes.json")
ARCHIVO_TXT = os.path.join(CARPETA, "estudiantes.txt")


class GestorEstudiantes:
    """Maneja la lista de estudiantes y el archivo JSON."""

    def __init__(self):
        """Crea la lista.

        de materias.
        """
        self.estudiantes = []   # lista de diccionarios
        self.cargar()

    # ---------- Archivo JSON ----------
    def cargar(self):
        """Lee el JSON al iniciar. Si no existe, empieza vacío."""
        if os.path.exists(ARCHIVO_JSON):
            try:
                with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
                    self.estudiantes = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.estudiantes = []

    def guardar_json(self):
        """Escribe la lista completa en el JSON."""
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(self.estudiantes, f, indent=4, ensure_ascii=False)

    # ---------- CRUD ----------
    def buscar(self, id_iest):
        """Regresa el diccionario del.

        estudiante o None si no existe.
        """
        for estudiante in self.estudiantes:
            if estudiante["id_iest"] == id_iest:
                return estudiante
        return None

    def guardar(self, estudiante):
        """Crea el estudiante; si el ID ya existe, lo actualiza.

        Regresa 'creado' o 'actualizado'.
        """
        existente = self.buscar(estudiante["id_iest"])
        if existente:
            existente.update(estudiante)
            accion = "actualizado"
        else:
            self.estudiantes.append(estudiante)
            accion = "creado"
        self.guardar_json()
        return accion

    def eliminar(self, id_iest):
        """Elimina por ID. Regresa True si lo encontró."""
        estudiante = self.buscar(id_iest)
        if estudiante is None:
            return False
        self.estudiantes.remove(estudiante)
        self.guardar_json()
        return True

    # ---------- Impresión ----------
    def imprimir(self):
        """Escribe todos los estudiantes en un archivo de texto."""
        with open(ARCHIVO_TXT, "w", encoding="utf-8") as f:
            f.write("LISTA DE ESTUDIANTES\n")
            f.write("=" * 40 + "\n")
            for e in self.estudiantes:
                f.write(f"Nombre:   {e['nombre']}\n")
                f.write(f"ID IEST:  {e['id_iest']}\n")
                f.write(f"Carrera:  {e['carrera']}\n")
                f.write(f"Semestre: {e['semestre']}\n")
                f.write(f"Correo:   {e['correo']}\n")
                f.write("-" * 40 + "\n")
        return ARCHIVO_TXT
