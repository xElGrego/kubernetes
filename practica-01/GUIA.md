# 📖 Guía Paso a Paso - Despliegue Manual en Kubernetes

Esta guía te llevará paso a paso por el proceso completo de desplegar los microservicios en Kubernetes, ejecutando cada comando manualmente para que entiendas exactamente qué hace cada parte.

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ Python 3.13 o superior instalado
- ✅ Docker Desktop con Kubernetes habilitado (o Minikube)
- ✅ kubectl instalado y configurado

---

## 🎯 Paso 1: Crear Entornos Virtuales

### 1.1 Crear entorno virtual para Users API

```powershell
# Navegar al directorio de users-api
cd users-api

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Desactivar entorno virtual
deactivate

# Volver al directorio raíz
cd ..
```

**¿Qué hace esto?**

- Crea un entorno virtual aislado para las dependencias de Python
- Instala FastAPI, Uvicorn y Pydantic específicos para este servicio
- Evita conflictos con otras versiones de paquetes en tu sistema

---

### 1.2 Crear entorno virtual para Orders API

```powershell
# Navegar al directorio de orders-api
cd orders-api

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Desactivar entorno virtual
deactivate

# Volver al directorio raíz
cd ..
```

**¿Qué hace esto?**

- Similar al anterior, pero incluye `httpx` para hacer requests HTTP
- `httpx` es lo que permite a Orders API comunicarse con Users API

---

## 🐳 Paso 2: Construir Imágenes Docker

### 2.1 Construir imagen de Users API

```powershell
# Navegar al directorio de users-api
cd users-api

# Construir la imagen Docker
docker build -t users-api:latest .

# Verificar que la imagen se creó
docker images | Select-String "users-api"

# Volver al directorio raíz
cd ..
```

**¿Qué hace esto?**

- `docker build`: Construye una imagen Docker
- `-t users-api:latest`: Etiqueta (tag) la imagen como "users-api" versión "latest"
- `.`: Usa el Dockerfile en el directorio actual
- La imagen contiene Python, las dependencias y el código de la API

**Detalles del Dockerfile:**

1. Usa Python 3.13 slim (versión ligera)
2. Copia requirements.txt e instala dependencias
3. Copia el código main.py
4. Expone el puerto 8000
5. Define el comando para ejecutar uvicorn

---

### 2.2 Construir imagen de Orders API

```powershell
# Navegar al directorio de orders-api
cd orders-api

# Construir la imagen Docker
docker build -t orders-api:latest .

# Verificar que la imagen se creó
docker images | Select-String "orders-api"

# Volver al directorio raíz
cd ..
```

**¿Qué hace esto?**

- Igual que el anterior, pero para Orders API
- Esta imagen incluye httpx para comunicarse con Users API

---

### 2.3 Verificar ambas imágenes

```powershell
# Ver todas las imágenes creadas
docker images
```

Deberías ver algo como:

```
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
orders-api    latest    abc123def456   2 minutes ago    180MB
users-api     latest    def456abc789   5 minutes ago    175MB
```

---

## ☸️ Paso 3: Desplegar en Kubernetes

### 3.1 Crear el Namespace

```powershell
# Aplicar el manifiesto del namespace
kubectl apply -f k8s/namespace.yaml

# Verificar que se creó
kubectl get namespaces
```

**¿Qué hace esto?**

- Crea un namespace llamado `ecommerce-platform`
- Los namespaces aíslan recursos dentro del cluster
- Es como tener un "proyecto" separado dentro de Kubernetes

**Salida esperada:**

```
namespace/ecommerce-platform created
```

---

### 3.2 Desplegar Users API - Deployment

```powershell
# Aplicar el deployment de users-api
kubectl apply -f k8s/users-api-deployment.yaml

# Ver el deployment
kubectl get deployments -n ecommerce-platform

# Ver los pods que se están creando
kubectl get pods -n ecommerce-platform
```

**¿Qué hace esto?**

- Crea un Deployment que gestiona 2 réplicas de users-api
- Kubernetes creará 2 pods con la imagen `users-api:latest`
- Si un pod falla, Kubernetes lo recreará automáticamente

**Salida esperada:**

```
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
users-api   2/2     2            2           30s
```

---

### 3.3 Desplegar Users API - Service

```powershell
# Aplicar el service de users-api
kubectl apply -f k8s/users-api-service.yaml

# Ver el service
kubectl get services -n ecommerce-platform
```

**¿Qué hace esto?**

- Crea un Service tipo ClusterIP
- Asigna el nombre DNS `users-api` dentro del cluster
- Balancea el tráfico entre las 2 réplicas
- **IMPORTANTE**: Solo accesible DENTRO del cluster (no desde tu máquina)

**Salida esperada:**

```
NAME        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
users-api   ClusterIP   10.96.123.45    <none>        8000/TCP   10s
```

---

### 3.4 Desplegar Orders API - Deployment

```powershell
# Aplicar el deployment de orders-api
kubectl apply -f k8s/orders-api-deployment.yaml

# Ver el deployment
kubectl get deployments -n ecommerce-platform

# Ver todos los pods
kubectl get pods -n ecommerce-platform
```

**¿Qué hace esto?**

- Crea un Deployment con 2 réplicas de orders-api
- Incluye la variable de entorno `USERS_API_URL=http://users-api:8000`
- Esta variable le dice a Orders API cómo encontrar Users API usando DNS

**Salida esperada:**

```
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
orders-api   2/2     2            2           20s
users-api    2/2     2            2           2m
```

---

### 3.5 Desplegar Orders API - Service

```powershell
# Aplicar el service de orders-api
kubectl apply -f k8s/orders-api-service.yaml

# Ver todos los services
kubectl get services -n ecommerce-platform
```

**¿Qué hace esto?**

- Crea un Service tipo NodePort
- Asigna un puerto en el rango 30000-32767
- **IMPORTANTE**: Este SÍ es accesible desde tu máquina local

**Salida esperada:**

```
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
orders-api   NodePort    10.96.234.56    <none>        8000:31733/TCP   5s
users-api    ClusterIP   10.96.123.45    <none>        8000/TCP         2m
```

En este ejemplo, el NodePort es `31733` (el tuyo será diferente).

---

### 3.6 Verificar que todo está corriendo

```powershell
# Ver todos los recursos en el namespace
kubectl get all -n ecommerce-platform
```

**Salida esperada:**

```
NAME                              READY   STATUS    RESTARTS   AGE
pod/orders-api-xxxxx-yyyyy        1/1     Running   0          1m
pod/orders-api-xxxxx-zzzzz        1/1     Running   0          1m
pod/users-api-aaaaa-bbbbb         1/1     Running   0          3m
pod/users-api-aaaaa-ccccc         1/1     Running   0          3m

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/orders-api   NodePort    10.96.234.56    <none>        8000:31733/TCP   1m
service/users-api    ClusterIP   10.96.123.45    <none>        8000/TCP         3m

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/orders-api   2/2     2            2           1m
deployment.apps/users-api    2/2     2            2           3m
```

---

## 🧪 Paso 4: Probar la Comunicación DNS

### 4.1 Obtener el NodePort

```powershell
# Obtener el NodePort de orders-api
kubectl get service orders-api -n ecommerce-platform
```

Anota el número de puerto después de `8000:` (ejemplo: 31733).

---

### 4.2 Probar Health Check de Orders API

```powershell
# Reemplaza 31733 con tu NodePort
curl http://localhost:31733/health
```

**¿Qué esperar?**

```json
{
  "service": "orders-api",
  "status": "healthy",
  "total_orders": 5,
  "users_api_connection": "healthy",
  "users_api_url": "http://users-api:8000",
  "timestamp": "2024-12-07T05:02:00"
}
```

**¡Fíjate!** `users_api_connection: "healthy"` significa que Orders API puede comunicarse con Users API vía DNS.

---

### 4.3 Probar endpoint simple

```powershell
# Listar todos los pedidos
curl http://localhost:31733/orders
```

**Respuesta esperada:**

```json
[
  {
    "id": 101,
    "user_id": 1,
    "product": "Laptop Dell XPS",
    "quantity": 1,
    "total": 1299.99,
    "status": "delivered",
    "created_at": "2024-05-01"
  },
  ...
]
```

---

### 4.4 🎯 DEMOSTRACIÓN DE DNS: Pedido con información de usuario

Este es el endpoint más importante que demuestra la comunicación DNS:

```powershell
# Obtener pedido 101 con información del usuario
curl http://localhost:31733/orders/101/details
```

**Respuesta esperada:**

```json
{
  "order": {
    "id": 101,
    "user_id": 1,
    "product": "Laptop Dell XPS",
    "quantity": 1,
    "total": 1299.99,
    "status": "delivered",
    "created_at": "2024-05-01"
  },
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "role": "customer",
    "created_at": "2024-01-15"
  }
}
```

**¿Qué pasó aquí?**

1. Tu navegador/curl hizo request a `http://localhost:31733/orders/101/details`
2. Kubernetes enrutó la petición a uno de los pods de Orders API
3. Orders API vio que necesita info del usuario con ID 1
4. Orders API hizo request interno a `http://users-api:8000/users/1`
5. Kubernetes DNS resolvió `users-api` a la IP del Service de Users API
6. El Service balanceó la carga a uno de los 2 pods de Users API
7. Users API respondió con la información del usuario
8. Orders API combinó los datos y te los devolvió

**¡Esto es comunicación entre microservicios vía DNS de Kubernetes!**

---

### 4.5 Probar con diferentes usuarios

```powershell
# Usuario 2
curl http://localhost:31733/orders/102/details

# Ver todos los pedidos del usuario 1
curl http://localhost:31733/orders/user/1/full
```

---

## 🔍 Paso 5: Inspeccionar el Sistema

### 5.1 Ver logs de Users API

```powershell
# Ver logs de todos los pods de users-api
kubectl logs -n ecommerce-platform -l app=users-api --tail=50
```

**¿Qué verás?**

- Requests recibidos desde Orders API
- Formato: `GET /users/1` cuando Orders API consulta información

---

### 5.2 Ver logs de Orders API

```powershell
# Ver logs de todos los pods de orders-api
kubectl logs -n ecommerce-platform -l app=orders-api --tail=50
```

**¿Qué verás?**

- Requests que tú haces desde el navegador
- Requests que Orders API hace a Users API internamente

---

### 5.3 Ver logs en tiempo real

```powershell
# Seguir logs de orders-api en tiempo real
kubectl logs -n ecommerce-platform -l app=orders-api -f
```

Ahora haz un request desde otra terminal:

```powershell
curl http://localhost:31733/orders/101/details
```

Verás los logs aparecer en tiempo real. Presiona `Ctrl+C` para salir.

---

### 5.4 Ejecutar comandos dentro de un pod

```powershell
# Listar todos los pods
kubectl get pods -n ecommerce-platform

# Copiar el nombre de un pod de orders-api (ejemplo: orders-api-xxxxx-yyyyy)
# Ejecutar shell interactivo dentro del pod
kubectl exec -it -n ecommerce-platform orders-api-xxxxx-yyyyy -- /bin/sh
```

Ahora estás DENTRO del contenedor. Prueba:

```sh
# Probar DNS interno desde dentro del pod
curl http://users-api:8000/health

# Ver variables de entorno
env | grep USERS_API_URL

# Salir del pod
exit
```

**¿Qué demuestra esto?**

- Desde dentro del pod, puedes acceder a `users-api` directamente
- El DNS de Kubernetes funciona automáticamente
- La variable de entorno está configurada correctamente

---

### 5.5 Verificar resolución DNS

```powershell
# Desde un pod de orders-api, verificar que DNS resuelve users-api
kubectl exec -n ecommerce-platform orders-api-xxxxx-yyyyy -- nslookup users-api
```

**Salida esperada:**

```
Server:    10.96.0.10
Address:   10.96.0.10:53

Name:      users-api.ecommerce-platform.svc.cluster.local
Address:   10.96.123.45
```

**¿Qué significa?**

- `users-api` se resuelve a `users-api.ecommerce-platform.svc.cluster.local`
- La IP es la del Service ClusterIP (10.96.123.45 en este ejemplo)

---

## 🎓 Paso 6: Experimentos para Aprender

### 6.1 Escalar réplicas

```powershell
# Escalar users-api a 3 réplicas
kubectl scale deployment users-api -n ecommerce-platform --replicas=3

# Ver los nuevos pods
kubectl get pods -n ecommerce-platform -l app=users-api

# Hacer varios requests y ver cómo se distribuyen
for ($i=1; $i -le 5; $i++) {
    curl http://localhost:31733/orders/101/details
}

# Ver logs de cada pod para ver cuál recibió requests
kubectl logs -n ecommerce-platform -l app=users-api --tail=10
```

**¿Qué aprendes?**

- El Service balancea automáticamente entre las 3 réplicas
- Kubernetes distribuye la carga

---

### 6.2 Simular fallo de un pod

```powershell
# Listar pods
kubectl get pods -n ecommerce-platform

# Eliminar un pod de users-api
kubectl delete pod users-api-xxxxx-yyyyy -n ecommerce-platform

# Inmediatamente ver los pods
kubectl get pods -n ecommerce-platform -w
```

**¿Qué observas?**

- Kubernetes detecta que falta un pod
- Automáticamente crea uno nuevo
- El Deployment mantiene siempre 3 réplicas (o las que configuraste)

---

### 6.3 Ver eventos del namespace

```powershell
# Ver eventos recientes
kubectl get events -n ecommerce-platform --sort-by='.lastTimestamp'
```

**¿Qué verás?**

- Creación de pods
- Asignación de IPs
- Problemas si los hay (ImagePullBackOff, CrashLoopBackOff, etc.)

---

### 6.4 Describir un recurso

```powershell
# Ver detalles completos de un deployment
kubectl describe deployment users-api -n ecommerce-platform

# Ver detalles de un service
kubectl describe service users-api -n ecommerce-platform

# Ver detalles de un pod
kubectl describe pod users-api-xxxxx-yyyyy -n ecommerce-platform
```

**¿Qué información obtienes?**

- Configuración completa
- Estado actual
- Eventos relacionados
- Problemas si los hay

---

## 🧹 Paso 7: Limpieza

### 7.1 Eliminar recursos uno por uno (para aprender)

```powershell
# Eliminar service de orders-api
kubectl delete service orders-api -n ecommerce-platform

# Eliminar deployment de orders-api
kubectl delete deployment orders-api -n ecommerce-platform

# Eliminar service de users-api
kubectl delete service users-api -n ecommerce-platform

# Eliminar deployment de users-api
kubectl delete deployment users-api -n ecommerce-platform

# Verificar que no quedan recursos
kubectl get all -n ecommerce-platform

# Eliminar el namespace
kubectl delete namespace ecommerce-platform
```

---

### 7.2 Eliminar todo de una vez (método rápido)

```powershell
# Eliminar el namespace (elimina todo dentro)
kubectl delete namespace ecommerce-platform

# Verificar que se eliminó
kubectl get namespaces
```

---

## 📚 Conceptos Clave que Aprendiste

### 1. **Namespace**

- Aísla recursos dentro del cluster
- Permite tener múltiples proyectos en el mismo cluster
- Formato DNS: `<service>.<namespace>.svc.cluster.local`

### 2. **DNS Interno de Kubernetes**

- Cada Service obtiene un nombre DNS automáticamente
- Formato completo: `users-api.ecommerce-platform.svc.cluster.local`
- Forma corta (mismo namespace): `users-api`
- Permite comunicación entre servicios sin conocer IPs

### 3. **Service Types**

#### ClusterIP (Users API)

- Solo accesible DENTRO del cluster
- Perfecto para comunicación interna
- No expuesto al exterior
- Balancea carga entre pods

#### NodePort (Orders API)

- Accesible desde FUERA del cluster
- Kubernetes asigna puerto 30000-32767
- Útil para desarrollo y pruebas
- En producción se usa LoadBalancer o Ingress

### 4. **Deployments**

- Gestiona réplicas de pods
- Auto-recuperación si un pod falla
- Permite actualizaciones rolling
- Mantiene el estado deseado

### 5. **Health Checks**

#### Liveness Probe

- ¿El contenedor está vivo?
- Si falla → Kubernetes reinicia el pod

#### Readiness Probe

- ¿El contenedor está listo para tráfico?
- Si falla → Kubernetes no envía tráfico

---

## 🎯 Próximos Pasos

1. **Modificar el código**: Cambia un endpoint y reconstruye la imagen
2. **Agregar ConfigMaps**: Externaliza configuración
3. **Agregar Secrets**: Maneja información sensible
4. **Implementar Ingress**: Exponer servicios con nombres de dominio
5. **Agregar base de datos**: Usar Persistent Volumes
6. **Implementar HPA**: Auto-escalado basado en CPU/memoria

---

**¡Felicidades!** 🎉 Ahora entiendes cómo funcionan los microservicios en Kubernetes y cómo se comunican vía DNS interno.
