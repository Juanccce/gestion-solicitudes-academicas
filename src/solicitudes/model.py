from dataclasses import asdict, dataclass
@dataclass
class Solicitud:
    id: int
    estudiante: str
    tipo: str
    prioridad: str
    descripcion: str
    responsable: str = ""
    estado: str = "pendiente"
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, data): return cls(**data)
