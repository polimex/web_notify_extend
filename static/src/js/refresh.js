odoo.define('ichecker.WebClient', function (require) {
"use strict";

var session = require('web.session');

var WebClient = require('web.WebClient');
// var core = require('web.core');
require("bus.BusService");

WebClient.include({
	show_application: function() {
		var res = this._super();
		this.start_polling();
		// this.call('bus_service', 'addChannel', 'ichecker_refresh');
        this._super.apply(this, arguments);

    },
	start_polling: function() {
            this.call("bus_service", "startPolling");

            if (this.call("bus_service", "isMasterTab")) {
                this.call("bus_service", "addChannel", 'ichecker_refresh');
            }
            this.call("bus_service", "on", "notification", this, this.ichecker_refresh);
        },
	ichecker_refresh: function(messages) {
		var self = this;
    	var action = this.action_manager.getCurrentAction();
    	var controller = this.action_manager.getCurrentController();
    	// console.log('Received event: ',messages)
		_.each(messages, function (m) {
			if ((m.length > 1)&&(controller)){
				// console.log('Received event: ',m[1])
				if((controller.widget)&&(controller.widget.modelName == 'board.board')){
					self._reload(m[1], controller);
				} else
				if (!self.call('bus_service', 'isMasterTab') || session.uid !== m[1].uid &&
					action && controller && (controller.widget.modelName === m[1].model || controller.widget.isDashboard) &&
					controller.widget.mode === "readonly") {
						var recordID = action.env.currentID || null; // pyUtils handles null value, not undefined
						if(controller.widget.isMultiRecord && (m[1].create || _.intersection(m[1].ids, action.env.ids) >= 1)) {
							self._reload(m[1], controller);
						} else if(!controller.widget.isMultiRecord && m[1].ids.includes(recordID)) {
							self._reload(m[1], controller);
						}
				}
			}
		})
    },
    _reload: function(message, controller) {
		if(controller && controller.widget) {
    		controller.widget.reload();
		}
    },
});

});