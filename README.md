# Proyecto Airflow - Procesamiento de un .csv 

Práctica - Apache Airflow con Docker

## Descripción

Este proyecto implementa un pipeline de datos usando Apache Airflow para procesar datos de empleados. Los datos se descargan desde un CSV externo, se cargan en una base de datos PostgreSQL temporal y luego se hace un merge a la tabla final.

## Requisitos

- Visual Studio con extensión WSL
- Docker desktop
- Docker Compose
- Git

## Configuración Inicial

### Variables de Entorno

Este proyecto usa variables de entorno para gestionar información sensible de forma segura. **Nunca subas el archivo `.env` a GitHub**.

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita el archivo `.env` y actualiza los valores:
   - `AIRFLOW__CORE__FERNET_KEY`: Genera una nueva clave con:
     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```
   - Cambia todas las contraseñas por valores seguros
   - Ajusta `AIRFLOW_UID` si estás en Linux (ejecuta `id -u`)

3. El archivo `.env` está en `.gitignore` para proteger tus credenciales

## Cómo ejecutar

### 1. Levantar los servicios

```bash
docker-compose up -d
```

### 2. Acceder a Airflow

Una vez que los contenedores estén corriendo, abre tu navegador en:

```
http://localhost:8080
```

- **Usuario:** airflow
- **Contraseña:** airflow

### 3. Configurar la conexión a PostgreSQL

En la interfaz de Airflow:
1. Ve a Admin → Connections
2. Crea una conexión con ID: `tutorial_pg_conn`
3. Configura los datos de PostgreSQL

### 4. Ejecutar los DAGs

Primero ejecuta el DAG `create_tables_dag` para crear las tablas necesarias, y después ejecuta `process_employees` para procesar los datos.

## Estructura del Proyecto

```
tarea_2_4_airflow/
├── docker-compose.yaml      # Configuración de contenedores
├── config/
│   └── airflow.cfg          # Configuración de Airflow
├── dags/
│   ├── create_tables_dag.py # DAG para crear tablas
│   ├── create_tables.sql    # Script SQL de creación
│   ├── process_employees.py # DAG principal de procesamiento
│   ├── merge_employees.sql  # Script SQL de merge
│   └── files/
│       └── employees.csv    # Datos descargados
├── logs/                    # Logs de Airflow
└── plugins/                 # Plugins personalizados
```

## DAGs Incluidos

### create_tables_dag
Crea las tablas necesarias en PostgreSQL:
- `employees_temp` (tabla temporal)
- `employees` (tabla final)

### process_employees
Pipeline completo de procesamiento:
1. **get_data**: Descarga el CSV desde GitHub y lo carga en la tabla temporal
2. **merge_employees**: Hace un merge de datos desde la tabla temporal a la final

## Comandos Útiles

```bash
# Ver logs de todos los contenedores
docker-compose logs -f

# Parar los servicios
docker-compose down

# Reiniciar desde cero (borra volúmenes)
docker-compose down -v
```

## Notas

- Los DAGs están configurados para ejecutarse manualmente (`schedule=None`)
- El proyecto usa PostgreSQL como base de datos
- Los datos de ejemplo vienen del repositorio oficial de Airflow

-------------------------------------------------------------------

**Autor:** Adrián Ginel Mañas
