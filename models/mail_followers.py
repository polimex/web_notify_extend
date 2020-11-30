from odoo import models


class Followers(models.Model):
    """ mail_followers holds the data related to the follow mechanism inside
    Odoo. Partners can choose to follow documents (records) of any kind
    that inherits from mail.thread. Following documents allow to receive
    notifications for new messages. A subscription is characterized by:

    :param: res_model: model of the followed objects
    :param: res_id: ID of resource (may be 0 for every objects)
    """
    _inherit = 'mail.followers'

    def notify_followers(self, title, message, sticky=True, warning=True):
        for follower in self:
            self.env['bus.bus'].sendone(
                (self._cr.dbname, 'res.partner', follower.partner_id.id),
                {'type': 'simple_notification', 'title': title, 'message': message,
                 'sticky': sticky, 'warning': warning})
    


