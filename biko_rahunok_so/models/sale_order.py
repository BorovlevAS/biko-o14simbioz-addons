from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def biko_get_invoice_filename(self):
        doc_num = self.name.split('/')[-1]
        doc_date = self.date_order.strftime("%d.%m.%Y")
        return f'Рахунок № {doc_num} від {doc_date}'