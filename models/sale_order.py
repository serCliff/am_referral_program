# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pdb


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    made_gift = fields.Boolean(default=False)
    added_gifts = fields.Boolean(default=False)

    @api.model
    def create(self, values):
        vals = super().create(values)
        if not vals.made_gift:
            vals.order_id.add_gifts()

        return vals


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_create_invoice_auto(self):
        """
        Herencia para meter la gestión de los regalos en el momento de crear la factura
        """
        self.ensure_one()
        fph = self.env['free.products.historic']

        # Recorremos las lineas y vamos actualizando los historicos asociado a cada cliente
        # con sus regalos y descuentos
        for so_line in self.order_line:
            if so_line.discount == 100:
                historic_line = {
                    'sale_order_id': self.id,
                    'sale_order_line_id': so_line.id,
                    'partner_related_id': self.partner_id.id,
                    'product_id': so_line.product_id.product_tmpl_id.id,
                    'uds': so_line.product_uom_qty,
                    'register_type': 'auto',
                }
                if not so_line.made_gift:
                    historic_line['uds'] *= -1
                old_fph = fph.search([('sale_order_line_id', '=', so_line.id)])
                if len(old_fph.ids):
                    old_fph.write(historic_line)
                else:
                    fph.create(historic_line)

        return super().action_create_invoice_auto()

    @api.multi
    def add_gifts(self):

        sol = self.env['sale.order.line']
        self_id = self.id

        # Recorremos los productos para averiguar los regalos
        for line in self.order_line:

            # Se comprueba que no se hayan introducido los regalos antes
            # También se comprueba que las unidades del producto sean positivas
            if not line.added_gifts and line.product_uom_qty > 0:

                # Chequeamos la regla de adición que tiene el producto
                gift_rule = line.product_id.product_tmpl_id.gift_rule
                qty_gifts = line.product_uom_qty
                if gift_rule == "so":
                    qty_gifts = 1

                # Añadimos los regalos de los productos del pedido
                for new_gift in line.product_id.product_tmpl_id.gift_ids:
                    pp_id = self.env['product.product'].search([('product_tmpl_id', '=', new_gift.product_id.id)], limit=1)
                    if pp_id:
                        sol.create({'name': "REGALO: "+str(pp_id.name),
                                    'order_id': self_id,
                                    'product_id': pp_id.id,
                                    'price_unit': pp_id.lst_price,
                                    'product_uom_qty': new_gift.uds * qty_gifts,
                                    'discount': new_gift.discount,
                                    'made_gift': True,
                                    'added_gifts': True})

                # Marcamos los regalos de esta linea como añadidos
                line.added_gifts = True
                self.env.cr.commit()
