/*global jQuery, window, document, console, OpenBadges */

var P2PU_OpenBadges = window.P2PU_OpenBadges || {};

(function ($, P2PU_OpenBadges) {
    'use strict';

    var
        callback = function () {
            var $this = $(this),
                assertion_url = $this.data('assertion-url'),
                pushed_to_backpack_url = $this.data('pushed-to-backpack-url');

            OpenBadges.issue([assertion_url], function (errors, successes) {
                if (successes.length === 1) {
                    $.get(pushed_to_backpack_url, function () {
                        $this.removeClass('btn-primary').addClass('disabled').html('In backpack');
                    });
                }
            });
        },

        init = function (push_to_backpack_class) {
            $(function () {
                $(push_to_backpack_class).click(callback);
            });
        };

    P2PU_OpenBadges.Issuer = {};
    P2PU_OpenBadges.Issuer.init = init;

}(jQuery, P2PU_OpenBadges));