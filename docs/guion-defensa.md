# Guion orientativo para la defensa

Duración sugerida: 10 a 15 minutos. Todos los integrantes deben aparecer con cámara encendida y explicar una parte con sus propias palabras. Completar los nombres y repartirse los bloques antes de grabar. No leer todo de corrido: usar este guion como ayuda.

## 0:00-1:00 | Presentación
Cada integrante dice su nombre. Presentamos un prototipo didáctico de gestión de solicitudes académicas con datos ficticios.

## 1:00-3:00 | Problema y alcance
Explicar alta, asignación, cambio de estado, búsqueda y reporte. Aclarar que usa JSON local y no está preparado para trámites reales, usuarios simultáneos ni permisos.

## 3:00-5:00 | Diagnóstico
Mostrar baseline/legacy_app.py. Elegir dos o tres smells para explicar: método que hace de todo, manejo que oculta excepciones y escritura JSON duplicada. Señalar que el informe enumera diez hallazgos y da su impacto.

## 5:00-8:00 | Refactoring y demo
Mostrar el modelo, servicio, repositorio y CLI. Ejecutar alta, listado, asignación, transición y resumen. Explicar una validación y cómo se informa un ID inexistente. Comparar el flujo de estado de la versión inicial con cambiar_estado y _actualizar.

## 8:00-10:00 | Pruebas
Ejecutar python -m unittest discover -s tests -v. Explicar qué comprueban los casos y que usan almacenamiento temporal. Mostrar docs/evidencia-ejecucion.txt como registro adicional.

## 10:00-12:00 | Code review y límites
Mencionar separación de responsabilidades, errores explícitos y límites de JSON. Proponer base de datos, auditoría, roles y backups como trabajo futuro antes de un uso institucional.

## Cierre
Resumir qué mejoró y qué queda pendiente. Cada integrante debe poder responder preguntas sobre el código que presenta.
