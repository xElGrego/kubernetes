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

¡Y listo! Ya tienes un framework de pruebas de rendimiento profesional.
