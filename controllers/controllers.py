# -*- coding: utf-8 -*-
from odoo import http

# class AmReferralProgram(http.Controller):
#     @http.route('/am_referral_program/am_referral_program/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/am_referral_program/am_referral_program/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('am_referral_program.listing', {
#             'root': '/am_referral_program/am_referral_program',
#             'objects': http.request.env['am_referral_program.am_referral_program'].search([]),
#         })

#     @http.route('/am_referral_program/am_referral_program/objects/<model("am_referral_program.am_referral_program"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('am_referral_program.object', {
#             'object': obj
#         })