/*global jQuery, window, document, console, parsley */

var Badges = window.Badges || {};

(function ($, Badges) {

    'use strict';

    var validate = function (url) {

        var form = $('#badge-create-form');

        /*form.submit(function(e){
            console.log('pressed');
            e.preventDefault();
            return false;
        });*/

        // CKEditor field needs to be updated it first
        form.on('submit', function(){
            CKEDITOR.instances.id_requirements.updateElement();
        });

        $(function () {
            form.parsley({
                trigger: 'change keyup blur'
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
                  , onFormSubmit: function ( isFormValid, event, ParsleyForm ) {
                        $.each(ParsleyForm.items, function(e, elem) {
                            // Not giving the effect we want yet
                            var $this = $(elem.$element);
                            if ($this.attr('id') === 'id_title'){
                                $this.removeAttr('data-remote');
                            }
                        });
                    }
                  }
            });
        });
    };

    Badges.Form = {};
    Badges.Form.validate = validate;

}(jQuery, Badges));
