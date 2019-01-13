# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pdb



class ReferralGifts(models.Model):
    _name = "free.products"

    product_id = fields.Many2one("product.template", "Productos", required=True)
    uds = fields.Float("Unidades")
    discount = fields.Float("Descuento (%)", default=100)
    partner_related_id = fields.Many2one("res.partner", "Cliente Asociado")
    product_related_id = fields.Many2one("product.template", "Producto Asociado")


class FreeProductsHistoric(models.Model):
    _name = "free.products.historic"

    product_id = fields.Many2one("product.template", "Productos", required=True)
    uds = fields.Float("Unidades", default="1")
    discount = fields.Float("Descuento (%)", default=100)

    date = fields.Date("Día", default=fields.Date.today)
    datetime = fields.Datetime("Fecha", default=fields.Datetime.now)

    partner_related_id = fields.Many2one("res.partner", "Cliente")
    sale_order_id = fields.Many2one("sale.order", "Pedido de venta")
    pos_order_id = fields.Many2one("pos.order", "Ticket")



    @api.multi
    def set_gift(self):
        """
        Busca el partner al que hay que hacerle el regalo
        Le hace el regalo y lo marca como regalado para que no tenga más regalos.
        """
        context = self._context
        partner_to_gift_id = self.env['res.partner'].browse(context.get('make_gift'))

        check_true = partner_to_gift_id.referrals_ids.filtered(lambda r: r.id == context.get('check_true'))
        check_true.gifted = True

        return True



    @api.model
    def create(self, values):
        """
        Estos 3 métodos fuerzan actualizar los datos del cliente
        """
        vals = super(FreeProductsHistoric, self).create(values)
        vals.partner_related_id.set_partner_free_products()
        return vals

    @api.multi
    def write(self, values):
        super(FreeProductsHistoric, self).write(values)
        self.partner_related_id.set_partner_free_products()
        return True

    @api.multi
    def unlink(self):
        partner = self.partner_related_id
        returned_value = super(FreeProductsHistoric, self).unlink()
        partner.set_partner_free_products()
        return returned_value

