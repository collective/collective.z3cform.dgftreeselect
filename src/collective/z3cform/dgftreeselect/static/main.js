/**
 * Multi-select tree choice helper javascript.
 */

/*global console*/

(function($) {

    "use strict";

    // Spit out or fancy logging messages?
    var debug = false;

    // Internal debug output
    function log(msg) {
        if(console && console.log && debug) {
            console.log(msg);
        }
    }

    /**
     * Get a debuf name for our DGF <table>
     * @param  {jQuery} elem selection for <table>
     */
    function getDGFName(elem) {
        var z3cWidget = elem.closest(".field");
        var name = z3cWidget.attr("id");
        return name;
    }

    var DGFTreeHelper = {

        dataCache : {},

        /**
         * Scale all DFG tree fields.
         *
         * Trigger AJAX load of the payload.
         *
         * After that move to per-widget initialization.
         *
         *
         */
        init : function() {

            var self =  this;

            var dgfs = $(".datagridwidget-table-view");

            dgfs.each(function() {
                var elem = $(this);
                self.initDGF(elem);

            });

            $(document.body).delegate(".datagridwidget-table-view", "beforeaddrow beforeaddrowauto", $.proxy(self.handleNestedDGFInsert, self));

        },

        /**
          * Delay AJAX calls for DataGridField widgets which are invisible by default
          */
        tryInitLater : function(elem) {
            var self = this;

            function checkIfBecomeVisible() {
                var name = getDGFName(elem);
                //log("Trying to initialize hidden:" + name);
                self.initDGF(elem, false);
            }
            window.setTimeout(checkIfBecomeVisible, 500);
        },

        /**
         * Initialize a datagridfield containing tree select widgets
         *
         * @param  {Objeect} elem .datagridwidget-table-view
         *
         * @param {Boolean} hiddenInit Initialize tree select widget even if
         *                  it is hidden. Otherwise we wait and poll
         *                  until the element becomes visibile
         *                  and after then trigger the AJAX request
         *                  loading the tree data.
         */
        initDGF : function(elem, hiddenInit) {
            var url = elem.attr("data-extra");
            var self = this;

            var name = getDGFName(elem);

            // Normal data grid field
            if(!url) {
                return;
            }

            // Avoid double init
            if(elem.data("tree-select-init")) {
                return;
            }

            // Check if we do hidden inits
            if(!hiddenInit) {

                // Wait until visible and poll back
                if(!elem.is(":visible")) {
                    //log("Postponing tree select init:" + name);
                    this.tryInitLater(elem);
                    return;
                }
            }

            // We have passed visibility check for the first time

            log("Initializing tree select:" + name);

            elem.data("tree-select-init", true);

            var field = elem.parent();

            // Make actual grid visible after it has been populated
            function got(data) {

                self.dataCache[url] = data;

                log("Got tree widget data:" + url);

                field.find(".tree-select-load").hide();
                self.populateTreeWidgets(elem, data);
                elem.show();

                // Set tree select event handler
                elem.delegate(".dgf-tree-select-widget", "change", $.proxy(self.handleSelect, self));
            }

            // JSON data reading over AJAX failed
            function fail(data) {
                window.console.error("Could not initialize:" + url);
            }

            // Check if we already have the tree data from this URL loaded on the same page
            var data = this.dataCache[url];

            if(data) {
                got(data);
            }  else {

                // Show the ajax spinner until we have data
                var img = window.portal_url + "/spinner.gif";
                var ajaxLoader = $("<img class='tree-select-load' src='" + img + "' />");
                field.prepend(ajaxLoader);
                //elem.hide();

                $.ajax({
                  url: url,
                  dataType: 'json',
                  data: null,
                  success: got,
                  error : fail
                });

            }
        },

        /**
         * See that if the datagridfield row contains nested tree select widgets and call
         * populateRow for them if needed.
         */
        handleNestedDGFInsert : function(event, dgf, row) {
            row = $(row);
            var dgfs = row.find(".datagridwidget-table-view");
            var self = this;

            dgfs.each(function() {
                var elem = $(this);
                self.initDGF(elem, true);
            });
        },

        /**
         * Get list of all parent ids so we can look our data source in the tree:
         *
         * @param {Object} select jQuery selection for <select>.
         */
        getParentChain : function(select) {

            var chain = [];

            while(select) {
                var master, masterId;

                masterId = select.attr("data-master-id");
                if(masterId) {
                    master = $("#" + masterId);
                } else {
                    master = null;
                }
                select = master;
            }

            chain.reverse();
            return chain;
        },


        /**
         * Get an element in array whose attribute key is set to value.
         */
        getNamedArrayElement : function(array, key, value) {
            var i;

            for(i=0; i<array.length; i++) {
                var elem = array[i];
                if(elem[key] == value) {
                    return elem;
                }
            }

            return undefined;
        },

        /**
         * Look-up selection list options data from a given parent in the source data tree.
         *
         * @param data: Array of choices
         */
        getOptionsList : function(data, parentValues) {

            // Clone array for working
            var chain = parentValues.slice();

            if(!chain) {
                return;
            }

            // Eat root note
            // chain.shift();

            // Walk down in the tree
            var id = chain.shift();

            while(id) {

                var desc = this.getNamedArrayElement(data, "id", id);
                if(!desc) {
                    return null;
                }

                id = chain.shift();
                data = desc["children"];
            }

            return data;
        },


        /**
         * Get all slaves for this select widget.
         */
        getSlaves : function(select) {
            var row = select.closest("tr");
            var slaves = [];
            while(true) {
                var slaveName = select.attr("data-slave-name");
                if(!slaveName) {
                    break;
                }

                select = row.find("select[data-tree-name=" + slaveName + "]");
                slaves.push(select);
            }

            return slaves;

        },

        getParentValues : function(select) {
            var row = select.closest("tr");

            var chain = [];
            var masterName;

            while(true) {
                masterName = select.attr("data-master-name");

                if(!masterName) {
                    break;
                }

                select = row.find("select[data-tree-name=" + masterName + "]");
                if(select.size() === 0) {
                    break;
                }
                chain.push(select.val());
            }

            chain.reverse();

            return chain;
        },


        /**
         * Initial population of the widge rows.
         *
         * After tree data is loaded, populate each
         * <select> with option list from the data and
         * select the initial value.
         */
        populateRow : function(elem, data, row) {

            var selects = row.children("td").children(".dgf-tree-select-widget");
            var i;

            for(i=0; i<selects.size(); i++) {
                var select = $(selects.get(i));
                log("Populating:" + select.attr("id") + " " + select.attr("data-initial-value"));
                select.data("treeData", data);
                this.refreshSelect(select, true);
            }
        },

        /**
         * (Re)populate <select> options after the parent has changed
         */
        refreshSelect : function(select, initialLoad) {

            var initialValue = select.attr("data-initial-value");

            function initOptions(select, options) {

                var i;

                for(i=0; i<options.length; i++) {
                    var src = options[i];
                    var opt = $("<option></option>");
                    opt.val(src.id);
                    opt.text(src.label);

                    if(initialValue == src.id && initialLoad) {
                        opt.attr("selected", true);
                    }

                    select.append(opt);
                }

            }


            var data = select.data("treeData");

            var chain = this.getParentValues(select);

            var options = this.getOptionsList(data, chain);

            //console.log("Initial value:" + initialValue);
            //console.log("Chain:" + chain);
            //console.log("Options:" + options);

            // No options availble
            if(!options) {
                select.hide();
                return;
            } else {
                select.show();
            }

            initOptions(select, options);
        },

        /**
         * Initial population of tree widgets after the tree data has loaded.
         *
         * :param elem: jQuery selection to the DataGridWidget
         */
        populateTreeWidgets : function(elem, data) {
            var self = this;

            $.each(elem.find("tr"), function() {
                self.populateRow(elem, data, $(this));
            });

            // The first <select> of last row (new row) must be visible
            // for user the be able to start data entering.
            // The final <tr> in <table> is the template row - don't select it
            var lastRow = elem.find("tr.auto-append").last();
            var firstSelect = lastRow.find("select").first();
            firstSelect.show();

            // Do the same for the template row
            lastRow = elem.find("tr.datagridwidget-empty-row").last();
            firstSelect = lastRow.find("select").first();
            firstSelect.show();

        },

        /**
         * Event handler for tree widget select choices.
         *
         */
        handleSelect : function(event) {
            var select = $(event.target);

            // Nuke out all the selections down in the chain
            // if any

            var slaves = this.getSlaves(select);
            $(slaves).each(function() {
                $(this).empty();
                $(this).hide();
            });

            // Initialize the next select widget in the chain
            if(slaves.length >= 1) {
                var neighbour = slaves[0];
                this.refreshSelect(neighbour);
            }

        }
    };

    $(document).ready(function() {
        // We need to make some timeout so that other possible field hiding
        // code has time to run before us, so that dynamic loading code does kick in
        // (All fields are visible by default, so is(":visible") does not work otherwise)
        setTimeout(function() {
            DGFTreeHelper.init();
        }, 20);

    });

    // Expose for monkey-patching
    window.DGFTreeHelper = DGFTreeHelper;

})(jQuery);