from collections import deque
from typing import Iterable
from paciente import Paciente

class ColaAtencion:
    def __init__(self, pacientes: Iterable[Paciente] = ()) -> None:
        self._cola: deque[Paciente] = deque(pacientes)

    def enqueue(self, paciente: Paciente) -> None:
        self._cola.append(paciente)

    def dequeue(self) -> Paciente | None:
        return self._cola.popleft() if self._cola else None

    def peek(self) -> Paciente | None:
        return self._cola[0] if self._cola else None

    def remove(self, paciente: Paciente) -> bool:
        try:
            self._cola.remove(paciente)
            return True
        except ValueError:
            return False

    def es_vacia(self) -> bool:
        return not self._cola

    def __len__(self) -> int:
        return len(self._cola)

    def pacientes(self) -> list[Paciente]:        
        return list(self._cola)

    def mostrar_agenda(self) -> None:
        print("\n=== AGENDA DE ATENCIÓN ===")
        pacientes = self.pacientes()
        if not pacientes:
            print("Sin pacientes en espera ..")
            return
        for turno, paciente in enumerate(pacientes, 1):
            print(f"Turno {turno}: {paciente}")
