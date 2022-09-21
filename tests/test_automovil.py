# Import de librerias
import unittest
from src.modelo.automovil import Automovil
from src.logica.Logica_mock import Logica_mock
import random
from faker import Faker
from faker.providers import DynamicProvider
from faker_vehicle import VehicleProvider


class AutomovilTestCase(unittest.TestCase):
    
    def setUp(self):
        """Método que permite preparar el ambiente necesario para realizar las pruebas"""
        self.logica = Logica_mock()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()
        # Lista de tipos de mantenimiento
        tipos_mantenimientos_proveedor = DynamicProvider(
            provider_name="tipos_mantenimientos",
            elements=[
                "PAGO IMPUESTOS AUTOMOVIL",
                "LAVAR AUTOMOVIL",
                "TANQUEAR GASOLINA",
                "POLICHAR AUTOMOVIL",
                "REVISION TECNICO MECANICA",
                "COMPRAR SOA",
                "PINTAR AUTOMOVIL",
                "ECHAR AIRE A LAS LLANTAS",
                "CAMBIAR ACEITE",
            ],
        )
        # Agregamos proveedor de tipos de mantenimiento
        self.data_factory.add_provider(tipos_mantenimientos_proveedor)
        # Lista de tipos de combustible
        tipos_combustibles_proveedor = DynamicProvider(
            provider_name="tipos_combustibles",
            elements=["Gasolina Diesel", "Gasolina Corriente", "Electrico", "ACPM"],
        )
        # Agregamos proveedor de tipos de combustible
        self.data_factory.add_provider(tipos_combustibles_proveedor)
        # Agregar provedor de vehiculos
        self.data_factory.add_provider(VehicleProvider)


    def test_agregar_automovil_sin_valor(self):
        """Prueba para agregar un automovil sin el  valor en el campo de marca"""

        seCreoAutomovil = self.logica.crear_auto(
            "",
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.assertFalse(seCreoAutomovil, "campos vacios")

    def test_agregar_automovil(self):
        """Prueba para agregar un automovil sin el  valor en el campo de marca"""
        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.assertTrue(seCreoAutomovil, "Se agrega Automovil")

    def test_agregar_automovil_placa_unica(self):
        """Prueba para agregar un automovil que no este registrado (la placa es el identificador y debe ser unica)"""
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "UCQ86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "UCQ86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        self.assertFalse(seCreoAutomovil, "Automovil duplicado")

    def test_automovil_consultar_automoviles(self):
        """Prueba para  consultar Automoviles Registrados"""
        # self.logica.eliminar_autos()
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "AAA86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        automovil = Automovil(
            "Ferrari",
            "AAA86C",
            "2013",
            35000.0,
            "Plateado",
            "5000",
            "Gasolina",
            False,
            5000,
            1000,
        )
        automoviles = self.logica.dar_autos()
        self.assertEqual(automovil.placa, automoviles[0]['placa'], "Lista con resultados")

    def test_vender_automovil_parametros_vacios(self):
        """Prueba para validar que no se envien parametros vacios al momento de vender un Automovil"""
        seVendioAutomovil = self.logica.vender_auto(
            "",
            self.data_factory.random_number(digits=5),
            self.data_factory.random_number(digits=6),
        )
        self.assertFalse(
            seVendioAutomovil, "Se valida que los parametros de entrada no esten vacios"
        )

    def test_vender_automovil(self):
        """Prueba para vender un Automovil"""
        # self.logica.eliminar_autos()
        placaAutoNuevo = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            placaAutoNuevo,
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        seVendioAutomovil = self.logica.vender_auto(
            placaAutoNuevo,
            self.data_factory.random_number(digits=5),
            self.data_factory.random_number(digits=6),
        )
        self.assertTrue(seVendioAutomovil, "Se raliza venta del Automovil")

    def test_vender_automovil_tiene_acciones(self):
        """Prueba para validar que no se venda un Automovil que tenga acciones registradas"""
        # self.logica.eliminar_autos()
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        # self.logica.eliminar_mantenimientos()
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence()
        )
        self.logica.aniadir_mantenimiento(
            self.data_factory.tipos_mantenimientos(), self.data_factory.sentence()
        )
        # self.logica.eliminar_acciones()
        self.logica.crear_accion(
            1,
            1,
            float(random.uniform(10000, 300000)),
            float(random.uniform(10000, 300000)),
            self.data_factory.date_between(start_date="-4y"),
        )
        self.logica.crear_accion(
            2,
            1,
            float(random.uniform(10000, 300000)),
            float(random.uniform(10000, 300000)),
            self.data_factory.date_between(start_date="-4y"),
        )
        seVendioAutomovil = self.logica.vender_auto(
            1,
            self.data_factory.random_number(digits=5),
            self.data_factory.random_number(digits=6),
        )
        self.assertFalse(
            seVendioAutomovil,
            "Se valida que no se realice la venta de un Automovil que tiene acciones registradas",
        )