from odoo import fields, models, api
from odoo.addons.bus.controllers.main import BusController
from odoo.http import request

class IcheckerBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # add new channel
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'ichecker_refresh', request.env.user.partner_id.id))
        return super(IcheckerBusController, self)._poll(dbname, channels, last, options)
