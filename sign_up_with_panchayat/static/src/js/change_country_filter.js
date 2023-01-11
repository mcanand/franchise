odoo.define('sign_up_with_panchayat.change_country_filter', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');

publicWidget.registry.change_country_filter = publicWidget.Widget.extend    ({
    selector: '.oe_signup_form',
    events:{
        'change select[name="district_id"]': '_onChangeDistrict'
    },
    start:function(){

        var district = $('select[name="district_id"] :selected').val()
        ajax.jsonRpc('/get/panchayats', 'call', {'district': district})
                .then(function (result) {

                    _.each(result, function(result) {
                        $('select[name="panchayat_id"]').append("<option value="+result.id+">"+result.name+"</option>")
                    });
                });
    },
    _onChangeDistrict:function(){
         var district = $('select[name="district_id"] :selected').val()
              ajax.jsonRpc('/get/panchayats', 'call', {'district': district})
                .then(function (result) {
                console.log($('select[name="panchayat_id"]'))
                    $('select[name="panchayat_id"]').children().remove()
//                    $('select[name="panchayat_id"] options').remove()
                    _.each(result, function(result) {
                        $('select[name="panchayat_id"]').append("<option value="+result.id+">"+result.name+"</option>")
                    });
                });
    },
    });
    });