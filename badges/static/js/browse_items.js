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
                    debug        : false
                                    // enable debug messaging ( to console.log )
                  });
            });
        },

        user = function () {
            $(function () {
                $('#landing-users').infinitescroll({
                    loading: {
                        finished: undefined,
                        finishedMsg: "<em>Congratulations, you've reached the end of the internet.</em>",
                        img: "/static/img/preloader-spinner.gif",
                        msg: null,
                        msgText: "",
                        selector: '.next',
                        speed: 'fast',
                        start: undefined
                    },
                                   // options for loading
                    navSelector  : "div.navigation",
                                   // selector for the paged navigation (it will be hidden)
                    nextSelector : "div.navigation a:first",
                                   // selector for the NEXT link (to page 2)
                    itemSelector : ".p2pu-user",
                                   // selector for all items you'll retrieve
                    debug        : true,
                                    // enable debug messaging ( to console.log )
                     behavior    : 'twitter',
                  });

                 // unbind normal behavior.
                //$(window).unbind('.infscr');

                /*$('.load-more-learners').bind('click', function(){
                    $(document).trigger('retrieve.infscr');
                    return false;
                });*/

                $(document).ajaxError(function(e,xhr,opt){
                    if(xhr.status==404)$
                    ('.load-more-learners').remove();
                });
            });
        };

    Badges.Browse = {};
    Badges.Browse.init = init;
    Badges.Browse.user = user;

}(jQuery, Badges));