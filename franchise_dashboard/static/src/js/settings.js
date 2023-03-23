odoo.define('franchise_dashboard.settings', function(require) {
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

    var FranchiseSettings = AbstractAction.extend({
        template: "franchise_settings",
        events: {

        },

    });
     return FranchiseSettings;
});