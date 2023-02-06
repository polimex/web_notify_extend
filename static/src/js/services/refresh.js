odoo.define('web_notify_extend.WebClient', (require) => {
    "use strict";

    const MESSAGE_CHANNEL = 'polimex';
    let session;
    try {
        session = require('web.session');
    } catch (error) {
        console.error(`Error loading 'web.session': ${error}`);
        return;
    }

    let WebClient;
    try {
        WebClient = require('web.WebClient');
    } catch (error) {
        console.error(`Error loading 'web.WebClient': ${error}`);
        return;
    }

    let busService;
    try {
        busService = require("bus.BusService");
    } catch (error) {
        console.error(`Error loading 'bus.BusService': ${error}`);
        return;
    }

    WebClient.include({
        show_application: function () {
            let res = this._super.apply(this, arguments);
            this.register_channel();
            return res;
        },
        register_channel: function () {
            busService.startPolling();
            if (busService.isMasterTab()) {
                busService.addChannel(MESSAGE_CHANNEL);
            }
            busService.on("notification", this.polimex_msg.bind(this));
        },
        polimex_msg: function (messages) {
            let isMasterTab = busService.isMasterTab();
            let action = this.action_manager.getCurrentAction();
            let controller = this.action_manager.getCurrentController();
            console.log('Received messages: ', messages);
            for (let message of messages) {
                if (message[0] === MESSAGE_CHANNEL) {
                    console.log('Processing message: ', message[1]);
                    if (action && controller && message[1].m_type === 'refresh') {
                        if (!isMasterTab || session.uid !== message[1].uid &&
                            (controller.widget.modelName === message[1].model ||
                                controller.widget.isDashboard) &&
                            controller.widget.mode === "readonly") {
                            this._reload(message[1], controller);
                        } else if (controller.widget &&
                            controller.widget.modelName === 'board.board') {
                            this._reload(message[1], controller);
                        }
                    } else if (message[1].m_type === 'notify' &&
                        message[1].uids.includes(session.uid)) {
                        this.displayNotification(message[1]);
                    } else if (message[1].m_type === 'browser' &&
                        message[1].uids.includes(session.uid) && isMasterTab) {
                        this._sendNativeNotification(
                            message[1].title,
                            message[1].message,
                            message[1].icon,
                            message[1].requireInteraction
                        );
                        busService._beep();
                    }
                }
            }
        },
    })
})