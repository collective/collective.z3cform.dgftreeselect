(function($) {

    "use strict";

    var DGFTreeHelper = {

        /**
         * Scale all DFG tree fields.
         *
         * Trigger AJAX load of the payload.
         *
         * After that move to per-widget initialization.
         */
        init : function(elem) {

            var self =  this;

            $(".dgf-tree-select-widget").each(function() {
                var elem = $(this);
                var url = elem.attr("data-source-url");


                function got(data) {
                    self.initTreeWidgets(elem, data);
                }

                $.get(url, got);
            });
        },

        initTreeWidgets : function(elem, data) {
            window.alert(data);
        }
    };

    $(document).ready(function() {
        DGFTreeHelper.init();
    });

    // Expose for monkey-patching
    window.DGFTreeHelper = DGFTreeHelper;

})(jQuery);