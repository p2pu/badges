/*global jQuery, window, document, console, OpenBadges */

var Badges = window.Badges || {};

(function ($, Badges) {

    'use strict';

    var share = function () {

        $(function () {
            var share_control = $('.badge-share-control'),
                textarea = $('.p2pu-badge').find('textarea');

            share_control.bind('click', function (e) {
                e.preventDefault();
                var $this = $(this),
                    container = $this.parents('.badge-info'),
                    slide_content = container.find('.badge-social');

                slide_content.slideToggle('slow', function () {
                    console.log($(this));
                });

                /*
                    slide_content = container.find('.badge-description-wrap'),
                    left_set = slide_content.css('left') === '0px',
                    left = '0px',
                    add_class = 'icon-share-sign',
                    remove_clas = 'icon-info-sign',
                    share = '',
                    info = 'hidden';

                if (left_set) {
                    left = '-180px';
                    add_class = 'icon-info-sign';
                    remove_clas = 'icon-share-sign';
                    share = 'hidden';
                    info = '';
                }
                slide_content.animate({
                    left: left
                }, {
                    duration: 200,
                    complete: function () {
                        var text = $(this).next('.badge-controls').find('.badge-share-control a');
                        text.find('i').addClass(add_class).removeClass(remove_clas);
                        text.find('.share').removeClass('hidden').addClass(share);
                        text.find('.info').removeClass('hidden').addClass(info);
                    }
                });*/

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
