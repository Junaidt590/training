from datetime import timedelta

from odoo import models, fields, api


class EstateModel(models.Model):
    _name = "estate.table"
    _description = "Estate Model"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.now() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute="_compute_best_off")
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(string="State",
                             selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')], required=True, copy=False, default='new')

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string='Orientation Type',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')]
                                          )
    property_type_id = fields.Many2one('property.type', string='Property Type')
    res_user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    res_partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_id = fields.Many2many('property.tag', string='Tag')
    price_id = fields.One2many('property.offer','property_id')
    total_area = fields.Integer(compute="_compute_total")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("price_id.price")
    def _compute_best_off(self):
        for record in self:
                record.best_offer = max(record.price_id.mapped('price'),default=0)



class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"

    name = fields.Char(required=True)


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False,
                              selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner',string='Partner',required=True)
    property_id = fields.Many2one('estate.table', required=True)
    validity = fields.Integer(store=True,default=7)
    date_deadline = fields.Date(compute="_compute_deadline",readonly=False)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        now = fields.Datetime.now()
        for record in self:
            record.date_deadline = record.create_date = now + timedelta(days=record.validity)
