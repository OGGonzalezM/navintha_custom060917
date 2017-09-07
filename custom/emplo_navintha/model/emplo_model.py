# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from openerp import api, fields, models

class emplo_navintha(models.Model):

    _inherit = 'hr.employee'

    x_numempleado = fields.Char(string="Número de Empleado",
         help="Número de control del empleado")

    x_contratacion = fields.Date(string="Fecha de Contratación")

    x_antiguedad = fields.Char(string="Antigüedad",
        readonly=True, 
        compute='_total_minutes')

    x_observaciones = fields.Text(string="Observaciones", 
         help="Observaciones en el empleado")

    x_fechaactual = fields.Date(default=fields.Date.today())

    x_perfilacademico = fields.Many2one('hr.escolaridad', 
         string="Perfil Académico",
         help="")

    #Campos para los documentos
    x_navintha_documentos_actanacimiento = fields.Boolean(string="Acta de nacimiento", 
         help="Si el empleado presentó este documento marque la casilla")

    #x_navintha_documentos
    x_navintha_documentos_ine = fields.Boolean(string="INE",
         help="Si el empleado presentó este documento marque la casilla")

    x_navintha_documentos_comprobantedomicilio = fields.Boolean(string="Comprobante de domicilio",
        help="Si el empleado presentó este documento marque la casilla")

    x_navintha_documentos_curp = fields.Boolean(string="CURP",
        help="Si el empleado presentó este documento marque la casilla")

    x_navintha_documentos_cv = fields.Boolean(string="Curriculum Vitae",
        help="Si el empleado presentó este documento marque la casilla")

    x_navintha_documentos_comprobanteestudios = fields.Boolean(string="Comprobante de estudios",
        help="Si el empleado presentó este documento marque la casilla")

    @api.one
    @api.depends('x_contratacion','x_fechaactual')
    def _total_minutes(self):
        if self.x_contratacion and self.x_fechaactual:
            start_dt = fields.Datetime.from_string(self.x_contratacion)
            finish_dt = fields.Datetime.from_string(self.x_fechaactual)
            difference = relativedelta(finish_dt, start_dt)
            year = difference.years
            month = difference.months
            days = difference.days
            self.x_antiguedad = str(year)+" anios "+str(month)+" meses "+str(days)+" dias"
        return {}
