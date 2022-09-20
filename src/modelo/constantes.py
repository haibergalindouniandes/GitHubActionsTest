# Clase que contiene constantes
class Constantes(object):
    
    # Script que permite hacer la limpieza de la tabla mantenimietos
    ELIMINAR_MANTENIMIENTOS = 'DELETE FROM Mantenimiento'
    # Script que permite hacer la limpieza de la tabla accion
    ELIMINAR_ACCIONES = 'DELETE FROM Accion'
    # Consulta que permite obtener las acciones asociadas a un Automovil con base al ID
    CONSULTA_ACCIONES_POR_AUTOMOVIL = 'SELECT a.id, a.kilometraje, a.valor, a.fecha, m.nombre AS mantenimiento FROM accion a INNER JOIN mantenimiento m ON a.mantenimiento_id = m.id  WHERE a.automovil_id = '

    # Consulta que permite obtener las acciones asociadas a un Automovil con base al ID por cada año
    CONSULTA_ACCIONES_POR_AUTOMOVIL_ANIO = "SELECT strftime('%Y', a.fecha) AS FECHA, SUM(a.valor) AS GASTOS FROM accion a WHERE a.automovil_id = {id_auto} GROUP BY strftime('%Y', a.fecha) ORDER BY a.fecha ;"

    # Consulta que permite obtener LOS GASTOS del ultimo mantenimiento realizad por cada accion por cada año
    CONSULTA_AGRUPADA_GASTOS_AUTOMOVIL_ANIO = "SELECT a.mantenimiento_id  as ID_MANTENIMIENTO, COUNT( a.mantenimiento_id) AS NUM_MANTENIMIENTO, a.valor  AS GASTOS  FROM accion a WHERE a.automovil_id = {id_auto} and strftime('%Y', a.fecha) = (SELECT strftime('%Y', a.fecha) AS FECHA  from accion a where a.automovil_id = {id_auto} order by a.fecha DESC LIMIT 1)  GROUP BY a.mantenimiento_id"

    # Consulta que permite obtener EL KILOMETRAJE INICIAL Y FINAL DEL del ultimo mantenimiento realizad en el ultimo año
    CONSULTA_AGRUPADA_KM_AUTOMOVIL_ANIO = "SELECT  (SELECT a.kilometraje  AS inicial  from accion a where a.automovil_id = {id_auto} and a.mantenimiento_id = {id_accion}  order by a.fecha ASC LIMIT 1) AS KM_INICIAL , (SELECT a.kilometraje  AS final  from accion a where a.automovil_id = {id_auto} and a.mantenimiento_id = {id_accion} order by a.fecha DESC  LIMIT 1) AS KM_FINAL FROM accion a WHERE a.automovil_id = {id_auto} and a.mantenimiento_id  = {id_accion} and strftime('%Y', a.fecha) = (SELECT strftime('%Y', a.fecha) AS FECHA  from accion a where a.automovil_id = {id_auto} order by a.fecha DESC LIMIT 1) limit 1"


def __setattr__(self, *_):
    raise Exception("Tried to change the value of a constant")
