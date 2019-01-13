# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pdb


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_referred = fields.Many2one("res.partner", "Referidos", related='self')
    referred_by = fields.Many2one("res.partner", "Referido por:")
    referrals_ids = fields.One2many("res.partner", "referred_by", "Referidos")
    gifted = fields.Boolean("Regalado")
    make_gift = fields.Boolean("Tiene regalos disponibles", default=False)
    product_ids = fields.One2many("free.products", "partner_related_id", string="Productos Gratuitos")
    product_historic_ids = fields.One2many("free.products.historic", "partner_related_id",
                                           string="Historico Productos Gratuitos")

    # TODO: Hacer constrain que referred_by no pueda ser igual que self
    # TODO: Controlar cuando se borra un referred_by quitarle el regalo al referido

    @api.multi
    def set_partner_free_products(self):
        # Actualiza la tabla de regalos gratuitos del cliente
        self.product_ids.unlink()
        self.env.cr.commit()

        for new_gift in self.product_historic_ids:
            self_gift = self.is_gift_on_self_gift(new_gift)

            # Busca si ya hay una entrada para actualizar las unidades y si no la hay la crea
            if self_gift:
                self_gift.uds += new_gift.uds
                if self_gift.uds == 0:
                    self_gift.unlink()
            else:
                self.product_ids.create({'product_id': new_gift.product_id.id,
                                         'uds': new_gift.uds,
                                         'discount': new_gift.discount,
                                         'partner_related_id': self.id})
            self.env.cr.commit()


    @api.multi
    def is_gift_on_self_gift(self, new_gift_id):
        """
        Busca un producto en la lista de regalos del cliente para actualizarlo
        :return: id de la tabla o falso
        """
        fp = self.env['free.products']
        self_id = self.id

        for self_gift in fp.search([('partner_related_id','=', self_id)]):
            # Si existe un producto igual con el mismo descuento devuelve el id para actualizarlo si es necesario
            if new_gift_id.product_id.id == self_gift.product_id.id and new_gift_id.discount == self_gift.discount:
                return self_gift
        return False



    @api.model
    def create(self, values):
        ret = super().create(values)
        if ret.referred_by:
            ret.referred_by.set_make_gift_filter()
        return ret

    @api.multi
    def write(self, values):
        super().write(values)
        if self.referred_by:
            self.referred_by.set_make_gift_filter()
        return True

    @api.multi
    def set_make_gift_filter(self):
        """
        Establece el filtro de regalado a true o false
        :return:
        """
        set_gifted = False
        for partner in self.referrals_ids:
            if not partner.gifted and partner.id != self.id:
                set_gifted = True
        self.make_gift = set_gifted




    @api.multi
    def action_make_gift(self):
        to_check = self.id
        to_gift = self._context.get("params").get("id")
        return {
            'name': _('Regalos'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'free.products.historic',
            'view_id': self.env.ref('am_referral_program.view_wizard_referral_gift').id,
            'type': 'ir.actions.act_window',
            'context': {'default_partner_related_id': to_gift, 'check_true': to_check, 'make_gift': to_gift},
            'target': 'new'
        }

