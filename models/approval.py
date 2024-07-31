# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class MarginApproval(models.Model):
    _name = "margin.approval"
    _description = "margin Approval"

    name = fields.Char(string="Name")
    user_ids = fields.Many2many('res.users', string='Approvers')
    min_margin_amount = fields.Float('Margin Min (%)')
    margin_amount = fields.Float('Margin Max (%)')
