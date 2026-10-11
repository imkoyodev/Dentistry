import unittest
from datetime import date
from paciente import Paciente
from cola_atencion import ColaAtencion
from pila_contingencia import PilaContingencia


def paciente(cedula, fecha, tipo="Extraccion", prioridad="Urgente", estado="Pendiente"):
    return Paciente(cedula, f"Paciente {cedula}", "3001234567", tipo, prioridad, date.fromisoformat(fecha), estado)

class TestColaAtencion(unittest.TestCase):
    def test_fifo_y_cola_vacia(self):
        a, b = paciente("1111111", "2026-11-01"), paciente("2222222", "2026-11-02")
        cola = ColaAtencion([a, b])
        self.assertIs(cola.peek(), a)
        self.assertIs(cola.dequeue(), a)
        self.assertIs(cola.dequeue(), b)
        self.assertIsNone(cola.dequeue())

    def test_remover_paciente_de_contingencia(self):
        a, b = paciente("1111111", "2026-11-01"), paciente("2222222", "2026-11-02")
        cola = ColaAtencion([a, b])
        self.assertTrue(cola.remove(b))
        self.assertFalse(cola.remove(b))
        self.assertEqual(cola.pacientes(), [a])

class TestPilaContingencia(unittest.TestCase):
    def test_filtra_y_prioriza_fecha_mas_cercana(self):
        cercana = paciente("1111111", "2026-10-15", tipo="Extraccion",)
        lejana = paciente("2222222", "2026-12-15", tipo="Extraccion",)
        no_extraccion = paciente("3333333", "2026-10-11", tipo="Limpieza")
        no_urgente = paciente("4444444", "2026-10-12", prioridad="Normal")
        atendido = paciente("5555555", "2026-10-13", estado="Atendido")
        pila = PilaContingencia()
        pila.construir_pila_desde_lista([lejana, no_extraccion, no_urgente, atendido, cercana])
        self.assertEqual(pila.pacientes_prioritarios(), [cercana, lejana])
        self.assertIs(pila.peek(), cercana)
        self.assertIs(pila.pop(), cercana)
        self.assertIs(pila.pop(), lejana)
        self.assertIsNone(pila.pop())

if __name__ == "__main__":
    unittest.main()
