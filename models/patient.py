from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = "id desc"

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], default='draft', string='Status', tracking=True)
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    image = fields.Binary(string="Patient Image")
    appointment_count = fields.Integer(string="Appointment Count")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    # def _compute_appointment_count(self):
    #     print("button di klik")
        # for rec in self:
        #     appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
        #     rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'





    def action_open_appointments(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree, form',
            'target': 'current',
        }



