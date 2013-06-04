/*global jQuery, window, document, console, OpenBadges */

var Badges = window.Badges || {};

(function ($, Badges) {
    'use strict';

    var init = function () {
            $(function () {
                $('#badges').infinitescroll({
                    loading: {
                        finished: undefined,
                        finishedMsg: "<em>Congratulations, you've reached the end of the internet.</em>",
                        img: "/static/img/preloader.gif",
                        msg: null,
                        msgText: "<em>Loading the next set of Badges...</em>",
                        selector: null,
                        speed: 'fast',
                        start: undefined
                    },
                                   // options for loading
                    navSelector  : "div.navigation",
                                   // selector for the paged navigation (it will be hidden)
                    nextSelector : "div.navigation a:first",
                                   // selector for the NEXT link (to page 2)
                    itemSelector : ".p2pu-badge",
                                   // selector for all items you'll retrieve
                    debug        : true
                                    // enable debug messaging ( to console.log )
                  });
            });
        };

    Badges.Browse = {};
    Badges.Browse.init = init;

}(jQuery, Badges));