# Guía Definitiva: Pruebas de Carga con Karate y Gatling

Esta guía está diseñada para llevarte desde cero hasta la ejecución de pruebas de estrés profesionales utilizando dos de las herramientas más potentes del mercado: **Karate** y **Gatling**.

---

## 1. ¿Qué estamos haciendo y por qué?

### Conceptos Básicos

- **Pruebas de Carga (Load Testing)**: Consiste en simular múltiples usuarios usando tu aplicación al mismo tiempo para ver cómo se comporta. ¿Se pone lenta? ¿Se cae?
- **Karate**: Es una herramienta para probar APIs. Usas un lenguaje casi humano (Gherkin) para decir "Ve a esta URL y espera un código 200". Es muy fácil de leer.
- **Gatling**: Es una "bestia" de rendimiento. Está diseñada para generar miles de peticiones por segundo.
- **La Combinación**: Usamos **Karate** para definir _qué_ probar (la lógica del negocio) y **Gatling** para definir _cuánto_ probar (la intensidad). ¡Lo mejor de los dos mundos!

---

## 2. Estructura del Proyecto

Tu proyecto de pruebas vive en `tests/performance`. Aquí está la magia explicada archivo por archivo:

### A. `pom.xml` (El Cerebro)

Es el archivo de configuración de Maven. Aquí le decimos a Java: "Necesito descargar Karate y Gatling para que esto funcione". No necesitas tocarlo mucho, salvo para actualizar versiones.

### B. `users.feature` (El Escenario)

Ubicación: `src/test/java/performance/users.feature`
Este archivo define **una sola interacción** de un usuario.

```gherkin
Feature: Users API Load Test

  Background:
    # Definimos la URL base. En pruebas locales usamos localhost.
    * url 'http://localhost:8000'

  Scenario: Health Check
    # Pasos simples: Ve a /health, usa GET, espera un 200 OK.
    Given path 'health'
    When method get
    Then status 200
```

### C. `UsersSimulation.scala` (La Intensidad)

Ubicación: `src/test/scala/performance/UsersSimulation.scala`
Aquí es donde Gatling toma el control. Definimos **cómo** vamos a atacar al API.

```scala
// 1. Definimos el escenario (usamos el archivo feature de arriba)
val users = scenario("Users API Load Test")
  .exec(karateFeature("classpath:performance/users.feature"))

// 2. Definimos la inyección de usuarios (La Carga)
setUp(
  users.inject(
      // Calentamiento: Sube de 0 a 10 usuarios en 10 segundos
      rampUsers(10) during (10 seconds),
      // Fuego a discreción: Mantiene 100 usuarios por segundo constantes
      constantUsersPerSec(100) during (60 seconds)
  ).protocols(protocol)
)
```

---

## 3. Cómo Ejecutar la Prueba (Paso a Paso)

### Paso 1: Preparar el Terreno (Port Forwarding)

Como tu API vive dentro de Kubernetes, tu computadora no puede verla directamente. Necesitamos abrir un "túnel".

Abre una terminal y ejecuta:

```bash
kubectl port-forward svc/users-api -n ecommerce-platform 8000:8000
```

_Déjala abierta. Esto conecta tu puerto 8000 local con el puerto 8000 del servicio en el clúster._

### Paso 2: Disparar la Prueba

Abre **otra** terminal, ve a la carpeta de pruebas y ejecuta Maven:

```bash
cd tests/performance
mvn clean test-compile gatling:test
```

- `clean`: Borra resultados anteriores.
- `test-compile`: Compila el código de prueba.
- `gatling:test`: Ejecuta la simulación.

---

## 4. Interpretando los Resultados

Cuando termine, verás algo así en la consola:

```text
---- Requests ------------------------------------------------------------------
> Global                                                   (OK=6010   KO=0     )
> GET /health                                              (OK=6010   KO=0     )
```

- **OK**: Peticiones exitosas.
- **KO**: Fallos (errores 500, timeouts, etc.). Si tienes KO, ¡algo va mal en tu API!

### El Reporte HTML

Al final, te dará una ruta como:
`.../target/gatling/userssimulation-20251207.../index.html`

Abre ese archivo en tu navegador. Verás gráficas increíbles sobre:

- **Latencia**: ¿Cuánto tardó en responder el API?
- **Peticiones/segundo**: ¿Cuánta carga real soportó?

---

## 5. Cómo Implementarlo en Otras APIs

Para probar otro servicio (ej. `orders-api`), sigue estos pasos:

1.  **Crea un nuevo Feature**:
    Copia `users.feature` a `orders.feature`. Cambia el `path` a la ruta que quieras probar (ej. `/orders`).

2.  **Crea una nueva Simulación**:
    Copia `UsersSimulation.scala` a `OrdersSimulation.scala`.

    - Cambia el nombre de la clase: `class OrdersSimulation extends Simulation`.
    - Apunta al nuevo feature: `.exec(karateFeature("classpath:performance/orders.feature"))`.

3.  **Ejecuta**:
    Maven detectará automáticamente la nueva simulación y te preguntará cuál quieres correr, o correrá ambas si lo configuras.

---

## 6. Pipeline de Pruebas Avanzado

Hemos configurado un pipeline completo con 4 tipos de pruebas para el endpoint `/orders`. Aquí te explico qué es cada una y cómo ejecutarla:

### A. Smoke Test (Prueba de Humo)

- **Concepto**: Una prueba rápida y ligera (1 usuario) solo para verificar que el sistema "enciende" y responde. Se corre después de cada despliegue.
- **Comando**:
  ```bash
  mvn clean test-compile gatling:test "-Dgatling.simulationClass=performance.OrdersSmokeTest"
  ```

### B. Stress Test (Prueba de Estrés)

- **Concepto**: Aumenta la carga progresivamente hasta encontrar el punto de quiebre del sistema.
- **Perfil**: Sube de 0 a 200 usuarios en 2 minutos.
- **Comando**:
  ```bash
  mvn clean test-compile gatling:test "-Dgatling.simulationClass=performance.OrdersStressTest"
  ```

### C. Spike Test (Prueba de Pico)

- **Concepto**: Simula un aumento repentino y masivo de tráfico (ej. una oferta flash) para ver si el sistema se recupera o colapsa.
- **Perfil**: Carga baja -> Pico de 500 usuarios -> Carga baja.
- **Comando**:
  ```bash
  mvn clean test-compile gatling:test "-Dgatling.simulationClass=performance.OrdersSpikeTest"
  ```

### D. Soak Test (Prueba de Resistencia/Remojo)

- **Concepto**: Mantiene una carga moderada constante durante un largo periodo (ej. horas) para detectar fugas de memoria o problemas de recursos a largo plazo.
- **Perfil**: 50 usuarios constantes por 5 minutos (en demo).
- **Comando**:
  ```bash
  mvn clean test-compile gatling:test "-Dgatling.simulationClass=performance.OrdersSoakTest"
  ```

---

## 7. Glosario de Inyección de Carga (Gatling)

Para diseñar tus propias pruebas, necesitas entender las instrucciones que definen cómo llegan los usuarios virtuales. Aquí tienes las más importantes:

### `atOnceUsers(n)`

- **Qué hace**: Inyecta `n` usuarios de golpe, al mismo tiempo.
- **Uso**: Ideal para **Smoke Tests** (verificar que funciona) o para simular un **Spike** (pico) repentino.
- **Ejemplo**: `atOnceUsers(1)` (1 usuario inmediato).

### `rampUsers(n) during (duration)`

- **Qué hace**: Inyecta `n` usuarios distribuidos linealmente durante un periodo de tiempo.
- **Uso**: Para calentar el sistema o subir la carga suavemente.
- **Ejemplo**: `rampUsers(10) during (10 seconds)` (Empieza con pocos y termina inyectando más rápido hasta completar 10 usuarios en 10 seg).

### `constantUsersPerSec(rate) during (duration)`

- **Qué hace**: Mantiene un flujo constante de `rate` usuarios por segundo.
- **Uso**: Para **Soak Tests** (carga constante) o para simular tráfico normal sostenido.
- **Ejemplo**: `constantUsersPerSec(50) during (5 minutes)` (50 usuarios nuevos CADA segundo durante 5 minutos).

### `rampUsersPerSec(rate1) to (rate2) during (duration)`

- **Qué hace**: Aumenta (o disminuye) la tasa de usuarios por segundo desde `rate1` hasta `rate2`.
- **Uso**: La mejor opción para **Stress Tests**. Te permite encontrar el punto exacto de quiebre aumentando la presión poco a poco.
- **Ejemplo**: `rampUsersPerSec(10) to (100) during (2 minutes)` (Empieza suave y termina muy agresivo).

### `nothingFor(duration)`

- **Qué hace**: No hace nada. Pausa la inyección.
- **Uso**: Útil para dejar "descansar" el sistema después de un pico y ver si se recupera (Cool-down).
- **Ejemplo**: `nothingFor(10 seconds)`.

### Ejemplo Combinado (Tu Stress Test Mejorado)

```scala
setUp(
  orders.inject(
    rampUsersPerSec(1) to 50 during (1.minute),      // 1. Calentamiento suave
    rampUsersPerSec(50) to 300 during (2.minutes),   // 2. Subida agresiva (Stress)
    constantUsersPerSec(300) during (1.minute),      // 3. Mantener la presión máxima
    rampUsersPerSec(300) to 50 during (30.seconds),  // 4. Enfriamiento
    nothingFor(10.seconds)                           // 5. Descanso final
  ).protocols(protocol)
)
```
