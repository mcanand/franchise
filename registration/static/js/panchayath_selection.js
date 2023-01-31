odoo.define('panchayat_selection.change_panchayath_filter', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
publicWidget.registry.change_panchayath_filter = publicWidget.Widget.extend ({
    selector: '.s_website_form_input',
    events:{
        'change select[name="district"]': '_onChangeDistrict',
        'change select[name="local_body"]': '_onChangeDistrict',
    },
    start:function(){
        var district = $('select[name="district"] :selected').val()
        var local_body = $('select[name="local_body"] :selected').val()
        ajax.jsonRpc('/get/panchayats', 'call', {'district': district, 'local_body': local_body})
                .then(function (result) {
                    _.each(result, function(result) {
                        $('select[name="panchayat"]').append("<option value="+result.id+">"+result.name+"</option>")
                    });
                                 console.log("resulttt", result)

                });
    },
    _onChangeDistrict:function(){
         var district = $('select[name="district"] :selected').val()
         var local_body = $('select[name="local_body"] :selected').val()
              ajax.jsonRpc('/get/panchayats', 'call', {'district': district, 'local_body': local_body})
                .then(function (result) {
                console.log('llllllllllllll',$('select[name="panchayat"]'))
                    $('select[name="panchayat"]').children().remove()
                    _.each(result, function(result) {
                        $('select[name="panchayat"]').append("<option value="+result.id+">"+result.name+"</option>")
                    });
                });
    },
    });
});