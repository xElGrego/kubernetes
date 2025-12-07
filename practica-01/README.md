# 🚀 Kubernetes Microservices - E-commerce Platform

Proyecto de práctica de Kubernetes que demuestra la **comunicación entre microservicios** usando **DNS interno** dentro de un namespace dedicado.

## 📋 Descripción del Proyecto

Este proyecto implementa dos microservicios FastAPI que se comunican entre sí dentro de un cluster de Kubernetes:

- **Users API** 👥: Servicio de gestión de usuarios
- **Orders API** 🛒: Servicio de pedidos que consulta información de usuarios internamente

### 🎯 Conceptos de Kubernetes Demostrados

✅ **Namespaces**: Aislamiento de recursos en `ecommerce-platform`  
✅ **DNS Interno**: Comunicación entre servicios usando nombres de servicio  
✅ **Deployments**: Gestión de réplicas y actualizaciones  
✅ **Services**: ClusterIP para comunicación interna, NodePort para acceso externo  
✅ **Health Checks**: Liveness y Readiness probes  
✅ **Resource Limits**: Gestión de CPU y memoria

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│         Namespace: ecommerce-platform                   │
│                                                         │
│  ┌──────────────┐              ┌──────────────┐       │
│  │  Users API   │◄─────────────│  Orders API  │       │
│  │  (ClusterIP) │   DNS interno│  (NodePort)  │       │
│  │              │ users-api:8000│              │       │
│  │  2 replicas  │              │  2 replicas  │       │
│  └──────────────┘              └──────────────┘       │
│                                        ▲               │
└────────────────────────────────────────┼───────────────┘
                                         │
                                    localhost:30XXX
                                    (acceso externo)
```

### 🔄 Flujo de Comunicación

1. Cliente hace request a `Orders API` via NodePort
2. `Orders API` necesita información de usuario
3. `Orders API` llama a `Users API` usando DNS: `http://users-api:8000`
4. Kubernetes resuelve el DNS al Service ClusterIP de `Users API`
5. El Service balancea la carga entre las 2 réplicas de `Users API`
6. `Orders API` recibe la respuesta y la combina con datos de pedidos

---

## 📁 Estructura del Proyecto

```
practica-01/
├── users-api/              # Microservicio de usuarios
│   ├── main.py            # API FastAPI
│   ├── requirements.txt   # Dependencias Python
│   ├── Dockerfile         # Imagen Docker
│   └── .gitignore
│
├── orders-api/            # Microservicio de pedidos
│   ├── main.py           # API FastAPI (llama a users-api)
│   ├── requirements.txt  # Dependencias Python (incluye httpx)
│   ├── Dockerfile        # Imagen Docker
│   └── .gitignore
│
├── k8s/                   # Manifiestos de Kubernetes
│   ├── namespace.yaml                # Namespace ecommerce-platform
│   ├── users-api-deployment.yaml     # Deployment Users API
│   ├── users-api-service.yaml        # Service ClusterIP
│   ├── orders-api-deployment.yaml    # Deployment Orders API
│   └── orders-api-service.yaml       # Service NodePort
│
├── setup-env.ps1          # Script para crear entornos virtuales
├── build-images.ps1       # Script para construir imágenes Docker
├── deploy.ps1             # Script para desplegar en Kubernetes
├── cleanup.ps1            # Script para limpiar recursos
└── README.md              # Este archivo
```

---

## 🚀 Guía de Inicio Rápido

### Prerrequisitos

- Python 3.12+ (recomendado 3.13)
- Docker Desktop (con Kubernetes habilitado) o Minikube
- kubectl configurado

### Paso 1: Crear Entornos Virtuales

```powershell
# Ejecutar desde la raíz del proyecto
.\setup-env.ps1
```

Este script creará entornos virtuales para ambos microservicios e instalará las dependencias.

### Paso 2: Construir Imágenes Docker

```powershell
.\build-images.ps1
```

Construye las imágenes Docker `users-api:latest` y `orders-api:latest`.

### Paso 3: Desplegar en Kubernetes

```powershell
.\deploy.ps1
```

Este script:

- Crea el namespace `ecommerce-platform`
- Despliega ambos microservicios
- Espera a que los pods estén listos
- Muestra el NodePort para acceder a Orders API

### Paso 4: Verificar el Despliegue

```powershell
# Ver todos los recursos
kubectl get all -n ecommerce-platform

# Ver logs de Users API
kubectl logs -n ecommerce-platform -l app=users-api --tail=50

# Ver logs de Orders API
kubectl logs -n ecommerce-platform -l app=orders-api --tail=50
```

---

## 🧪 Probar la Comunicación DNS

Una vez desplegado, obtén el NodePort:

```powershell
kubectl get service orders-api -n ecommerce-platform
```

### Endpoints de Users API (solo accesible internamente)

```bash
# Health check
http://users-api:8000/

# Listar todos los usuarios
http://users-api:8000/users

# Obtener usuario específico
http://users-api:8000/users/1
```

### Endpoints de Orders API (accesible externamente)

Reemplaza `<NODEPORT>` con el puerto asignado (ej: 30123):

```bash
# Health check (muestra conectividad con users-api)
curl http://localhost:<NODEPORT>/health

# Listar todos los pedidos
curl http://localhost:<NODEPORT>/orders

# Obtener pedido específico
curl http://localhost:<NODEPORT>/orders/101

# 🎯 DEMOSTRACIÓN DE DNS: Pedido con información de usuario
curl http://localhost:<NODEPORT>/orders/101/details

# 🎯 DEMOSTRACIÓN DE DNS: Todos los pedidos de un usuario
curl http://localhost:<NODEPORT>/orders/user/1/full
```

### 🔍 Ejemplo de Respuesta con DNS

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

**¡Nota!** La información del usuario proviene de `users-api` a través de DNS interno de Kubernetes.

---

## 🔧 Desarrollo Local (sin Kubernetes)

### Ejecutar Users API localmente

```powershell
cd users-api
.\venv\Scripts\Activate.ps1
python main.py
# Disponible en http://localhost:8000
```

### Ejecutar Orders API localmente

```powershell
cd orders-api
.\venv\Scripts\Activate.ps1
# Configurar URL de users-api
$env:USERS_API_URL = "http://localhost:8000"
python main.py
# Disponible en http://localhost:8000 (cambiar puerto si es necesario)
```

---

## 🐛 Debugging

### Ver logs en tiempo real

```powershell
# Users API
kubectl logs -n ecommerce-platform -l app=users-api -f

# Orders API
kubectl logs -n ecommerce-platform -l app=orders-api -f
```

### Ejecutar comandos dentro de un pod

```powershell
# Obtener nombre de un pod
kubectl get pods -n ecommerce-platform

# Ejecutar shell interactivo
kubectl exec -it -n ecommerce-platform <POD_NAME> -- /bin/sh

# Probar DNS desde dentro del pod
kubectl exec -it -n ecommerce-platform <ORDERS_POD_NAME> -- curl http://users-api:8000/health
```

### Verificar DNS interno

```powershell
# Desde un pod de orders-api, verificar que puede resolver users-api
kubectl exec -it -n ecommerce-platform <ORDERS_POD_NAME> -- nslookup users-api
```

---

## 🧹 Limpieza

Para eliminar todos los recursos:

```powershell
.\cleanup.ps1
```

O manualmente:

```powershell
kubectl delete namespace ecommerce-platform
```

---

## 📚 Conceptos Clave de Kubernetes

### 1. **Namespace**

Aísla recursos lógicamente dentro del cluster. En este proyecto usamos `ecommerce-platform`.

### 2. **DNS Interno**

Kubernetes proporciona DNS automático para los Services:

- Formato: `<service-name>.<namespace>.svc.cluster.local`
- Forma corta (mismo namespace): `<service-name>`
- En este proyecto: `http://users-api:8000`

### 3. **Service Types**

#### ClusterIP (Users API)

- Solo accesible dentro del cluster
- Ideal para comunicación interna entre microservicios
- No expuesto externamente

#### NodePort (Orders API)

- Accesible desde fuera del cluster
- Kubernetes asigna un puerto en el rango 30000-32767
- Útil para desarrollo y pruebas

### 4. **Deployments**

- Gestiona réplicas de pods
- Permite actualizaciones rolling
- Auto-recuperación si un pod falla

### 5. **Health Checks**

#### Liveness Probe

- Verifica si el contenedor está vivo
- Kubernetes reinicia el pod si falla

#### Readiness Probe

- Verifica si el contenedor está listo para recibir tráfico
- Kubernetes no envía tráfico si falla

---

## 🎓 Ejercicios de Aprendizaje

1. **Escalar réplicas**: Cambia el número de réplicas a 3 y observa el balanceo de carga
2. **Simular fallo**: Elimina un pod y observa cómo Kubernetes lo recrea automáticamente
3. **Agregar nuevo endpoint**: Crea un nuevo endpoint en Orders API que consulte Users API
4. **Cambiar a LoadBalancer**: Modifica el Service de Orders API a tipo LoadBalancer (si tu cluster lo soporta)
5. **Agregar ConfigMap**: Externaliza la URL de users-api usando un ConfigMap

---

## 🔗 Recursos Adicionales

- [Documentación de Kubernetes](https://kubernetes.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)

---

## 📝 Notas

- Las imágenes Docker usan `imagePullPolicy: Never` para desarrollo local
- En producción, usa un registry (Docker Hub, GCR, ECR, etc.)
- Los datos son simulados en memoria, se pierden al reiniciar los pods
- Para persistencia, considera usar bases de datos con Persistent Volumes

---

**¡Feliz aprendizaje de Kubernetes!** 🎉
