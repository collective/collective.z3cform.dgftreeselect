/**
 * Multi-select tree choice helper javascript.
 */

(function($) {

    "use strict";

    var DGFTreeHelper = {

        dataSources : {},

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
                var url = elem.attr("data-extra");

                // Normal data grid field
                if(!url) {
                    return;
                }

                function got(data) {
                    self.populateTreeWidgets(elem, data);
                }

                $.getJSON(url, got);
            });

            // Set global event handler
            dgfs.delegate(".dgf-tree-select-widget", "change", $.proxy(this.handleSelect, this));
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
                console.log("Populating:" + select.attr("id") + " " + select.attr("data-initial-value"));
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

            console.log("Initial value:" + initialValue);
            console.log("Chain:" + chain);
            console.log("Options:" + options);

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
        DGFTreeHelper.init();
    });

    // Expose for monkey-patching
    window.DGFTreeHelper = DGFTreeHelper;

})(jQuery);