# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'create_date desc'

    # Basic Information
    name = fields.Char(string="Patient Full Name", required=True, tracking=True)
    patient_id = fields.Char(string="Patient ID", required=True, copy=False, readonly=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('hospital.patient'))
    id_no = fields.Char(string="National ID", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", required=True, tracking=True)

    # Contact Information
    phone = fields.Char(string="Phone Number", tracking=True)
    mobile = fields.Char(string="Mobile Number", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    address = fields.Text(string="Address", tracking=True)

    # Medical Information
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-')
    ], string="Blood Group", tracking=True)

    allergies = fields.Text(string="Allergies", tracking=True)
    medical_history = fields.Text(string="Medical History", tracking=True)
    emergency_contact = fields.Char(string="Emergency Contact", tracking=True)
    emergency_phone = fields.Char(string="Emergency Phone", tracking=True)

    # Visit Information
    first_visit_datetime = fields.Datetime(string="First Visit",
                                           default=fields.Datetime.now, tracking=True)
    last_visit_date = fields.Datetime(string="Last Visit", tracking=True)
    total_visits = fields.Integer(string="Total Visits", default=0, tracking=True)

    # Financial Information
    total_amount = fields.Float(string="Total Amount", default=0.0, tracking=True)
    paid_amount = fields.Float(string="Paid Amount", default=0.0, tracking=True)
    due_amount = fields.Float(string="Due Amount", compute="_compute_due_amount", store=True)

    # Status and Stages
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_treatment', 'In Treatment'),
        ('treated', 'Treated'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string="Priority", default='0', tracking=True)

    # Additional Fields
    active = fields.Boolean(string="Active", default=True, tracking=True)
    notes = fields.Text(string="Notes")
    assigned_doctor = fields.Many2one('res.users', string="Assigned Doctor", tracking=True)

    # Computed Fields
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                record.age = relativedelta(date.today(), record.date_of_birth).years
            else:
                record.age = 0

    @api.depends('total_amount', 'paid_amount')
    def _compute_due_amount(self):
        for record in self:
            record.due_amount = record.total_amount - record.paid_amount

    # Validation
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Please enter a valid email address!")

    @api.constrains('date_of_birth')
    def _check_birth_date(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > date.today():
                raise ValidationError("Birth date cannot be in the future!")

    # Button Actions
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True

    def action_start_treatment(self):
        self.write({
            'state': 'in_treatment',
            'last_visit_date': fields.Datetime.now(),
            'total_visits': self.total_visits + 1
        })
        return True

    def action_complete_treatment(self):
        self.write({'state': 'treated'})
        return True

    def action_discharge(self):
        self.write({'state': 'discharged'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_schedule_appointment(self):
        # This would open appointment scheduling wizard
        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule Appointment',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'context': {'default_patient_id': self.id},
            'target': 'new'
        }

    def action_view_medical_history(self):
        # This would show medical history
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medical History',
            'res_model': 'hospital.medical.history',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
        }

    # Override create to generate sequence
    @api.model
    def create(self, vals):
        if vals.get('patient_id', '/') == '/':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.patient') or '/'
        return super(Patient, self).create(vals)