# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Sale(models.Model):
    _inherit = "sale.order"

    margin_approval_ids = fields.One2many('margin.approval.groups', 'order_id', 'Approval List')
    state = fields.Selection(selection_add=[('to_approve', "To Approve")], ondelete={'to_approve': 'set default'})

    def fetch_approval_rule(self):
        for order in self:
            margin_per = round(order.margin_percent * 100, 2)
            domain=[('min_margin_amount', '<', margin_per), ('margin_amount', '>', margin_per)]
            approval = self.env['margin.approval'].search(domain, limit=1)
            return approval

    def _create_approvals(self, approvals):
        for approval in approvals:
            user_ids = approval.user_ids.ids
            if approval:
                for user in user_ids:
                    self.env['margin.approval.groups'].create({
                        'order_id': self.id,
                        'name': approval.name,
                        'required_user_ids': [(6, 0, [user])],
                        'approval_data_id': approval.id,
                    })
            self.state = 'to_approve'

    def action_confirm(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(_('Please add lines!'))
            is_approvel =  self.env.context.get('is_approvel', False)
            if not is_approvel:
                order.margin_approval_ids.filtered(lambda x: x.status == 'none').unlink()
                approval = order.fetch_approval_rule()
                if approval:
                    for approve in approval:
                        self._create_approvals(approve)
                else:
                    return super(Sale, self).action_confirm()
            else:
                return super(Sale, self).action_confirm()

    def rejected_order(self):
        line = self.margin_approval_ids.filtered(lambda x: self.env.uid in x.required_user_ids.ids and x.status in ['none', 'approved'])
        if line:
            if line.status == 'rejected':
                raise ValidationError(_('You are not allowed to approve or already Rejected!'))
            line.write({'status': 'rejected', 'user_id': self.env.uid, 'approval_date': fields.Datetime.now()})
        else:
            raise ValidationError(_('You are not allowed to approve or already rejected!'))
        return True

    def approve_order(self):
        line = self.margin_approval_ids.filtered(lambda x: self.env.uid in x.required_user_ids.ids and x.status in ['none', 'rejected'])
        if line:
            if line.status == 'approved':
                raise ValidationError(_('You are not allowed to approve or already Approved!'))
            line.write({'status': 'approved', 'user_id': self.env.uid, 'approval_date': fields.Datetime.now()})
        else:
            raise ValidationError(_('You are not allowed to approve or already Approved!'))
        if all(line.status != 'none' for line in self.margin_approval_ids):
            return self.sudo().with_context(is_approvel=True).action_confirm()
        return True

class MargingApprovelList(models.Model):
    _name = "margin.approval.groups"
    _description = 'Margin Approval Groups'

    name = fields.Char('Type')
    order_id = fields.Many2one('sale.order', 'Sale Order',)
    user_id = fields.Many2one('res.users', 'Approved by')
    required_user_ids = fields.Many2many('res.users', string='Requested Users')
    status = fields.Selection([
        ('none', 'Not Yet'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')], string='Status',
        default='none')
    approval_date = fields.Datetime('Approval Date')
    approval_data_id = fields.Many2one('margin.approval', 'Technical field')
