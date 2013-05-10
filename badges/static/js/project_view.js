/**************************************************************
 * Badges base.html template helper.
 **************************************************************/

/*global window */
/*global jQuery */

var Badges = window.Badges || {};

(function ($, Badges) {

    "use strict";
    var toggleDiv = function (selector, button) {
            var $this = $(selector);

            //Close div, if open.
            if ($this.hasClass('open')) {
                var originalHeight = $this.data('height');
                $this.animate({
                    height: originalHeight
                }, 'slow',
                    function () {
                        $(this).removeClass('open');
                        button.html('Show more');
                    });
                return false;
            }

            //Open the div
            var currentHeight =  $this.height(),
                autoHeight = $this.css('height', 'auto').height();
            $this.data('height', currentHeight)
                 .height(currentHeight)
                 .animate({
                    height: autoHeight
                }, 'slow',
                    function () {
                        $(this).addClass('open');
                        button.html('Show less');
                    });
        },

        init = function () {
            $(function () {
                var given_feedback = $('.feedback-already-given'),
                    $control_button = $('.show-more');

                if (given_feedback.height() < 290) {
                    given_feedback.parent().css('height', '300px');
                    $control_button.hide();
                } else {
                    $control_button.click(function(e) {
                        e.preventDefault();
                        toggleDiv($(this).attr('href'), $control_button);
                    });
                }
            });
        };



    Badges.ProjectView = {};
    Badges.ProjectView.init = init;

}(jQuery, Badges));


