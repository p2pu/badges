/*global jQuery, window, document, console, OpenBadges */

var Badges = window.Badges || {};

(function ($, Badges) {
    'use strict';

    var init = function () {
        $(function () {
            $(".p2pu-tab").p2puSlider({
                navbarContainer: '.navbar',
                icon: '.p2pu-tab-icon',
                iconUp: 'icon-chevron-sign-down',
                iconDown: 'icon-chevron-sign-up'
            });

            dropdown_search_handler();
            clear_search_button_handler();
            side_plugin_handler();
        });
    };

    var dropdown_search_handler = function() {
        var search_form = $('.dropdown-menu'),
                dropdown_button = $('.dropdown-toggle');

            $(document).bind('click', function() {
               search_form.hide();
            });

            dropdown_button.on('click', function(){
                if(search_form.is(':visible')) {
                    search_form.hide();
                }else{
                    search_form.show();

                }
            });

            search_form.bind('click', function(e) {
                $(e.currentTarget).css('display', 'block');
                dropdown_button.parent().addClass('open');
                return false;
            });
    };

    var clear_search_button_handler = function() {
        var clear = $('.clear-search'),
                search = $('.search');

            clear.bind('click', function() {
                search.val('');
            });
    };

    var side_plugin_handler = function() {
        //var colapse_button = $('[data-toggle="collapse"]');

        $('.navbar-btn').sidr({
                name: 'main-menu-panel',
                source: '.nav-collapse.collapse'
            });


        /*var menu = $('.mindevices-side-menu');

        var jPM = $.jPanelMenu({
            menu: '.mindevices-side-menu',
            trigger: '[data-toggle="collapse"]',
            duration: 300
        });
        jPM.on();

        colapse_button.on('click', function() {
            menu.css('height', '0')
        });*/
    };

    Badges.Splash = {};
    Badges.Splash.init = init;

}(jQuery, Badges));