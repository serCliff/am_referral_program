{
    'name': "Programa de Referidos",

    'summary': """
        Modulo creado para gestionar el sistema de referidos de audiomedical.
        """,

    'description': """

        ## HISTORICO DE PRODUCTOS REGALADOS
        Genera un historico de transacciones con el cliente en las que alguno de los productos vendidos tenga un descuento.
        A mayores cuando un producto tiene asociado un producto de regalo suma al conjunto de productos gratuitos disponibles.
        
        ## PRODUCTOS REGALADOS DISPONIBLES
        Habrá una tabla con los productos que tiene disponibles para llevarse a coste 0.
        
        ## PRODUCTOS GRATUITOS ASOCIADOS A OTROS PRODUCTOS
        Los productos podrán tener asociados otros productos gratuitos. Estos productos
        se incluirán automáticamente a las facturas a coste 0 junto con el escogido. También actualizará la tabla de productos
        gratuitos asociados. El objetivo es que si no los entregamos en el momento, en cualquier otro momento podamos hacerlo.

    """,

    'author': "Sergio Del Castillo Baranda",
    'website': "http://www.sergiodelcastillo.com",

    'category': 'Sales',
    'version': '0.2',


    'depends': ['am_personalizations'],

    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/referral_gifts.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/sale_order.xml',
    ],
}
# -*- coding: utf-8 -*-
