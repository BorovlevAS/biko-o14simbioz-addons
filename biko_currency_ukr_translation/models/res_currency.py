from odoo import fields, models

class Currency(models.Model):
    _inherit = "res.currency"

    biko_str_one = fields.Char(string='One', translate=True)
    biko_str_two = fields.Char(string='Two', translate=True)
    biko_str_five = fields.Char(string='Five', translate=True)

    biko_cent_str_one = fields.Char(string='One', translate=True)
    biko_cent_str_two = fields.Char(string='Two', translate=True)
    biko_cent_str_five = fields.Char(string='Five', translate=True)

    def biko_get_names(self, cents):

        if not cents:
            str_one = self.biko_str_one if self.biko_str_one else self.currency_unit_label
            str_two = self.biko_str_two if self.biko_str_two else self.currency_unit_label
            str_five = self.biko_str_five if self.biko_str_five else self.currency_unit_label
        else:
            str_one = self.biko_cent_str_one if self.biko_cent_str_one else self.currency_subunit_label
            str_two = self.biko_cent_str_two if self.biko_cent_str_two else self.currency_subunit_label
            str_five = self.biko_cent_str_five if self.biko_cent_str_five else self.currency_subunit_label

        return {str_one, str_two, str_five}

    def biko_get_currency_name(self, sum, cents):
        
        str_one, str_two, str_five = self.biko_get_names(cents)

        last_num = int(repr(sum)[-1])

        if last_num == 1:
            return str_one
        elif last_num > 1 and last_num < 5:
            return str_two
        else:
            return str_five