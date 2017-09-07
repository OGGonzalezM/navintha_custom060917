# -*- coding: utf-8 -*-
from openerp import fields, models

class Navintha_datosempresa(models.Model):
    _name = 'company.profile'

    name = fields.Char(required=True, string="Nombre de la compañia")

    x_navintha_mision = fields.Text(string="Misión",
    	 help="La misión de la empresa seleccionada")

    x_navintha_vision = fields.Text(string="Visión",
    	 help="Visión de la empresa seleccionada")
    
    x_navintha_valores = fields.Text(string="Valores",
         help="Valores base en la empresa.")
    
    x_navintha_politicadecalidad = fields.Text(string="Política de Calidad")
    
    x_navintha_objetivosdecalidad = fields.Text(string="Objetivos de Calidad")
