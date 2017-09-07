#Fijarse bien en las importaciones.
from datetime import timedelta

from openerp import api, exceptions, fields, models, _


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today())
    datetime_eg = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help='Duration in days')
    seats = fields.Integer(string='Numero de asientos')

    instructor_id = fields.Many2one('res.partner', string='Instructor',
        domain=['|', ('instructor', '=', True),
        ('category_id.name', 'ilike', 'Teacher')])

    course_id = fields.Many2one('openacademy.course', ondelete='cascade',
        string='Course', required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    # Las comillas dobles suelen usarse para los strings, aunque no es restrictivo
    taken_seats = fields.Float(string="Taken Seats", compute='_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in hours", compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)
    color = fields.Integer()
    
    #Workflow
    state = fields.Selection([
         ('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ], default='draft', readonly=True)
    
    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        #if not hace referencia a nada, es decir, null, cero, etc.
        if not self.seats:
            self.seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        print "Verifying valid seats"
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of avaliable seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return{
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }
    
    #Verificar que el numero de asientos se menor o igual al numero de asistentes
    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError(_("A session's instructor can't be an attendee"))

    #Funciones para el calculo de la fecha de inicio y la fecha de finalizacion
    @api.one
    @api.depends('duration', 'start_date')
    def _get_end_date(self):
        print "****** _get_end_date_*******"
        if not(self.start_date and self.duration):
            self.end_date = self.start_date
            return
        start = fields.Datetime.from_string(self.start_date)
        duration = timedelta(days=self.duration, seconds=-1)
        self.end_date = start + duration

    @api.one
    def _set_end_date(self):
        if not (self.start_date and self.end_date):
            return
        print "*******_set_end_date******"
        start_date = fields.Datetime.from_string(self.start_date)
        end_date = fields.Datetime.from_string(self.end_date)
        self.duration = (end_date - start_date).days + 1

    #Definicion de las funciones para el campo 'hours'
    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    #Obtener cuenta de los asistentes
    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)
 
    #Functions to change state in the openacademy_session table
    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'
