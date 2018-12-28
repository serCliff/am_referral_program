# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pdb


class StockPicking(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, values):
        # Descuenta las unidades de este producto del picking si es un regalo
        if 'sale_line_id' in values and self.env['sale.order.line'].browse(values['sale_line_id']).made_gift:
            values['product_uom_qty'] = 0
        return super().create(values)

