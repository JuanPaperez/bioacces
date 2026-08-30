-- ============================================================
-- Sistema BioAccess - Esquema completo (MySQL / XAMPP)
-- Recrea las 12 tablas desde cero, con relaciones y ON DELETE RESTRICT
-- ============================================================

CREATE DATABASE IF NOT EXISTS bioacces;
USE bioacces;

-- Se borran en orden inverso a las dependencias, para poder recrear limpio
DROP TABLE IF EXISTS auditoria_logs;
DROP TABLE IF EXISTS configuraciones;
DROP TABLE IF EXISTS historial_horarios;
DROP TABLE IF EXISTS registros_acceso;
DROP TABLE IF EXISTS asistencia_movimientos;
DROP TABLE IF EXISTS permisos_justificaciones;
DROP TABLE IF EXISTS asistencias;
DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS horarios;
DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS usuarios_administrative;
DROP TABLE IF EXISTS roles;

-- ============ roles ============
CREATE TABLE roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

-- ============ usuarios_administrative ============
CREATE TABLE usuarios_administrative (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    documento VARCHAR(20) NOT NULL,
    correo_electronico VARCHAR(100),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    id_role INT NOT NULL,
    CONSTRAINT fk_admin_role FOREIGN KEY (id_role) REFERENCES roles(id_role) ON DELETE RESTRICT
);

-- ============ areas ============
CREATE TABLE areas (
    id_area INT AUTO_INCREMENT PRIMARY KEY,
    nombre_area VARCHAR(100) NOT NULL
);

-- ============ horarios ============
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_turno VARCHAR(50) NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_inicio_desayuno TIME,
    hora_fin_desayuno TIME,
    hora_inicio_almuerzo TIME,
    hora_fin_almuerzo TIME,
    hora_salida TIME NOT NULL,
    tiempo_almuerzo_permitido INT,
    estado BOOLEAN DEFAULT TRUE
);

-- ============ funcionarios ============
CREATE TABLE funcionarios (
    id_funcionario VARCHAR(20) PRIMARY KEY COMMENT 'documento de la persona',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cargo VARCHAR(80),
    categoria VARCHAR(50) COMMENT 'Funcionario / Visitante / Vigilancia / Administrativo',
    telefono VARCHAR(20),
    correo_electronico VARCHAR(100),
    genero VARCHAR(20),
    fecha_ingreso DATE,
    huella_template TEXT,
    id_area INT NOT NULL,
    id_horario INT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    CONSTRAINT fk_funcionario_area FOREIGN KEY (id_area) REFERENCES areas(id_area) ON DELETE RESTRICT,
    CONSTRAINT fk_funcionario_horario FOREIGN KEY (id_horario) REFERENCES horarios(id_horario) ON DELETE RESTRICT
);

-- ============ asistencias ============
CREATE TABLE asistencias (
    id_asistencia BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora_primera_entrada TIME,
    hora_ultima_salida TIME,
    minutos_trabajados INT COMMENT 'calculado sumando cada par entrada/salida del día',
    minutos_retraso INT,
    alerta_estado VARCHAR(30) COMMENT 'Ej: A tiempo / Tarde / Ausente',
    CONSTRAINT fk_asistencia_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE RESTRICT
);

-- ============ permisos_justificaciones ============
CREATE TABLE permisos_justificaciones (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario VARCHAR(20) NOT NULL,
    fecha_permiso DATE NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    tipo_novedad VARCHAR(100),
    descripcion_justificacion TEXT,
    estado VARCHAR(20) COMMENT 'Aprobado / Pendiente',
    aprobado_por INT NULL COMMENT 'opcional: vacío mientras el permiso esté Pendiente',
    CONSTRAINT fk_permiso_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE RESTRICT,
    CONSTRAINT fk_permiso_aprobador FOREIGN KEY (aprobado_por) REFERENCES usuarios_administrative(id_usuario) ON DELETE RESTRICT
);

-- ============ asistencia_movimientos ============
CREATE TABLE asistencia_movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_asistencia BIGINT NOT NULL,
    tipo VARCHAR(10) COMMENT 'entrada / salida',
    hora TIME NOT NULL,
    motivo VARCHAR(100) COMMENT 'Ej: Jornada, Almuerzo, Permiso médico',
    id_permiso INT NULL COMMENT 'opcional: solo si esta salida/entrada corresponde a un permiso',
    CONSTRAINT fk_movimiento_asistencia FOREIGN KEY (id_asistencia) REFERENCES asistencias(id_asistencia) ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_permiso FOREIGN KEY (id_permiso) REFERENCES permisos_justificaciones(id_permiso) ON DELETE RESTRICT
);

-- ============ registros_acceso ============
CREATE TABLE registros_acceso (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    tipo_acceso VARCHAR(50) COMMENT 'Ej: Huella Digital',
    estado VARCHAR(20) COMMENT 'Permitido / Denegado',
    codigo_registro VARCHAR(20) COMMENT 'Ej: ACC-00001',
    CONSTRAINT fk_registro_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE RESTRICT
);

-- ============ historial_horarios ============
CREATE TABLE historial_horarios (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario VARCHAR(20) NOT NULL,
    id_horario_anterior INT NULL COMMENT 'opcional: vacío si es la primera asignación de horario del funcionario',
    id_horario_nuevo INT NOT NULL,
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(255),
    modificado_por INT NOT NULL,
    CONSTRAINT fk_historial_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE RESTRICT,
    CONSTRAINT fk_historial_horario_anterior FOREIGN KEY (id_horario_anterior) REFERENCES horarios(id_horario) ON DELETE RESTRICT,
    CONSTRAINT fk_historial_horario_nuevo FOREIGN KEY (id_horario_nuevo) REFERENCES horarios(id_horario) ON DELETE RESTRICT,
    CONSTRAINT fk_historial_modificador FOREIGN KEY (modificado_por) REFERENCES usuarios_administrative(id_usuario) ON DELETE RESTRICT
);

-- ============ configuraciones ============
CREATE TABLE configuraciones (
    id_config INT AUTO_INCREMENT PRIMARY KEY,
    nombre_institucion VARCHAR(150),
    nit_institucion VARCHAR(20),
    ruta_backup_local VARCHAR(255),
    minutos_tolerancia_entrada INT,
    correo_notificaciones VARCHAR(100),
    fecha_ultimo_backup DATETIME NULL
);

-- ============ auditoria_logs ============
CREATE TABLE auditoria_logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    tipo_accion VARCHAR(50),
    detalle_cambio TEXT,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_log_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios_administrative(id_usuario) ON DELETE RESTRICT
);
