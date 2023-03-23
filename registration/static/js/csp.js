odoo.define('registration.csp', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var table_head = ""
publicWidget.registry.csp = publicWidget.Widget.extend ({
    selector: '.csps',
    events:{
        'change select[name="district"]': '_onChangeDistrict',
    },
    start:function(){
          var d_id = $('.district').val()
          ajax.jsonRpc('/get/cpcs', 'call', {'id':d_id}).then(function(result){
                if(result){
                    $('.append_tr').remove()
                    var no = 0
                    _.each(result, function(result){
                        no = no + 1
                        $('table').append("<tr class='append_tr'><td>"+no+"</td><td>"+result.name+"</td><td>center id</td><td>center</td><td>"+result.location+"</td></tr>")
                    })
                }
                else{
                    $('.append_tr').remove()
                }
          });
    },
    _onChangeDistrict:function(){
        var d_id = $('.district').val()
          ajax.jsonRpc('/get/cpcs', 'call', {'id':d_id}).then(function(result){
                if(result){
                    $('.append_tr').remove()
                    var no = 0
                    _.each(result, function(result){
                        no = no + 1
                        $('table').append("<tr class='append_tr'><td>"+no+"</td><td>"+result.name+"</td><td>center id</td><td>center</td><td>"+result.location+"</td></tr>")
                    })
                }
                else{
                    $('.append_tr').remove()
                }
          });
    },
    });
});
