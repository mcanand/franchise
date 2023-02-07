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
            'click .home_run' : '_render_dash_home',
            'click .menu_item' : '_render_links_space',
            'click .harmburger': '_click_side_nav_open',
            'click .link_select': '_click_link_select',
            'click .user_detail_form button': '_click_submit_values',
            'click .link_pop_up_close': '_click_popup_close',
            'click .link_pop_up_check': '_click_popup_check',
            'click .button_space_move': '_click_button_space_move',
            'click .continue_session': '_click_continue_session',
            'click .delete_order_line': '_click_delete_order_line',
            'click .delete_order': '_click_delete_current_order',
            'click .order_cancel': '_click_order_cancel',
            'click .confirm_button': '_click_order_confirm',
            'click .order_set':'_click_set_quotation',
            'click .order_paid':'_click_order_paid',
            'click .order_invoice_print': '_click_invoice_print',
            'click .order_complete': '_click_complete_order',
        },
        init: function(parent, context) {
            this._super(parent, context);
            this.login_employee = true;
            this._super(parent, context);
        },
        start: function() {
            var self = this;
            qweb.render('franchise_dashboard', {
                    widget: self
                });
            this._rpc({
                model: 'res.users',
                method: 'get_values',
                args: [[]],
            }).then(function(result) {
                self.user = result[0]
                self.categories = result[1]
                self.current_order_detail = false
                console.log(self.categories)
                $('.f_dash').prepend(qweb.render('dash_board', {
                    widget: self
                }))
                self._render_dash_home()
            });

            setInterval(function() {
              var status = navigator.onLine
              if(status == true){
                    $('.active_status').removeClass('background_red')
                    $('.active_status').addClass('background_green')
              }
              else{
                    $('.active_status').removeClass('background_green')
                    $('.active_status').addClass('background_red')
              }
        }, 2000);
        },
        _render_dash_home:function(){
             var self = this
                this._rpc({
                    model: 'sale.order',
                    method: 'get_active_order',
                    args: [[]],
                }).then(function(result) {
                    if(result != false){
                         self.order = result.order
                         self.order_lines = result.lines
                         self.invoice = result.invoice
                         if(result.lines != false){
                            self.line_length = result.lines.length
                         }
                         else{
                            self.line_length = 0
                         }
                         self.active_order = true
                         $('.action_space').html('')
                         $('.action_space').prepend(qweb.render('dash_home', {
                                widget: self
                         }))
                    }
                    else{
                        self.order = false
                        self.order_lines = false
                        self.invoice = false
                        self.active_order = false
                        $('.action_space').html('')
                        $('.action_space').prepend(qweb.render('dash_home', {
                               widget: self
                        }))
                    }
                });
        },
        _render_links_space:function(events){
            var self = this
            var category_id = $(events.target).parents('li').val()
            if(category_id){
                this._rpc({
                    model: 'res.users',
                    method: 'get_products',
                    args: [[],category_id],
                }).then(function(result) {
                    if(result){
                          self.products = result
                         $('.action_space').html('')
                         $('.action_space').prepend(qweb.render('dash_links', {
                                widget: self
                         }))
                    }

                });
            }
        },
        _click_side_nav_open:function(){
            if($('#mySidenav').hasClass('opened')){
                $('.user_detail').animate({opacity:'0'})
                $('#mySidenav').removeClass('opened')
                $('.menu_text').hide()
                $('.user_detail').animate({height:'0%'})
                setTimeout(function(){
                    $('#mySidenav').css({'width':'53px'})
                    $('#main').css({'margin-left':'53px'})
                },500)
            }
            else{
                $('#mySidenav').addClass('opened')
                setTimeout(function(){
                    $('.menu_text').css({'display':'contents'})
                    $('.user_detail').animate({height:'30%'})
                    $('.user_detail').animate({opacity:'1'})
                },500)

                $('#mySidenav').css({'width':'250px'})
                $('#main').css({'margin-left':'250px'})
            }
        },
        _click_link_select:function(event){
            var self = this
            var product_id = $(event.target).val()
            if(this.order != false){
                /*if current_order_detail present*/
                var vals = {'order_id':this.order.id,'product_id':product_id}
                this._rpc({
                    model: 'product.template',
                    method: 'get_product_create_line',
                    args: [[],vals],
                }).then(function(result) {
                    if(result != false){
                         $('.dash_link_popup').prepend(qweb.render('link_pop_up', {
                            widget: self
                        }));
                        $('.content_load').children().remove()
                        $('.content_load').append('<iframe src="'+result.url+'"></iframe>')
                        $('.link_pop_up_check').removeClass('d-none')
                        $('.continue_session').removeClass('d-none')
                    }
                });
            }
            else{
               self.current_product_id = product_id
               console.log('link select else', self)
               $('.dash_link_popup').prepend(qweb.render('link_pop_up', {
                        widget: self
               }));
            }
        },
        _click_submit_values:function(){
            var name = $("input[name='name']").val()
            var mobile = $("input[name='mobile']").val()
            var address = $("input[name='address']").val()
            var age = $("input[name='age']").val()
            var zip = $("input[name='zip']").val()
            var location = $("input[name='location']").val()
            var street = $("input[name='street']").val()
            var self = this
            var vals = {name:name,
                        mobile:mobile,
                        address:address,
                        age:age,
                        zip:zip,
                        location:location,
                        street:street}
            if(!name || !mobile || !street || !zip){
                $('.errors').html('Please Fill up the fields')
            }
            else{
                vals['product_id'] = self.current_product_id
                console.log('sadsad',vals)
                this._rpc({
                    route: '/save/customer/create/order',
                    params: {vals: vals}
                }).then(function(result) {
                    if(result != false){
                        self.current_order_detail = result
                        $('.customer_id').val(result.customer_id)
                        $('.content_load').children().remove()
                        $('.content_load').append('<iframe src="'+result.product_url+'"></iframe>')
                        $('.link_pop_up_check').removeClass('d-none')
                        $('.continue_session').removeClass('d-none')
                    }
                });
            }
        },
        _click_popup_close:function(){
            if(this.current_order_detail != false){
                this.delete_current_order(this.current_order_detail.order_id)
                this.current_products = false
                this.current_order_detail = false
                $('.dash_link_popup').children().remove()
            }
            else{
                $('.dash_link_popup').children().remove()
                this.current_products = false
                this.current_order_detail = false
            }
        },
        _click_button_space_move:function(){
            if($('.buttons_space').hasClass('moved')){
                $('.buttons_space').animate({right: "-=400px"},400)
                $('.buttons_space').removeClass('moved')
                $('.button_space_move').children().remove()
                $('.button_space_move').append("<i class='fa fa-angle-left'/>")
            }
            else{
                $('.buttons_space').animate({right: "+=400px"},400)
                $('.buttons_space').addClass('moved')
                $('.button_space_move').children().remove()
                $('.button_space_move').append("<i class='fa fa-angle-right'/>")
            }
        },
        _click_popup_check:function(event){
               $('.dash_link_popup').children().remove()
                this._render_dash_home()
        },
        _click_continue_session:function(){
            $('.dash_link_popup').children().remove()

        },
        delete_current_order:function(order_id){
            var self = this
                this._rpc({
                    model: 'sale.order',
                    method: 'delete_current_order',
                    args: [[],order_id],
                });
        },
        _click_delete_order_line:function(event){
            var line_id = $(event.target).attr('data-id')
            var self = this
            console.log('line_id',line_id)
            this._rpc({
                    model: 'sale.order.line',
                    method: 'delete_order_line',
                    args: [[],line_id],
                }).then(function(result) {
                     if(result){
                        self._render_dash_home()
                     }
                });
        },
        _click_delete_current_order:function(event){
           var self = this
           var order_id = $(event.target).attr('data-id')
           console.log('order_delte',order_id)
           this._rpc({
                    model: 'sale.order',
                    method: 'delete_current_order',
                    args: [[],order_id],
                }).then(function(result){
                    if(result){
                        self.current_products = false
                        self.current_order_detail = false
                        self._render_dash_home()
                    }
                });
        },
        _click_order_cancel:function(event){
            var order_id = $(event.target).attr('data-id')
            var self = this
            this._rpc({
                model: 'sale.order',
                method: 'order_cancel',
                args: [[],order_id],
            }).then(function(result){
                if(result != false){
                    self._render_dash_home()
                }
            });
        },
        _click_order_confirm:function(event){
            var self = this
            var order_id = $(event.target).attr('data-id')
            this._rpc({
                    model: 'sale.order',
                    method: 'confirm_order',
                    args: [[],order_id],
                }).then(function(result) {
                    if(result != false){
                        self._render_dash_home()
                    }
                });
        },
        _click_set_quotation:function(event){
            var self = this
            var order_id = $(event.target).attr('data-id')
            this._rpc({
                    model: 'sale.order',
                    method: 'order_set_quotation',
                    args: [[],order_id],
                }).then(function(result) {
                    self._render_dash_home()
                });
        },
        _click_order_paid:function(event){
            var self = this
            var invoice_id = $(event.target).attr('data-id')
            this._rpc({
                    model: 'account.move',
                    method: 'order_paid',
                    args: [[],invoice_id],
                }).then(function(result) {
                    if(result != false){
                        self._render_dash_home()
                    }
                });
        },
        _click_invoice_print:function(){
            this.printContent = $('<iframe id="print_iframe_content" src="' + this.invoice.print_url + '" style="display:none"></iframe>');
            this.$el.append(this.printContent);
            this.printContent.on('load', function () {
                $(this).get(0).contentWindow.print();
            });
        },
        _click_complete_order:function(event){
            var self = this
            var order_id = $(event.target).attr('data-id')
            this._rpc({
                    model: 'sale.order',
                    method: 'complete_order',
                    args: [[],order_id],
                }).then(function(result) {
                    if(result != false){
                        self._render_dash_home()
                    }
                });
        },

    });

    core.action_registry.add('franchise_dashboard_tag', FranchiseDashboard);
    return FranchiseDashboard;
});