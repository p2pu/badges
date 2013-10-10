/*global jQuery, window, document, console, parsley */

var Badges = window.Badges || {};

(function ($, Badges) {

    'use strict';

    var validate = function (url) {
        /*$('#badge-create-form').submit(function(e){
            console.log('pressed');
            e.preventDefault();
            return false;
        });*/
        var form = $('#badge-create-form');

        // CKEditor field needs to be updated it first
        form.on('submit', function(){
            CKEDITOR.instances.id_requirements.updateElement();
        });

        $(function () {
            form.parsley({
                trigger: 'change'
                , validateIfUnchanged: false
                , successClass: 'success'
                , errorClass: 'error'
                , errors: {
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
                , listeners: {
                    onFieldValidate: function (elem, ParsleyField) {

                        // if field is readonly, do not apply Parsley validation!
                        return ($(elem).is('[readonly]'));


                    }
                  }
            });
        });
    };

    Badges.Form = {};
    Badges.Form.validate = validate;

}(jQuery, Badges));
