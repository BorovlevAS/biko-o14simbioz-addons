odoo.define('web.partner.OrgChart', function (require) {
    "use strict";

    const AbstractField = require('web.AbstractField');
    const concurrency = require('web.concurrency');
    const core = require('web.core');
    const field_registry = require('web.field_registry');
    const session = require('web.session');
    const QWeb = core.qweb;

    let FieldOrgChart = AbstractField.extend({
        events: {
            "click .biko_o_partner_redirect": "_onPartnerRedirect",
            "click .biko_o_partner_sub_redirect": "_onPartnerSubRedirect",
            "click .biko_o_partner_more_parents": "_onPartnerMoreParents"
        },
        /**
         * @constructor
         * @override
         */
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.dm = new concurrency.DropMisordered();
            this.partner = null;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
        /**
         * Get the chart data through a rpc call.
         *
         * @private
         * @returns {Promise}
         */
        _getOrgData: function () {
            return this.dm.add(this._rpc({
                route: '/partner/biko_get_org_chart',
                params: {
                    partner_id: this.partner,
                    context: session.user_context,
                },
            })).then(function (data) {
                return data;
            });
        },
        /**
         * Get subordonates of a partner through a rpc call.
         *
         * @private
         * @param {integer} partner_id
         * @returns {Promise}
         */
        _getSubordinatesData: function (partner_id, type) {
            return this.dm.add(this._rpc({
                route: '/partner/biko_get_subordinates',
                params: {
                    partner_id: partner_id,
                    subordinates_type: type,
                    context: session.user_context,
                },
            }));
        },
        /**
         * @override
         * @private
         */
        _render: function () {
            if (!this.recordData.id) {
                return this.$el.html(QWeb.render("biko_partner_org_chart", {
                    parents: [],
                    children: [],
                }));
            } else if (!this.partner) {
                // the widget is either dispayed in the context of a partner form or a res.users form
                this.partner = this.recordData.partner_ids !== undefined ? this.recordData.partner_ids.res_ids[0] : this.recordData.id;
            }

            let self = this;
            return this._getOrgData().then(function (orgData) {
                if (_.isEmpty(orgData)) {
                    orgData = {
                        parents: [],
                        children: [],
                    }
                }
                orgData.view_partner_id = self.recordData.id;
                self.$el.html(QWeb.render("biko_partner_org_chart", orgData));
                self.$('[data-toggle="popover"]').each(function () {
                    $(this).popover({
                        html: true,
                        title: function () {
                            var $title = $(QWeb.render('biko_partner_orgchart_popover_title', {
                                partner: {
                                    name: $(this).data('partner-name'),
                                    id: $(this).data('partner-id'),
                                },
                            }));
                            $title.on('click', '.biko_o_partner_redirect', _.bind(self._onPartnerRedirect, self));
                            return $title;
                        },
                        container: this,
                        placement: 'left',
                        trigger: 'focus',
                        content: function () {
                            var $content = $(QWeb.render('biko_partner_orgchart_popover_content', {
                                partner: {
                                    id: $(this).data('partner-id'),
                                    name: $(this).data('partner-name'),
                                    direct_sub_count: parseInt($(this).data('partner-dir-subs')),
                                    indirect_sub_count: parseInt($(this).data('partner-ind-subs')),
                                },
                            }));
                            $content.on('click', '.biko_o_partner_sub_redirect', _.bind(self._onPartnerSubRedirect, self));
                            return $content;
                        },
                        template: QWeb.render('biko_partner_orgchart_popover', {}),
                    });
                });
            });
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        _onPartnerMoreParents: function (event) {
            event.preventDefault();
            this.partner = parseInt($(event.currentTarget).data('partner-id'));
            this._render();
        },
        /**
         * Redirect to the partner form view.
         *
         * @private
         * @param {MouseEvent} event
         * @returns {Promise} action loaded
         */
        _onPartnerRedirect: function (event) {
            let self = this;
            event.preventDefault();
            let partner_id = parseInt($(event.currentTarget).data('partner-id'));
            return this._rpc({
                model: 'res.partner',
                method: 'get_formview_action',
                args: [partner_id],
            }).then(function (action) {
                return self.do_action(action);
            });
        },
        /**
         * Redirect to the sub partner form view.
         *
         * @private
         * @param {MouseEvent} event
         * @returns {Promise} action loaded
         */
        _onPartnerSubRedirect: function (event) {
            event.preventDefault();
            let partner_id = parseInt($(event.currentTarget).data('partner-id'));
            let type = $(event.currentTarget).data('type') || 'direct';
            let self = this;
            if (partner_id) {
                this._getSubordinatesData(partner_id, type).then(function (data) {
                    let domain = [['id', 'in', data]];
                    return self._rpc({
                        model: 'res.partner',
                        method: 'get_formview_action',
                        args: [partner_id],
                    }).then(function (action) {
                        action = _.extend(action, {
                            'name': 'Contacts',
                            'view_mode': 'kanban,list,form',
                            'views': [[false, 'kanban'], [false, 'list'], [false, 'form']],
                            'domain': domain,
                        });
                        return self.do_action(action);
                    });
                });
            }
        },
    });

    field_registry.add('biko_partner_org_chart', FieldOrgChart);

    return FieldOrgChart;
});
