odoo.define('franchise_application.dashboard', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');

    var session = require('web.session');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;
    var AbstractAction = require('web.AbstractAction');
    var rpc = require('web.rpc');
    var utils = require('web.utils');

    var AdminDashboard = AbstractAction.extend({
    jsLibs: [
        '/web/static/lib/Chart/Chart.js',
    ],
        template: "admin_dashboard",
        events: {
            'click #fb': 'on_click_fb',
            'click .f_details':'f_details',
        },
        init: function(parent, context) {
            this._super(parent, context);
            this.login_employee = true;
            this._super(parent, context);
        },
        start:function(){
            var self = this;
            qweb.render('admin_dashboard', { widget: self});
            this._rpc({
                    route: '/admin/dashboard/values',
                    params: {}
            }).then(function(result){
                self.dash_details = result
                $('.admin_dash').prepend(qweb.render('dash_views', {
                    widget: self
                }))
            });
        },
        on_click_fb:function(events){
            var self = this
            var val = $(events.target).attr('data-val')
            self.fb_select = val
            this._rpc({
                    route: '/admin/dah/table',
                    params: {val:val}
            }).then(function(result){
                self.record = result
                console.log(result)
                $('.record_tables').html('')
                $('.record_tables').prepend(qweb.render('admin_dash_table', {
                    widget: self
                }))
            });
        },
        f_details:function(events){
            var id =$(events.target).attr('data-id')
            events.preventDefault();
            return this.do_action({
                    type:'ir.actions.act_window',
                    res_id: parseInt($(events.target).attr('data-id')),
                    res_model: 'franchise.application.partner',
                    views: [[false, 'form']],
                    target: 'current',
                });
        },
    });
    core.action_registry.add('admin_dashboard_tag', AdminDashboard);
    return AdminDashboard;
});


