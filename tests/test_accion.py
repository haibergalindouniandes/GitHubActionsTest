# Import de librerias
import unittest
import random
from faker import Faker
from faker.providers import DynamicProvider
from faker_vehicle import VehicleProvider
from src.logica.Logica_mock import Logica_mock


class AccionTestCase(unittest.TestCase):

    def setUp(self):
        """Método que permite preparar el ambiente necesario para realizar las pruebas"""
        # Se genera instancia de Logica_Mock
        self.logica = Logica_mock()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()
        # Lista de tipos de mantenimientos
        tipos_mantenimientos_proveedor = DynamicProvider(provider_name="tipos_mantenimientos",
                                                         elements=["PAGO IMPUESTOS AUTOMOVIL", "LAVAR AUTOMOVIL", "TANQUEAR GASOLINA",
                                                                   "POLICHAR AUTOMOVIL", "REVISION TECNICO MECANICA", "COMPRAR SOA",
                                                                   "PINTAR AUTOMOVIL", "ECHAR AIRE A LAS LLANTAS", "CAMBIAR ACEITE"])
        # Agregar provedor de tipos de mantenimiento
        self.data_factory.add_provider(tipos_mantenimientos_proveedor)
        # Lista de tipos de combustible
        tipos_combustibles_proveedor = DynamicProvider(provider_name="tipos_combustibles",
                                                       elements=["Gasolina Diesel", "Gasolina Corriente", "Electrico", "ACPM"])
        # Agregamos proveedor de tipos de combustible
        self.data_factory.add_provider(tipos_combustibles_proveedor)
        # Agregar provedor de vehiculos
        self.data_factory.add_provider(VehicleProvider)

    def test_agregar_accion_parametros_vacios(self):
        """Prueba para validar que no se envien parametros vacios"""
        seCreaAccion = self.logica.crear_accion(2, 1, "", float(random.uniform(
            10000, 300000)), self.data_factory.date_between(start_date='-12y'))
        self.assertFalse(seCreaAccion, 'Se valida que los parametros de entrada no esten vacios')

    def test_agregar_accion(self):
        """Prueba para agregar una accion"""
        self.logica.eliminar_mantenimientos()
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence())
        self.logica.eliminar_autos()
        self.logica.crear_auto(self.data_factory.vehicle_make_model(), self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
                               self.data_factory.vehicle_year(), self.data_factory.random_number(
                                   digits=4), self.data_factory.color_name(),
                               self.data_factory.random_number(digits=4), self.data_factory.tipos_combustibles())
        seCreaAccion = self.logica.crear_accion(1, 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        self.assertTrue(seCreaAccion, 'Se agrega Accion')

    def test_agregar_accion_mantenimiento_automovil_invalido(self):
        """Prueba para validar que no se agregue una accion con un mantenimiento no existente"""
        seCreaAccion = self.logica.crear_accion(random.randint(100, 10000), 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        self.assertFalse(seCreaAccion, 'Validacion agregar Accion mantenimiento no existe')

    def test_listar_acciones(self):
        """Prueba para listar las acciones asociadas a un automovil"""
        for item in range(1, 10):
            self.logica.crear_accion(1, 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                     self.data_factory.date_between(start_date='-4y'))
        acciones = self.logica.dar_acciones_auto(1)
        self.assertGreater(len(acciones), len([]), 'Consulta lista de acciones asociadas a un Automovil')                                   
        
    def test_reporte_ganancias_automovil(self):
        """Prueba para validar que no existan mantenimientos asociados a un automovil"""
        #self.logica.eliminar_autos()
        self.logica.crear_auto(
            "",
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.logica.crear_auto(
            "",
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        #self.logica.eliminar_mantenimientos()
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence())
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence())
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence())
        #self.logica.eliminar_acciones()
        self.logica.crear_accion(random.randint(100, 10000), 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        self.logica.crear_accion(random.randint(100, 10000), 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        self.logica.crear_accion(random.randint(100, 10000), 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        self.logica.crear_accion(random.randint(100, 10000), 1, float(random.uniform(10000, 300000)), float(random.uniform(10000, 300000)),
                                                self.data_factory.date_between(start_date='-4y'))
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(1)

        self.assertGreater(len(lista_gastos), len([]), 'Consulta lista de gastos asociadas a un Automovil')
        self.assertGreater(float(valor_kilometro) ,0.0,'valor km 0')        