odoo.define('web_notify_extend.WebClient', function (require) {
"use strict";
const MESSAGE_CHANNEL = 'polimex'

var session = require('web.session');

var WebClient = require('web.WebClient');
// var core = require('web.core');
require("bus.BusService");

WebClient.include({
	show_application: function() {
		var res = this._super();
		// console.log('WebClient show_application')
		this.register_channel();
        return res;
    },
	register_channel: function() {
		this.call("bus_service", "startPolling");
		if (this.call("bus_service", "isMasterTab")) {
			this.call("bus_service", "addChannel", MESSAGE_CHANNEL);
			// console.log('Add channel: ',MESSAGE_CHANNEL)
		}
		this.call("bus_service", "on", "notification", this, this.polimex_msg);
		// console.log('Register for notification channel: ',this.polimex_msg)
    },
	polimex_msg: function(messages) {
		var self = this;
    	var action = this.action_manager.getCurrentAction();
    	var controller = this.action_manager.getCurrentController();
		console.log('Received messages: ',messages)
		_.each(_.filter(messages, function (e) {
            var channel = e[0];
            // var message = e[1];
            return MESSAGE_CHANNEL === channel
		}), function (m) {
			console.log('Proccessing message: ',m[1])
			var isMasterTab = self.call('bus_service', 'isMasterTab')
			if ((action)&&(controller)&&(m[1].m_type == 'refresh')){
				if (!isMasterTab || session.uid !== m[1].uid &&
					 (controller.widget.modelName === m[1].model || controller.widget.isDashboard) &&
					controller.widget.mode === "readonly") {
						// var recordID = action.env.currentID || null; // pyUtils handles null value, not undefined
						// if(controller.widget.isMultiRecord && (m[1].create || _.intersection(m[1].ids, action.env.ids) >= 1)) {
						// 	self._reload(m[1], controller);
						// } else if(!controller.widget.isMultiRecord && m[1].ids.includes(recordID)) {
						// 	self._reload(m[1], controller);
						// }
					self._reload(m[1], controller);
				} else
				if((controller.widget)&&(controller.widget.modelName == 'board.board')){
					self._reload(m[1], controller);
				}
			}
			else if ((m[1].m_type == 'notify')&&(m[1].uids.includes(session.uid))){
				self.displayNotification(m[1]);
			}
			else if ((m[1].m_type == 'browser')&&(m[1].uids.includes(session.uid))&&isMasterTab){
				self._sendNativeNotification( m[1].title, m[1].message, m[1].icon, m[1].requireInteraction);
				// self.call('bus_service', 'sendNotification', m[1].title,m[1].message);
				self.call('bus_service', '_beep');
			}
		})
    },
    _reload: function(message, controller) {
		if(controller && controller.widget) {
    		controller.widget.reload();
		}
    },
	 _sendNativeNotification: function (title, content, icon, requireInteraction=false, callback) {
		if (icon){
			var icn = icon
		} else {
			var icn = "/web_notify_extend/static/src/img/icon-90x90.png"
		}
		icn = session['web.base.url']+icn
		console.log('icon:',icn)
        var notification = new Notification(title, {
        	body: content,
			icon: icn,
			requireInteraction: requireInteraction,
        });
        notification.onclick = function () {
            window.focus();
            if (this.cancel) {
                this.cancel();
            } else if (this.close) {
                this.close();
            }
            if (callback) {
                callback();
            }
        };
    },
});

});