from dataclasses import field
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    biko_phone_e164 = fields.Char()
    biko_mobile_e164 = fields.Char()

    @api.onchange('phone', 'country_id', 'company_id')
    def _onchange_phone_validation_e164(self):
        if self.phone:
            biko_phone_e164 = self.phone_format(self.phone, raise_exception=True, force_format='E164')
            self.biko_phone_e164 = biko_phone_e164 if biko_phone_e164[0] != '+' else biko_phone_e164[1:]
        else:
            self.biko_phone_e164 = ''

    @api.onchange('mobile', 'country_id', 'company_id')
    def _onchange_mobile_validation_e164(self):
        if self.mobile:
            biko_mobile_e164 = self.phone_format(self.mobile, raise_exception=True, force_format='E164')
            self.biko_mobile_e164 = biko_mobile_e164 if biko_mobile_e164[0] != '+' else biko_mobile_e164[1:]
        else:
            self.biko_mobile_e164 = ''

    def _fill_e164_phone(self):
        for partner in self.with_context(active_test=False).search(
            [("phone", "!=", False)]
        ):
            biko_phone_e164 = partner.phone_format(partner.phone, raise_exception=False, force_format='E164')
            biko_phone_e164 = biko_phone_e164 if biko_phone_e164[0] != '+' else biko_phone_e164[1:]
            partner.update({'biko_phone_e164': biko_phone_e164})

        for partner in self.with_context(active_test=False).search(
            [("mobile", "!=", False)]
        ):
            biko_mobile_e164 = partner.phone_format(partner.mobile, raise_exception=False, force_format='E164')
            biko_mobile_e164 = biko_mobile_e164 if biko_mobile_e164[0] != '+' else biko_mobile_e164[1:]
            partner.update({'biko_mobile_e164': biko_mobile_e164})
