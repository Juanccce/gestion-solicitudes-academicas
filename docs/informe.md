# Trabajo Práctico Integrador
## Evolución profesional de un sistema existente
### Gestión de Solicitudes Académicas

Metodología de Sistemas II · Tecnicatura Universitaria en Programación a Distancia · UTN
Integrantes: completar con nombres del grupo
Fecha: 10 de noviembre de 2026

> Prototipo didáctico con información ficticia. No es un sistema institucional ni debe utilizarse para gestionar trámites reales.

## Resumen ejecutivo

Este trabajo toma un prototipo de consola para registrar solicitudes de estudiantes y lo mejora desde el punto de vista de su mantenimiento. La primera versión permitía dar de alta solicitudes, asignar responsables, cambiar estados, buscar y emitir un resumen, pero concentraba todo en una clase y guardaba los datos desde cada operación. También ocultaba cualquier error de lectura como si no hubiera solicitudes.

La versión final separa el modelo, las reglas del servicio, el repositorio JSON y la interfaz de consola. Se agregaron validaciones y errores claros. El diagnóstico registra diez code smells y se aplicaron refactorings para separar responsabilidades, centralizar valores permitidos, mejorar la identificación de registros y hacer la persistencia reemplazable. El proyecto incluye ocho pruebas automatizadas. El formato JSON resulta suficiente para una demostración individual; concurrencia, auditoría, permisos y resguardo de datos quedan fuera de este alcance.

## 1. Sistema base y alcance

El caso es un sistema de gestión de solicitudes académicas, como sugiere la consigna. Una solicitud tiene identificador, estudiante, tipo, prioridad, descripción, responsable y estado. Las operaciones disponibles son alta, asignación, cambio de estado, listado con filtros y reporte por estado. Se usan tres estados: pendiente, en revisión y resuelta; y tres prioridades: baja, media y alta.

El sistema guarda un archivo JSON local. No incluye inicio de sesión, roles, notificaciones, interfaz web ni integración con servicios de la UTN. Los nombres usados en los ejemplos son ficticios. La versión inicial deliberadamente defectuosa se mantiene en baseline/legacy_app.py y la versión refactorizada se encuentra en src/solicitudes/.

## 2. Calidad externa e interna

En términos externos, los flujos del prototipo son acotados y se ejecutan desde comandos reconocibles. La persona puede registrar una solicitud y luego seguirla por su ID. Para el alcance de una práctica, esa interfaz permite demostrar las operaciones. Como limitación, quien la usa debe conocer las categorías y estados válidos; no hay una pantalla guiada ni mensajes de ayuda para completar una solicitud paso a paso.

La principal debilidad estaba en la calidad interna. La clase inicial se ocupaba de reglas de negocio, manipulación de datos, lectura y escritura del archivo y armado del reporte. Eso volvía difícil cambiar una regla sin afectar otros caminos. Los errores de JSON se ocultaban. En la versión final, el servicio coordina reglas, el repositorio se ocupa de persistir y el modelo representa una solicitud. La consola solamente interpreta argumentos y muestra resultados. Esta separación facilita mantener el código y probar las reglas sin depender de la interfaz.

## 3. Deuda técnica y code smells

El diagnóstico se hizo mediante lectura del código inicial y revisión de los flujos solicitados. Los impactos son cualitativos y se priorizan para este prototipo; no son resultados de una herramienta estática.

1. **Objeto con demasiadas responsabilidades.** Sistema.hacer_todo atiende alta, asignación, cambios de estado, búsqueda y reporte. Un cambio de persistencia puede afectar operaciones que no tienen relación. Riesgo alto.
2. **Método extenso con muchos caminos.** hacer_todo recibe una acción y toma decisiones para todos los casos. Es difícil aislar cada camino y revisar qué sucede ante errores. Riesgo alto.
3. **Obsesión por tipos primitivos.** Acción, estado, prioridad y tipo se representan con cadenas sueltas. Un valor escrito de otra manera puede avanzar sin validación. Riesgo alto.
4. **Valores mágicos repetidos.** Las cadenas pendiente, en_revision y resuelta aparecen en el flujo de reporte y actualización sin un conjunto central de estados admitidos. Sumar un estado exige revisar manualmente varios lugares. Riesgo medio.
5. **Persistencia duplicada.** El alta y las modificaciones escriben el archivo con bloques similares. Si cambia el formato o el tratamiento de errores, hay que acordarse de corregir cada bloque. Riesgo alto.
6. **Error ignorado.** La captura genérica de excepciones hace que un archivo JSON corrupto parezca un archivo vacío. Se pierde información diagnóstica y la aplicación podría dar una impresión equivocada. Riesgo alto.
7. **Ruta global fija.** La constante DATA acopla la clase al lugar donde vive el archivo. Dificulta usar almacenamiento temporal en pruebas o cambiar el destino. Riesgo medio.
8. **Acoplamiento entre dominio y almacenamiento.** La lógica opera sobre diccionarios y conoce el detalle de guardado. Sustituir JSON por otra persistencia exige modificar los casos de uso. Riesgo alto.
9. **Identificador derivado de la cantidad de registros.** Usar longitud más uno puede reutilizar un identificador si alguna vez se elimina un elemento o quedan huecos. Riesgo medio.
10. **Conteo manual en el reporte.** Cada estado tiene su contador escrito a mano. Si aparece otro estado, puede no entrar en el reporte aunque sí exista en los datos. Riesgo medio.

## 4. Principios SOLID y Clean Code

Se dividieron las responsabilidades entre Solicitud, ServicioSolicitudes, RepositorioJson y cli.py. La capa de servicio depende del contrato RepositorioSolicitudes, de modo que la regla de negocio no exige que el almacenamiento sea JSON. La ruta se entrega al crear el repositorio en el punto de entrada.

Las validaciones de estado y prioridad se centralizan. Los campos obligatorios se recortan y se rechazan si quedan vacíos. Los errores para un ID inexistente y para un archivo JSON dañado son explícitos. Los nombres de las operaciones describen lo que hacen. Para un prototipo pequeño no agregamos patrones más complejos: la separación actual alcanza para mostrar el límite entre las capas.

## 5. Refactorings y comparación

Se aplicó Extract Class al dividir la clase inicial en módulos con responsabilidades distintas. Se extrajeron operaciones de registro, asignación, cambio de estado, búsqueda y resumen. Se reemplazaron valores dispersos por conjuntos de estados y prioridades. Se introdujo el objeto Solicitud para representar juntos los datos relacionados. Se encapsuló la lectura y escritura JSON en un repositorio. Para evitar colisiones ante huecos, el nuevo ID se calcula a partir del máximo ID existente más uno.

**Antes, versión inicial:** la operación de cambio recorría los diccionarios, actualizaba el estado, abría el archivo, escribía los datos y devolvía el registro dentro del mismo bloque. La operación de asignación repetía el patrón de guardado.

**Después, versión refactorizada:** cambiar_estado valida primero que el valor esté entre los estados admitidos y delega la actualización común a _actualizar. Ese método busca el registro y persiste la colección por medio del repositorio. Una transición válida conserva el mismo resultado observable; una transición inválida ahora se rechaza con un mensaje.

El cambio evita repetir el guardado en cada operación y deja las reglas de estado en un punto visible. No se eliminaron funciones del caso de uso; la mejora apunta a la organización, validación y facilidad de modificación.

## 6. Pruebas y verificación

El repositorio incluye ocho pruebas con unittest y almacenamiento temporal. Cubren alta y persistencia, asignación, transición, prioridad inválida, campos obligatorios vacíos, estado inválido, ID inexistente, búsqueda sin distinguir mayúsculas en el tipo y conteo del reporte. Para ejecutarlas desde la carpeta del proyecto: python -m unittest discover -s tests -v.

Los casos sirven para comparar el comportamiento esperado antes y después: el alta crea un registro pendiente; asignar solo actualiza responsable; cambiar de estado mantiene los demás datos; el filtro encuentra el tipo solicitado; y el resumen cuenta correctamente cada estado. La versión nueva también informa con claridad los datos inválidos y los identificadores inexistentes.

Se ejecutó la suite en el entorno de trabajo: las ocho pruebas finalizaron correctamente. También se ejecutaron los cinco comandos de demostración (alta, listado, asignación, transición y resumen) con datos ficticios; la salida real quedó registrada en docs/evidencia-ejecucion.txt. La carpeta tests usa un directorio temporal; los comandos de demostración dejaron un JSON de ejemplo dentro de data/. Para la entrega oral, conviene agregar capturas propias de la consola y del repositorio, además del registro de texto.

## 7. Revisión técnica

La revisión cubrió separación de responsabilidades, nombres, validación de entradas, errores de dominio, persistencia UTF-8, ubicación de la ruta y posibilidad de probar la lógica aislada. El checklist está en docs/code-review.md. El prototipo no implementa control de acceso, por lo que no debe almacenar solicitudes reales.

Hay límites conocidos. Un archivo JSON no gestiona escrituras simultáneas ni transacciones. El listado carga la colección completa en memoria. No existe auditoría del historial de estados, ni autenticación, permisos, copias de seguridad o proceso institucional de aprobación. Para uso real se debería elegir una base de datos, definir roles y revisar los requisitos de privacidad y operación.

## 8. Conclusiones y aprendizajes

La mejora principal fue hacer más claro dónde vive cada decisión. Separar persistencia y reglas hizo posible validar la lógica sin consola y comunicar errores que antes desaparecían. También se comprobó que no hace falta sumar funcionalidad para mejorar un sistema: ordenar el código y cubrir comportamientos ayuda a reducir el costo de cambios futuros.

JSON es una elección razonable para este ejemplo, no una recomendación para un sistema universitario real. Si el sistema tuviera varios usuarios o necesitara rastrear quién hizo cada cambio, habría que revisar la arquitectura antes de ampliarlo.

## Anexo A. Uso de inteligencia artificial

Se utilizó ChatGPT como apoyo para organizar el informe, considerar alternativas de estructura y revisar la redacción. La herramienta no reemplaza la autoría ni la defensa: quienes presentan deben revisar el código, comprender las decisiones y poder explicarlas. Se recomienda adjuntar a la entrega el intercambio relevante con la herramienta, según lo pide la consigna. No se atribuyen análisis a herramientas que no se ejecutaron ni se inventan resultados de pruebas.

## Anexo B. Evidencias para completar

Para la entrega oral, agregar capturas auténticas de: (1) ejecución de la suite unittest, (2) alta y listado desde consola, (3) repositorio con las versiones inicial y refactorizada, y (4) historial de commits. También completar nombres de integrantes y fecha de entrega. La salida real de pruebas y comandos está en docs/evidencia-ejecucion.txt; las capturas de pantalla quedan como tarea del grupo.
