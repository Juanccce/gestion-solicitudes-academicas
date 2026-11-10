# Defensa del TPI: guía de grabación paso a paso

**Duración objetivo:** 12 minutos (la cátedra sugiere 10 a 15). Todos los integrantes deben mostrar el rostro con cámara encendida y hablar con voz propia. No usar voz sintética. Repartan los bloques; si son menos de cuatro, junten bloques, pero asegúrense de que todos hablen y puedan explicar su parte.

## 1. Antes de grabar

1. Completen en el informe los nombres reales y la fecha de entrega.
2. Descarguen el ZIP para ejecutar el proyecto. Para conservar el historial Git, clonen también el bundle: desde una terminal, ejecuten git clone ruta-completa-a-gestion-solicitudes-academicas.bundle tp-ms2 y luego cd tp-ms2. El README explica cómo publicarlo.
3. Comprueben que Python 3.10 o posterior esté disponible: python --version.
4. En la carpeta del proyecto, corran python -m unittest discover -s tests -v. Revisen que aparezcan ocho líneas ok y al final Ran 8 tests y OK.
5. Para la demostración, limpien solo el archivo de ejemplo creado por el programa si existe: data/solicitudes.json. No borren el código. Al iniciar la demo desde cero, el primer ID será 1.
6. Abran la herramienta de videollamada o grabación elegida. Activen cámara y micrófono, compartan la pantalla con el código o la consola visible y acomoden las cámaras para que se vea la cara de cada participante. Hagan una prueba de audio de 10 segundos.
7. Cierren ventanas con notificaciones, datos privados o pestañas que no formen parte de la presentación. No usen nombres reales de estudiantes en la demo.

## 2. Reparto sugerido

- Integrante 1: presentación, problema y alcance (0:00-3:00).
- Integrante 2: versión inicial y diagnóstico (3:00-5:00).
- Integrante 3: arquitectura, refactoring y demostración (5:00-8:00).
- Integrante 4: pruebas, revisión técnica y cierre (8:00-12:00).

Si el grupo tiene dos integrantes, cada uno presenta dos bloques. Si tiene tres, una persona puede tomar introducción y cierre. Todos deben aparecer y participar.

## 3. Guion hablado, con tiempos

### 0:00-1:00 — Presentación

**Integrante 1:** “Hola, somos [nombres]. Vamos a presentar nuestro Trabajo Práctico Integrador de Metodología de Sistemas II. Tomamos un prototipo de gestión de solicitudes académicas y trabajamos sobre su calidad interna: primero identificamos problemas concretos y después reorganizamos el código sin cambiar el propósito de las operaciones.”

“Los datos que aparecen en la demostración son ficticios. Es un prototipo de aprendizaje, no un sistema conectado a la facultad.”

### 1:00-3:00 — Qué hace el sistema y hasta dónde llega

**Integrante 1:** “Una solicitud tiene un ID, estudiante, tipo, prioridad, descripción, responsable y estado. Desde la consola se puede registrar, asignar una persona, cambiar el estado, filtrar el listado y consultar un resumen. Los estados que usamos son pendiente, en revisión y resuelta.”

“Elegimos un archivo JSON porque alcanza para mostrar el flujo y no necesitamos dependencias externas. Tiene límites: no resuelve escrituras simultáneas, permisos, auditoría ni copias de seguridad. Por eso no se debe usar para trámites reales.”

### 3:00-5:00 — Versión inicial y diagnóstico

**Integrante 2:** “Esta es la versión inicial, guardada en baseline/legacy_app.py. La clase Sistema concentraba las operaciones. El método hacer_todo recibía una acción y, según el valor, registraba, asignaba, cambiaba el estado, buscaba o armaba el reporte.”

“Identificamos diez code smells. Por ejemplo, hay responsabilidades mezcladas, un método con demasiados caminos, valores de estado escritos directamente, escritura JSON duplicada y una excepción genérica que se ignora. Si el archivo se rompía, el programa podía tratarlo como una lista vacía y ocultar el problema.”

“Los riesgos del informe son cualitativos y pensados para este prototipo. No presentamos un análisis de una herramienta automática: el diagnóstico salió de leer el código y revisar los casos de uso.”

### 5:00-8:00 — Refactoring y demostración

**Integrante 3:** “En la versión final separamos cuatro partes. Solicitud representa los datos; ServicioSolicitudes aplica las reglas; RepositorioJson lee y guarda; y cli.py conecta los comandos con el servicio. Así, las reglas no dependen directamente del archivo JSON.”

“Por ejemplo, cambiar_estado valida que el estado sea permitido y después delega la actualización común. El repositorio guarda los cambios. También calculamos el ID a partir del máximo ID existente para evitar colisiones si hay huecos.”

Compartir la consola y ejecutar, uno por vez:

    python -m src.solicitudes.cli add --estudiante Ana --tipo Inscripcion --prioridad alta --descripcion Correlativa pendiente
    python -m src.solicitudes.cli list
    python -m src.solicitudes.cli assign 1 --responsable Mesa
    python -m src.solicitudes.cli transition 1 --estado en_revision
    python -m src.solicitudes.cli report

**Integrante 3:** “La primera operación registra la solicitud con estado pendiente. Después se asigna Mesa y se cambia a en revisión. En el resumen vemos una solicitud en revisión y ninguna pendiente. Los datos se guardan localmente en JSON.”

Mostrar brevemente src/solicitudes/service.py y repository.py. No hace falta leer cada línea: señalar la validación y la separación de responsabilidades.

### 8:00-10:00 — Pruebas

**Integrante 4:** “Las pruebas usan unittest y un directorio temporal, así que no escriben en los datos del usuario. Cubren alta y persistencia, asignación, transición, filtros, resumen y entradas inválidas.”

Ejecutar otra vez:

    python -m unittest discover -s tests -v

**Integrante 4:** “La ejecución terminó con ocho pruebas, todas en estado ok, y el resultado final OK. Son pruebas del comportamiento del servicio; no cubren concurrencia, seguridad institucional ni integraciones externas.”

### 10:00-11:00 — Code review y deuda pendiente

**Integrante 4:** “En la revisión miramos nombres, responsabilidades, validaciones, errores y persistencia. Dejamos un checklist en docs/code-review.md. Para pasar de prototipo a producción habría que agregar una base transaccional, roles, auditoría, backups y definir el circuito de aprobación.”

Mostrar el historial con:

    git log --oneline --decorate --all -10
    git tag --list

“Los tags permiten ubicar estado-inicial, estado-refactorizado y las etapas de diagnóstico, refactoring, pruebas y documentación.”

### 11:00-12:00 — Cierre

**Integrante 1 o todos por turno:** “La mejora no consistió en sumar pantallas. Reordenamos las responsabilidades, hicimos explícitos algunos errores y agregamos pruebas para poder cambiar el código con más confianza. La solución es deliberadamente chica y tiene límites claros.”

“Usamos ChatGPT como apoyo para ordenar el informe y revisar la redacción. Revisamos el material y podemos explicar las decisiones. Gracias.”

## 4. Cómo tomar las capturas para el anexo

Las capturas deben salir de la ejecución real en su computadora. Abran Recortes o la herramienta de captura de Windows y guarden tres PNG, procurando que se vean el comando, la salida y la carpeta o repositorio correctos.

1. **Pruebas:** ejecuten python -m unittest discover -s tests -v. Capturen desde el primer test hasta Ran 8 tests y OK. Guarden como Anexo_01_tests.png.
2. **Consola:** ejecuten los cinco comandos de demostración. Capturen el alta, el cambio a en_revision y el resumen. Guarden como Anexo_02_demo.png.
3. **Git:** ejecuten git log --oneline --decorate --all -10 y git tag --list. Capturen los commits por etapa y los seis tags. Guarden como Anexo_03_git.png. Si no caben juntos, hagan dos capturas.

Luego adjunten esas imágenes aquí. Con los archivos PNG puedo insertarlas en el PDF final con sus pies de imagen. No recreen la consola en un editor: la cátedra pidió capturas reales.

## 5. Revisión antes de entregar el video

- Duración entre 10 y 15 minutos.
- Se ven los rostros de todos y cada integrante habla.
- Audio claro y voz propia; nada de voz sintética.
- La pantalla muestra comandos y código legibles.
- La demo usa solo datos ficticios.
- Se muestran las pruebas y el historial Git.
- Guardan el video en un formato aceptado por la cátedra, lo reproducen desde el inicio hasta el final y verifican audio y duración antes de subirlo.
