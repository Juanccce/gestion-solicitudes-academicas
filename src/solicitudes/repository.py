import json
from pathlib import Path
from typing import Protocol
from .model import Solicitud
class RepositorioSolicitudes(Protocol):
    def listar(self) -> list[Solicitud]: ...
    def guardar(self, solicitudes: list[Solicitud]) -> None: ...
class RepositorioJson:
    def __init__(self, ruta: Path): self.ruta = ruta
    def listar(self):
        if not self.ruta.exists(): return []
        try: datos = json.loads(self.ruta.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: raise ValueError("El archivo JSON está dañado") from exc
        return [Solicitud.from_dict(item) for item in datos]
    def guardar(self, solicitudes):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        datos = json.dumps([s.to_dict() for s in solicitudes], ensure_ascii=False, indent=2)
        self.ruta.write_text(datos + "\n", encoding="utf-8")
