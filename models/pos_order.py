# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pdb


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    made_gift = fields.Boolean(default=False)
    added_gifts = fields.Boolean(default=False)

    @api.model
    def create(self, values):
        vals = super().create(values)
        if not vals.made_gift:
            # vals.order_id.add_gifts()
            vals.order_id.action_create_free_product_historic()

        return vals


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def action_create_free_product_historic(self):
        """
        Gestión de los regalos en el momento de crear el ticket del PdV
        """
        self.ensure_one()
        fph = self.env['free.products.historic']

        # Recorremos las lineas y vamos actualizando los historicos asociado a cada cliente
        # con sus regalos y descuentos
        if self.partner_id:
            for pos_line in self.lines:
                if pos_line.discount == 100:
                    historic_line = {
                        'pos_order_id': self.id,
                        'pos_order_line_id': pos_line.id,
                        'partner_related_id': self.partner_id.id,
                        'product_id': pos_line.product_id.product_tmpl_id.id,
                        'uds': pos_line.qty,
                        'register_type': 'auto',
                    }
                    if not pos_line.made_gift:
                        historic_line['uds'] *= -1

                    old_fph = fph.search([('pos_order_line_id', '=', pos_line.id)])
                    if len(old_fph.ids):
                        old_fph.write(historic_line)
                    else:
                        fph.create(historic_line)

        return True

    @api.multi
    def add_gifts(self):
        """
        Añade productos de regalo a los pedidos si se venden desde el punto de venta

        **DESACTIVADO** para activarlo descomentar del create del metodo PosOrderLine
        :return:
        """

        sol = self.env['pos.order.line']
        self_id = self.id
        pdb.set_trace()
        # Recorremos los productos para averiguar los regalos
        for line in self.lines:

            # Se comprueba que no se hayan introducido los regalos antes
            # También se comprueba que las unidades del producto sean positivas
            if not line.added_gifts and line.qty > 0:

                # Chequeamos la regla de adición que tiene el producto
                gift_rule = line.product_id.product_tmpl_id.gift_rule
                qty_gifts = line.qty
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
                                    'qty': new_gift.uds * qty_gifts,
                                    'discount': new_gift.discount,
                                    'made_gift': True,
                                    'added_gifts': True})

                # Marcamos los regalos de esta linea como añadidos
                line.added_gifts = True
                self.env.cr.commit()
