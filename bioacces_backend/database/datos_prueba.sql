-- ============================================================
-- Sistema BioAccess - Datos de prueba
-- Ejecutar DESPUÉS de esquema_bioacces.sql, en la base "bioacces"
-- ============================================================

USE bioacces;

-- ============ roles ============
INSERT INTO roles (nombre_rol) VALUES
('Administrador');

-- ============ usuarios_administrative ============
-- Usuario: admin | Contraseña: admin123
-- (el hash ya está generado con bcrypt, así el login funciona tal cual al importar)
INSERT INTO usuarios_administrative (usuario, password_hash, nombre_completo, documento, correo_electronico, fecha_creacion, estado, id_role) VALUES
('admin', '$2b$12$0zwJ6lgP1yOpoS5lsFEAduE5Ks33FlGN8vN.v73mYpVbFV1c86iRS', 'Administrador de Prueba', '1000000001', 'admin@bioaccess.test', NOW(), TRUE, 1);

-- ============ areas ============
INSERT INTO areas (nombre_area) VALUES
('Administrativo'),
('Gestión Humana');

-- ============ horarios ============
INSERT INTO horarios (nombre_turno, hora_entrada, hora_inicio_desayuno, hora_fin_desayuno, hora_inicio_almuerzo, hora_fin_almuerzo, hora_salida, tiempo_almuerzo_permitido, estado) VALUES
('Jornada Mañana', '07:00:00', '09:00:00', '09:15:00', '12:00:00', '13:00:00', '16:00:00', 60, TRUE);

-- ============ funcionarios ============
-- 3 funcionarios de ejemplo, cubriendo las 2 áreas y el horario de arriba
INSERT INTO funcionarios (id_funcionario, nombres, apellidos, cargo, categoria, telefono, correo_electronico, genero, fecha_ingreso, huella_template, id_area, id_horario, estado, observaciones) VALUES
('1000000101', 'Carlos', 'Pérez', 'Auxiliar Administrativo', 'Administrativo', '3001234567', 'carlos.perez@bioaccess.test', 'Masculino', '2026-01-15', NULL, 1, 1, TRUE, NULL),
('1000000102', 'Jefferson', 'Gonzales Hurtado', 'Analista de Gestión Humana', 'Administrativo', '3007654321', 'jefferson.gonzales@bioaccess.test', 'Masculino', '2026-02-01', NULL, 2, 1, TRUE, NULL),
('1000000103', 'Linda Maria', 'Contreras Pulgarin', 'Coordinadora de Gestión Humana', 'Administrativo', '3009876543', 'linda.contreras@bioaccess.test', 'Femenino', '2026-02-10', NULL, 2, 1, TRUE, NULL);

-- ============ configuraciones ============
-- Una sola fila con datos institucionales de ejemplo (fecha_ultimo_backup queda en NULL a propósito)
INSERT INTO configuraciones (nombre_institucion, nit_institucion, ruta_backup_local, minutos_tolerancia_entrada, correo_notificaciones, fecha_ultimo_backup) VALUES
('INPEC - Sede Ipiales', '900000000-1', 'C:\\BioAccess\\Backups', 10, 'notificaciones@bioaccess.test', NULL);
