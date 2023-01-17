odoo.define('franchise_dashboard.dashboard', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');

    var session = require('web.session');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
    var AbstractAction = require('web.AbstractAction');
    var rpc = require('web.rpc');
    console.log('hai');
    var utils = require('web.utils');



    var FranchiseDashboard = AbstractAction.extend({
        template: "franchise_dashboard",
        events: {

        },
        init: function(parent, context) {
            console.log('happy')
            this._super(parent, context);
            this.login_employee = true;
            this._super(parent, context);
        },

        start: function() {
            var self = this;
            qweb.render('franchise_dashboard', {widget: self});
        },
            /*this._rpc({
                model: 'franchise.dashboard',
                method: 'get_value',
                args: [],
            }).then(function(result) {
                console.log('result', result);
                QWeb.render('franchise_dashboard', {
                    widget: self
                });*/
                // if(self.login_employee.dashboard_access == 'admin'){
//                console.log("admin");
//                $('.o_hr_dashboard').prepend(QWeb.render('LoginEmployeeDetails', {
//                    widget: self
//                }));
//                self.draw_bar_chart_manager();
//                self.draw_bar_chart_manager_product();
            /*return this._super().then(function() {
                self.$el.parent().addClass('oe_background_grey');
            });*/
    });

    core.action_registry.add('franchise_dashboard_tag', FranchiseDashboard);
    return FranchiseDashboard;
});