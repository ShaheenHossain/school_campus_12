# -*- coding: utf-8 -*-
from odoo import http

# class Gravience(http.Controller):
#     @http.route('/gravience/gravience/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gravience/gravience/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gravience.listing', {
#             'root': '/gravience/gravience',
#             'objects': http.request.env['gravience.gravience'].search([]),
#         })

#     @http.route('/gravience/gravience/objects/<model("gravience.gravience"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gravience.object', {
#             'object': obj
#         })