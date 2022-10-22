odoo.define('biko_nextel_patch.CallTabPatch', function (require) {
    "use strict";

    const { patch } = require('web.utils');
    const CallTab = require('nextel.CallTab');

    patch(CallTab, 'biko_nextel_patch.CallTabPatch', {

        _onSearchCallPhone: function (event) {
            this._btnSearch(event, 'partner_phone');
        },
        _enterSearchCallPhone: function (event) {
            this._enterSearch(event, 'partner_phone');
        },

    });
});