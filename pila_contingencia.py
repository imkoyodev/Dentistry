from collections import deque
from paciente import Paciente

class PilaContingencia:
    def __init__(self) -> None:
        self._elementos: deque[Paciente] = deque()

    def push(self, paciente: Paciente) -> None:
        self._elementos.append(paciente)

    def pop(self) -> Paciente | None:
        return self._elementos.pop() if self._elementos else None

    def peek(self) -> Paciente | None:
        return self._elementos[-1] if self._elementos else None

    def es_vacia(self) -> bool:
        return not self._elementos

    def __len__(self) -> int:
        return len(self._elementos)

    def pacientes_prioritarios(self) -> list[Paciente]:
        """Listado de pacientes"""
        return list(reversed(self._elementos))

    def construir_pila_desde_lista(self, lista_pacientes: list[Paciente]) -> None:
        elegibles = [c for c in lista_pacientes
                     if c.estado == "Pendiente"
                     and c.tipo_atencion == "Extraccion"
                     and c.prioridad == "Urgente"]
        elegibles.sort(key=lambda c: c.fecha)
        self._elementos.clear()
        for paciente in reversed(elegibles):
            self.push(paciente)

    def generar_informe(self) -> None:
        print("\n=== REPORTE DE CONTINGENCIA ===")
        print("Criterio: Extracción + prioridad urgente + estado pendiente.")
        pacientes = self.pacientes_prioritarios()
        if not pacientes:
            print("No hay pacientes en contingencia")
            return
        for numero, paciente in enumerate(pacientes, 1):
            print(f"Pacientes Prioritarios {numero}: {paciente}")
