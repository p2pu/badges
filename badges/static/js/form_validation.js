/*global jQuery, window, document, console, OpenBadges */

var Badges = window.Badges || {};

(function ($, Badges) {

    'use strict';

    var validate = function () {

        $(function () {
            $('#badge-create-form').parsley({
                trigger: 'change',
                successClass: 'success',
                errorClass: 'error',
                errors: {
                    classHandler: function (elem, isRadioOrCheckbox) {
                        return $(elem).parent().parent();
                    },
                    container: function (elem, isRadioOrCheckbox) {
                        var $container = $(elem).parent().parent().find(".control-group");
                        if ($container.length === 0) {
                            $container = $("<div class='help-inline'></div>").insertAfter(elem);
                        }
                        return $container;
                    }
                }
            });
        });
    };

    Badges.Form = {};
    Badges.Form.validate = validate;

}(jQuery, Badges));
