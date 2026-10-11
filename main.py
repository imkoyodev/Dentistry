"""
Interfaz de terminal basada en Click.
"""

import click
from datetime import date, datetime
from paciente import Paciente
from cola_atencion import ColaAtencion
from pila_contingencia import PilaContingencia

TIPOS_ATENCION = {"1": "Limpieza", "2": "Calzas",
                  "3": "Extraccion", "4": "Diagnostico",
                  }


class ConsultorioOdontologico:
    """Coordina el registro y las estructuras de atención en memoria."""

    def __init__(self) -> None:
        self.lista_general: list[Paciente] = []
        self.pila_contingencia = PilaContingencia()
        self.cola_atencion = ColaAtencion()

    @staticmethod
    def _leer_fecha() -> date:
        """Solicita una fecha válida en formato DD/MM/AAAA."""
        while True:
            entrada = click.prompt("Fecha de la cita (DD/MM/AAAA)", type=str).strip()
            try:
                fecha = datetime.strptime(entrada, "%d/%m/%Y").date()
            except ValueError:
                click.secho("Fecha inválida. Use el formato DD/MM/AAAA.", fg="red")
                continue
            if fecha < date.today():
                click.secho("La fecha no puede ser anterior a hoy.", fg="red")
                continue
            return fecha

    def registrar_paciente(self) -> None:
        click.secho("\n--- REGISTRO DE CLIENTE ---", bold=True)
        cedula = click.prompt("Cédula (7-10 dígitos)").strip()
        if not cedula.isdigit() or not 7 <= len(cedula) <= 10:
            raise click.ClickException("Cédula inválida: debe contener entre 7 y 10 dígitos.")
        if any(c.cedula == cedula and c.estado == "Pendiente" for c in self.lista_general):
            raise click.ClickException("El paciente ya tiene una cita pendiente registrada.")

        nombre = click.prompt("Nombre completo").strip()
        if len(nombre) < 3 or not all(ch.isalpha() or ch.isspace() for ch in nombre):
            raise click.ClickException("Nombre inválido: use al menos 3 caracteres, solo letras y espacios.")

        telefono = click.prompt("Teléfono (10 dígitos)").strip()
        if not telefono.isdigit() or len(telefono) != 10:
            raise click.ClickException("Teléfono inválido: debe contener exactamente 10 dígitos.")

        click.echo("Tipo de atención:")
        for numero, tipo in TIPOS_ATENCION.items():
            click.echo(f"  {numero}. {tipo.capitalize()}")
        tipo_opcion = click.prompt("Seleccione el tipo (1-4)", type=click.Choice(list(TIPOS_ATENCION)))

        prioridad_opcion = click.prompt(
            "Prioridad", type=click.Choice(["1", "2"]), value_proc=lambda value: value,
            show_choices=False, prompt_suffix=" (1 = Normal, 2 = Urgente): "
        )
        prioridad = "Urgente" if prioridad_opcion == "2" else "Normal"
        fecha = self._leer_fecha()

        paciente = Paciente(cedula, nombre, telefono, TIPOS_ATENCION[tipo_opcion], prioridad, fecha)
        self.lista_general.append(paciente)
        self.cola_atencion.enqueue(paciente)
        click.secho(f"Paciente {nombre} registrado correctamente.", fg="green")

    def procesar_pila_contingencia(self) -> None:
        self.pila_contingencia.construir_pila_desde_lista(self.lista_general)
        self.pila_contingencia.generar_informe()

    def atender_siguiente_contingencia(self) -> None:
        self.pila_contingencia.construir_pila_desde_lista(self.lista_general)
        paciente = self.pila_contingencia.peek()
        if paciente is None:
            click.echo("Sin procedimientos de extracción pendientes")
            return
        click.echo(f"Siguiente contingencia: {paciente}")
        if not click.confirm("Validar atención?", default=False):
            click.echo("Atención cancelada - Paciente en espera")
            return
        atendido = self.pila_contingencia.pop()
        if atendido is not None:
            atendido.estado = "Atendido"
            self.cola_atencion.remove(atendido)
            click.secho(f"Paciente {atendido.nombre} atendido por contingencia.", fg="green")

    def atender_siguiente_cola(self) -> None:
        paciente = self.cola_atencion.peek()
        if paciente is None:
            click.echo("No hay pacientes en espera")
            return
        click.echo(f"Siguiente turno: {paciente}")
        if not click.confirm("¿Confirmar atención?", default=False):
            click.echo("Turno sin cambios.")
            return
        atendido = self.cola_atencion.dequeue()
        if atendido is not None:
            atendido.estado = "Atendido"
            click.secho(f"Paciente {atendido.nombre} atendido.", fg="green")

    def mostrar_pacientes(self) -> None:
        if not self.lista_general:
            click.echo("No hay pacientes registrados.")
            return
        click.secho("\n=== CLIENTES REGISTRADOS ===", bold=True)
        for paciente in self.lista_general:
            click.echo(str(paciente))

    def ejecutar_menu(self) -> None:
        """Mantiene una sesión interactiva para conservar el estado en memoria."""
        opciones = {
            "1": ("Registro de pacientes", self.registrar_paciente),
            "2": ("Agenda diaria", self.cola_atencion.mostrar_agenda),
            "3": ("Atender siguiente paciente", self.atender_siguiente_cola),
            "4": ("Generar informe de contingencia", self.procesar_pila_contingencia),
            "5": ("Atender siguiente urgente", self.atender_siguiente_contingencia),
            "6": ("Listar todos los pacientes", self.mostrar_pacientes),
            "7": ("Salir", None),
        }
        while True:
            click.secho("\n=== CONSULTORIO ODONTOLÓGICO ===", fg="cyan", bold=True)
            for numero, (descripcion, _) in opciones.items():
                click.echo(f"{numero}. {descripcion}")
            opcion = click.prompt("Seleccione una opción", type=click.Choice(list(opciones)))
            if opcion == "7":
                click.echo("Hasta pronto.")
                return
            accion = opciones[opcion][1]
            if accion is not None:
                try:
                    accion()
                except click.ClickException as exc:
                    click.secho(f"Error: {exc.message}", fg="red", err=True)


@click.command()
@click.version_option(version="2.0.0", prog_name="consultorio-odontologico")
def main() -> None:
    """Administra pacientes, agenda FIFO y pila de contingencia LIFO."""
    sistema = ConsultorioOdontologico()
    try:
        sistema.ejecutar_menu()
    except (KeyboardInterrupt, click.Abort):
        click.echo("\nOperación cancelada. Hasta pronto.")


if __name__ == "__main__":
    main()
