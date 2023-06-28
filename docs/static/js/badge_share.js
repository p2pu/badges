/*global jQuery, window, document, console, OpenBadges */

var Badges = window.Badges || {};

(function ($, Badges) {

    'use strict';

    var share = function () {

        $(function () {
            var share_control = $('.btn-share'),
                embed_control = $('.btn-embed'),
                share_panel = $('.badge-sharing-inner-wrap'),
                textarea = $('.badge-sharing-inner').find('textarea');

            share_control.bind('click', function (e) {
                e.preventDefault();
                var $this = $(this);
                $this.addClass('active');
                embed_control.removeClass('active');
                share_panel.animate({
                    left: 0
                });
            });

            embed_control.bind('click', function (e) {
                e.preventDefault();
                var $this = $(this);
                $this.addClass('active');
                share_control.removeClass('active');
                share_panel.animate({
                    left: '-100%'
                });
            });

            textarea.bind('click', function (e) {
                var $this = $(this);
                $this.select();
            });
        });
    };

    Badges.Tile = {};
    Badges.Tile.share = share;

}(jQuery, Badges));
