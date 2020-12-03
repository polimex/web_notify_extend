from odoo import fields, models, api
from odoo.addons.bus.controllers.main import BusController
from odoo.http import request

class PolimexBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # add new channel
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'polimex', request.env.user.partner_id.id))
        return super(PolimexBusController, self)._poll(dbname, channels, last, options)
