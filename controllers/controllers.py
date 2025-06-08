# -*- coding: utf-8 -*-
# from odoo import http


# class AioHms(http.Controller):
#     @http.route('/aio_hms/aio_hms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aio_hms/aio_hms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('aio_hms.listing', {
#             'root': '/aio_hms/aio_hms',
#             'objects': http.request.env['aio_hms.aio_hms'].search([]),
#         })

#     @http.route('/aio_hms/aio_hms/objects/<model("aio_hms.aio_hms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aio_hms.object', {
#             'object': obj
#         })

