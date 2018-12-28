# -*- coding: utf-8 -*-

from odoo import models, fields, api

GIFT_RULES = [
    ('ud', 'Unidad vendida'),
    ('so', 'Linea de Pedido'),
    ]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    gift_ids = fields.One2many("free.products", "product_related_id", "Gratuitos asociados")
    gift_rule = fields.Selection(GIFT_RULES, string="Regla", default='ud', required="True")

