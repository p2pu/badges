/**************************************************************
 * Badges base.html template helper.
 **************************************************************/

/*global window */
/*global jQuery */
/*global console */

var Badges = window.Badges || {};

(function ($, Badges) {

    "use strict";
    var init = function () {
            $(function () {
                var $delete_button = $('*[data-delete="p2pu-badge"]'),
                    $badge_delete_cancel = $('.badge-delete-cancel');

                $delete_button.on('click', function (e) {
                    e.preventDefault();
                    var $this = $(this),
                        $badge_popover = $this.parent().find('.badge-delete-popover');
                    $badge_popover.css('display', 'block');
                });

                $badge_delete_cancel.on('click', function (e) {
                    var $badge_popover = $('.badge-delete-popover');
                    e.preventDefault();
                    $badge_popover.css('display', 'none');
                });
            });
        };



    Badges.Dashboard = {};
    Badges.Dashboard.init = init;

}(jQuery, Badges));


