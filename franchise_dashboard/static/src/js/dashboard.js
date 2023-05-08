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
    var utils = require('web.utils');

    var FranchiseDashboard = AbstractAction.extend({
        template: "franchise_dashboard",
        events: {
            'click .home_run' : '_render_dash_home',
            'click .menu_item' : '_render_links_space',
            'click .f_settings':'_render_settings',
            'click .f_download':'_render_downloads',
            'click .file_download':'_file_download',
//            'click .harmburger': '_click_side_nav_open',
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
            'click .home_menu':'_click_home_menu',
            'click .customer_edit': '_click_edit_customer',
            'click .customer_save': '_click_save_customer',
            'mouseover .sale_line_view': '_hover_sale_line_view',
            'mouseout .sale_line_view': '_hoverout_sale_line_view',
            'keyup #mobile':'_keyup_input_mobile',
            'keyup .product_search_b_catefg': '_search_product_by_category',
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
        get_random_color:function() {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++ ) {
                color += letters[Math.round(Math.random() * 15)];
            }
            var bg = "background-color:"+color+" !important;"
            return bg;
        },
        _render_dash_home:function(){
             var self = this
                this._rpc({
                    model: 'sale.order',
                    method: 'get_active_order',
                    args: [[]],
                }).then(function(result) {
                    if(result != false){
                         var binary = result.bg_image.replace(/(..)/gim,'%$1');
                         console.log('anand',typeof(binary),binary)
                         self.bg_image = binary

                         self.total_customers = result.total_customers
                         self.total_services = result.total_service
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
//                         $('.dash_home').css({"background-image":" url('data:image/png;base64,"self.bg_image+"');)"})
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
        _render_settings:function(){
            var self = this
            console.log('settings0, this',this)
            $('.action_space').html('')
            $('.action_space').prepend(qweb.render('franchise_settings', {
                widget: self
            }))
        },
        _render_downloads:function(){
            var self = this
            this._rpc({
                    route: '/franchise/files',
                    params: {}
                }).then(function(result){
                    if(result){
                        self.files = result
                        $('.action_space').html('')
                        $('.action_space').prepend(qweb.render('downloads', {
                            widget: self
                        }))
                    }
                });
        },
        _file_download:function(events){
            var self = this
            this.modelName = 'franchise.files'
            this.id = $(events.target).attr('data-id')
            var file_id = $(events.target).attr('data-id')
            window.location = `/web/content/${this.modelName}/${this.id}/file?download=true`;
//            alert(file_id)
//            this._rpc({
//                    route: '/files/download',
//                    params: {file_id:file_id}
//                }).then(function(result){
////                    self.do_action({type: 'ir.actions.act_url', url: result});
//
//                });
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
                          self.category_id = category_id
                         $('.action_space').html('')
                         $('.action_space').prepend(qweb.render('dash_links', {
                                widget: self
                         }))
                    }

                });
            }
        },
        _keyup_input_mobile:function(event){
            var number = $(event.target).val()
            if(number.length > 4){
                this._rpc({
                    route: '/find/customer/address',
                    params: {number: number}
                }).then(function(result){
                    if(result != false){
                        $("input[name='name']").val(result.name)
//                        $("input[name='mobile']").val(result.mobile)
                        $("input[name='street']").val(result.street)
                        $("input[name='street2']").val(result.street2)
                        $("input[name='email']").val(result.email)
                    }
                })
            }

        },
        /*_click_side_nav_open:function(){
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
        },*/
        _click_link_select:function(event){
            var self = this
            var product_id = $(event.target).val()
//            if(this.order != false){
                /*if current_order_detail present*/
                self.current_product_id = product_id
//                var vals = {'order_id':this.order.id,'product_id':product_id}
                var vals = {'product_id':product_id}
                this._rpc({
                    model: 'product.product',
                    method: 'get_product_create_line',
                    args: [[],vals],
                }).then(function(result) {
                    if(result != false){
//                         $('.dash_link_popup').prepend(qweb.render('link_pop_up', {
//                            widget: self
//                        }));
//                        $('.content_load').children().remove()
//                        $('.content_load').append('<iframe src="'+result.url+'"></iframe>')
                        window.open(result.url, '_blank');
//                        $('.link_pop_up_check').removeClass('d-none')
//                        $('.continue_session').removeClass('d-none')
//                        self._render_dash_home()
                    }
                });
//            }
//            else{
//               self.current_product_id = product_id
//               $('.dash_link_popup').prepend(qweb.render('link_pop_up', {
//                        widget: self
//               }));
               /*next button goes to _click_submit_values*/

        },
        _click_submit_values:function(){
            var name = $("input[name='name']").val()
            var mobile = $("input[name='mobile']").val()
            var street = $("input[name='street']").val()
            var street2 = $("input[name='street2']").val()
            var email = $("input[name='email']").val()
            var self = this
            var vals = {name:name,
                        mobile:mobile,
                        street:street,
                        street2:street2,
                        email:email}
            if(!name ){
                $('.errors').html('Please Fill up customer name')
                $("input[name='name']").addClass('border_red')
            }
            else if(!mobile){
                $('.errors').html('Please Fill up customer address')
                $("input[name='mobile']").addClass('border_red')
            }
            else if(!street){
                ('.errors').html('Please Fill up customer Mobile Number')
                $("input[name='street']").addClass('border_red')
            }
            else{
                vals['product_id'] = self.current_product_id
                this._rpc({
                    route: '/save/customer/create/order',
                    params: {vals: vals}
                }).then(function(result) {
                    if(result != false){
                        self.current_order_detail = result
                        $('.customer_id').val(result.customer_id)
                        $('.content_load').children().remove()
//                        $('.content_load').append('<iframe src="'+result.product_url+'"></iframe>')

                        window.open(result.product_url, '_blank');
                        $('.link_pop_up_check').removeClass('d-none')
                        $('.continue_session').removeClass('d-none')
                        self._render_dash_home()
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
            this.order = true
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
        _click_home_menu:function(event){
            var val = $(event.target).val()
            var self = this
            console.log('sadasd',val)
            this._rpc({
                model: 'sale.order',
                method: 'get_values',
                args: [[],val],
            }).then(function(result){
                self.menu_val = val
                if(result != false){
                    $('.action_space').html('')
                    $('.action_space').prepend(qweb.render('show_details_layout', {
                        widget: self
                    }))
                    if(val == 'partner'){
                        self.customers = result
                        $('.show_details_space').prepend(qweb.render('customer_view', {
                            widget: self
                        }))
                    }
                    else if(val == 'sales'){
                        self.sale_orders = result
                        $('.show_details_space').html('')
                        $('.show_details_space').prepend(qweb.render('sales_view', {
                            widget: self
                        }))
                    }
                    else if(val == 'invoice'){
                        self.invoice_details = result
                        $('.show_details_space').html('')
                        $('.show_details_space').prepend(qweb.render('invoice_view', {
                            widget: self
                        }))
                    }
                }
            });
        },
        _hover_sale_line_view:function(event){
            var order_id = $(event.target).attr('data-id')
            var self = this
            this._rpc({
                model: 'sale.order',
                method: 'get_sale_order_lines',
                args: [[],order_id],
            }).then(function(result){
                self.sale_view_lines = result
                $('.order_line_pop_up_space').html('')
                $('.order_line_pop_up_space').prepend(qweb.render('order_line_pop_up', {
                    widget: self
                }))
            });
        },
        _hoverout_sale_line_view:function(event){
            $('.order_line_pop_up_space').html('')

        },
        _click_edit_customer:function(event){
            var customer_id = $(event.target).attr('data-id')
            $('.customer_' + customer_id + ' input').removeAttr('readonly')
            $('.customer_' + customer_id + ' input').css({'border-bottom':'1px solid blue'})
            $(event.target).addClass('d-none')
            $(event.target).siblings('i').removeClass('d-none')
        },
        _click_save_customer:function(event){
            var vals = {}
            var customer_id = $(event.target).attr('data-id')
            _.each($('.customer_' + customer_id + ' input'),function(result){
                vals[$(result).attr('name')] = $(result).val()
            })
            var self = this
            this._rpc({
                model: 'res.partner',
                method: 'update_partner',
                args: [[],vals,customer_id],
            }).then(function(result){
                if(result != false){
                    $('.customer_' + customer_id + ' input').css({'border-bottom':'0px'})
                    $('.customer_' + customer_id + ' input').attr('readonly','readonly')
                    $(event.target).addClass('d-none')
                    $(event.target).siblings('i').removeClass('d-none')
                }
            });

        },
        _search_product_by_category:function(event){
            var input_val = $(event.target).val()
            var category_id = this.category_id
            var self = this
            var vals = {
                'input_val':input_val,
                'category_id':category_id
            }
//
//            process_links
            this._rpc({
                    route: '/search/product',
                    params: {vals: vals}
                }).then(function(result) {
                    self.products = result
//                    $(".process_links").load(location.href + " .process_links");
                    $('.action_space').html('')
                     $('.action_space').prepend(qweb.render('dash_links', {
                            widget: self
                     }))
                     $('.product_search_b_catefg').val(input_val)
                     $('.product_search_b_catefg').focus()
                });
        },
    });

    core.action_registry.add('franchise_dashboard_tag', FranchiseDashboard);
    return FranchiseDashboard;
});