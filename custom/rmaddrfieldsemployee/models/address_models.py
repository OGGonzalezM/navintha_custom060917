# -*- coding: utf-8 -*-
from openerp import fields, models

class Address_models(models.Model):
    _inherit = "hr.employee"

    address_id = fields.Char(string="Dirección de trabajo")

    address_home_id = fields.Char(string="Dirección particular")