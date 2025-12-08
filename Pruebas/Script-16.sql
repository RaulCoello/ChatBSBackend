-- crear tabla para el data_set del clima por zonas greograficas y meses
CREATE TABLE clima_mensual (
    id SERIAL PRIMARY KEY,
    estacion VARCHAR(20),
    nombre_estacion VARCHAR(200),
    longitud NUMERIC,
    latitud NUMERIC,
    altitud NUMERIC,
    anio INT,
    mes INT,
    temperatura NUMERIC,
    fecha DATE
);


-- select * from clima_mensual

/*

	select * from clima_mensual cm where cm.nombre_estacion ilike '%QUEVEDO%' order by cm.anio, cm.mes

*/