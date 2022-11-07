odoo.define('BikoDashboardPatch.AccountingDashboard', function(require) {
    "use strict";
    
    debugger;
    const ActionMenu = require('AccountingDashboard.AccountingDashboard');
    
    ActionMenu.include({
        events: _.extend({}, accounting_dashboard.prototype.events, {
            'change #income_expense_values': 'onchange_income_expense',
        }),

        onchange_income_expense: function (ev) {

            switch(ev.target.value) {
                case 'income_this_month':
                    this.onclick_income_this_month(ev);
                    break;
                case 'income_this_year':
                    this.onclick_income_this_year(ev);
                    break;
                case 'income_last_month':
                    this.onclick_income_last_month(ev);
                    break;
                case 'income_last_year':
                    this.onclick_income_last_year(ev);
                    break;
            }
        },

    });

});