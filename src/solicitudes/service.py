from .model import Solicitud
from .repository import RepositorioSolicitudes
ESTADOS = {"pendiente", "en_revision", "resuelta"}
PRIORIDADES = {"baja", "media", "alta"}
class SolicitudNoEncontrada(LookupError): pass
class ServicioSolicitudes:
    def __init__(self, repositorio: RepositorioSolicitudes): self.repositorio = repositorio
    def registrar(self, estudiante, tipo, prioridad, descripcion):
        estudiante, tipo, descripcion = estudiante.strip(), tipo.strip(), descripcion.strip()
        if not estudiante or not tipo or not descripcion: raise ValueError("Completá estudiante, tipo y descripción")
        prioridad = prioridad.strip().lower()
        if prioridad not in PRIORIDADES: raise ValueError("Prioridad inválida")
        actuales = self.repositorio.listar()
        nuevo = Solicitud(max((s.id for s in actuales), default=0)+1, estudiante, tipo, prioridad, descripcion)
        self.repositorio.guardar([*actuales, nuevo])
        return nuevo
    def _actualizar(self, ident, **cambios):
        actuales = self.repositorio.listar()
        for solicitud in actuales:
            if solicitud.id == ident:
                for clave, valor in cambios.items(): setattr(solicitud, clave, valor)
                self.repositorio.guardar(actuales)
                return solicitud
        raise SolicitudNoEncontrada(f"No existe la solicitud {ident}")
    def asignar(self, ident, responsable):
        responsable = responsable.strip()
        if not responsable: raise ValueError("El responsable no puede quedar vacío")
        return self._actualizar(ident, responsable=responsable)
    def cambiar_estado(self, ident, estado):
        estado = estado.strip().lower()
        if estado not in ESTADOS: raise ValueError("Estado inválido")
        return self._actualizar(ident, estado=estado)
    def buscar(self, estado=None, tipo=None):
        return [s for s in self.repositorio.listar() if (estado is None or s.estado == estado) and (tipo is None or s.tipo.casefold() == tipo.casefold())]
    def resumen(self):
        solicitudes = self.repositorio.listar()
        return {**{estado: sum(s.estado == estado for s in solicitudes) for estado in sorted(ESTADOS)}, "total": len(solicitudes)}
