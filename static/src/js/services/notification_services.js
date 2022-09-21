odoo.define("web_notify.NotificationService", function (require) {
    "use strict";
    const {browser} = require("@web/core/browser/browser");
    const {registry} = require("@web/core/registry");

    const webNotificationService = {
        dependencies: ["notification"],

        start(env, {notification}) {
            let webNotifTimeouts = {};
            /**
             * Displays the web notification on user's screen
             */

            function displaywebNotification(notifications) {
                Object.values(webNotifTimeouts).forEach((notif) =>
                    browser.clearTimeout(notif)
                );
                webNotifTimeouts = {};

                notifications.forEach(function (notif) {
                    browser.setTimeout(function () {
                        notification.add(notif.message, {
                            title: notif.title,
                            type: notif.type,
                            sticky: notif.sticky,
                            className: notif.className,
                        });
                    });
                });
            }
            env.bus.on("WEB_CLIENT_READY", null, async () => {
                const legacyEnv = owl.Component.env;
                legacyEnv.services.bus_service.onNotification(this, (notifications) => {
                    for (const {payload, type} of notifications) {
                        if (type === "web.notify") {
                            if (payload[0].type == 'browser'){
                                legacyEnv.services.bus_service.sendNotification(payload[0]);
                                // legacyEnv.services.bus_service._sendNativeNotification(payload[0].title, payload[0].message);
                                // legacyEnv.services.bus_service._beep();
                            } else if (payload[0].type == 'refresh'){

                            } else
                            displaywebNotification(payload);
                        }
                    }
                });
                legacyEnv.services.bus_service.startPolling();
            });
        },
    };

    registry.category("services").add("webNotification", webNotificationService);
});
