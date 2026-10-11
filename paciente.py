from dataclasses import dataclass, field
from datetime import date, datetime

DATE_FORMAT = "%d/%m/%Y"

@dataclass
class Paciente:
    cedula: str
    nombre: str
    telefono: str
    tipo_atencion: str
    prioridad: str
    fecha: date | str
    estado: str = field(default="Pendiente")

    def __post_init__(self) -> None:
        self.cedula = str(self.cedula).strip()
        self.nombre = self.nombre.strip()
        self.telefono = str(self.telefono).strip()
        self.tipo_atencion = self.tipo_atencion.strip().capitalize()
        self.prioridad = self.prioridad.strip().capitalize()
        if isinstance(self.fecha, str):
            self.fecha = datetime.strptime(self.fecha, DATE_FORMAT).date()

    @property
    def fecha_dt(self) -> date:        
        return self.fecha

    @property
    def fecha_str(self) -> str:
        return self.fecha.strftime(DATE_FORMAT)

    def __str__(self) -> str:
        return (f"Cédula: {self.cedula} | Nombre Paciente: {self.nombre} | Tel.: {self.telefono} | "
                f"Atención: {self.tipo_atencion.capitalize()} | Prioridad: {self.prioridad} | "
                f"Fecha: {self.fecha_str} | Estado: {self.estado}")
