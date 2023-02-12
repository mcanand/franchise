odoo.define('panchayat_selection.change_panchayath_filter', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
publicWidget.registry.change_panchayath_filter = publicWidget.Widget.extend ({
    selector: '.s_website_form_input',
    events:{
        'change select[name="district"]': '_onChangeDistrict',
        'change select[name="local_body"]': '_onChangeDistrict',
        'click .btn-form-submit': '_checkpartner',
        'click .close': '_onClickClosePopup',
        'keyup .referd-by': '_onKeyUpSearch',
        'keydown .referd-by': '_onKeydownSearch',
    },
    start:function(){
        var district = $('select[name="district"] :selected').val()
        var local_body = $('select[name="local_body"] :selected').val()
        ajax.jsonRpc('/get/panchayats', 'call', {'district': district, 'local_body': local_body})
                .then(function (result) {
                    _.each(result, function(result) {
                        $('select[name="panchayat"]').append("<option value="+result.id+">"+result.name+"</option>")
                    });
                });
    },
    show_popup: function(){
         $("#myModal").show()
    },
    _onClickClosePopup:function(){
         $("#myModal").hide()
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

    _checkpartner:function(){
        var self = this;
        var email = $('input[name="email"]').val()
        var phone = $('input[name="phone"]').val()
        var referal = $('input[name="referd_by"]').val()
        var msg = $('#msg-cls')
        var checkatsymbol = email.includes("@");
        var checkdotsymbol = email.includes(".");
        if ($('input[name="name"]').val() == "" || $('input[name="dob"]').val() =="" || phone=="" ||
            $('input[name="location"]').val() == "" || email==""){
                    msg.html("Required Details Not Filled")
                    self.show_popup()
            }
        else if (checkatsymbol==false || checkdotsymbol==false){
            msg.html("please enter valid email")
            this.show_popup()
        }
        else{
            ajax.jsonRpc('/check/user', 'call', {'email': email, 'phone': phone})
              .then(function (result) {
                  if(result != false){
                      msg.html("Email/Phone is Alredy Exist")
                      self.show_popup()
                  }
                  else{
                        $("#form_input_id").submit();
                  }
              });
        }
    },
    _onKeyUpSearch:function(event){
        var msg = $('#msg-cls')
        var self = this;
        $(".referd-by").css("color", "red");
        var referal_code = $(".referd-by").val()
        if(referal_code){
            if(referal_code.length == 8){
                console.log("enterdddddddd")
                ajax.jsonRpc('/check/referal', 'call', {'referal': referal_code})
                .then(function(result){
                    if(result){
                        console.log("in function this")
                        $(".referd-by").css("color", "green");
                    }
                    else{
                        msg.html("Referd user deos not exist");
                        self.show_popup();
                    }
                })
            }
            else{
                msg.html("referal code must be 8 character");
                self.show_popup();
            }
        }
    },
    _onKeydownSearch:function(event){
        $(".referd-by").css("color", "red");
    },
    });
});