import tempfile, unittest
from pathlib import Path
from src.solicitudes.repository import RepositorioJson
from src.solicitudes.service import ServicioSolicitudes, SolicitudNoEncontrada
class ServicioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.s=ServicioSolicitudes(RepositorioJson(Path(self.tmp.name)/"data.json"))
    def tearDown(self): self.tmp.cleanup()
    def test_alta_persistencia(self):
        x=self.s.registrar(" Ana ","Inscripción","alta","Correlativa"); self.assertEqual((x.id,x.estudiante,x.estado),(1,"Ana","pendiente")); self.assertEqual(len(self.s.buscar()),1)
    def test_asignacion_y_transicion(self):
        self.s.registrar("Ana","Inscripción","media","Correlativa"); self.s.asignar(1,"Mesa"); x=self.s.cambiar_estado(1,"en_revision"); self.assertEqual((x.responsable,x.estado),("Mesa","en_revision"))
    def test_prioridad_invalida(self):
        with self.assertRaises(ValueError): self.s.registrar("Ana","X","urgente","Y")
    def test_campos_vacios(self):
        with self.assertRaises(ValueError): self.s.registrar(" ","X","media","Y")
    def test_estado_invalido(self):
        with self.assertRaises(ValueError): self.s.cambiar_estado(1,"cerrada")
    def test_id_inexistente(self):
        with self.assertRaises(SolicitudNoEncontrada): self.s.asignar(99,"Mesa")
    def test_filtro_tipo_sin_distinguir_mayusculas(self):
        self.s.registrar("Ana","Inscripción","baja","X"); self.assertEqual(len(self.s.buscar(tipo="inscripción")),1)
    def test_resumen(self):
        self.s.registrar("Ana","X","media","Y"); self.s.cambiar_estado(1,"resuelta"); self.assertEqual(self.s.resumen()["resuelta"],1)
if __name__=="__main__": unittest.main()
