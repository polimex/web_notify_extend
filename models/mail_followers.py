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

    '''
    **
     * Displays a notification.
     *
     * @param {Object} options
     * @param {string} options.title
     * @param {string} [options.subtitle]
     * @param {string} [options.message]
     * @param {string} [options.type='warning'] 'info', 'success', 'warning', 'danger' or ''
     * @param {boolean} [options.sticky=false]
     * @param {string} [options.className]
     */
    displayNotification: function (options) {
        return this.call('notification', 'notify', options);
    },
    '''

    def notify_followers(self, title, subtitle='', message='', sticky=False, m_type='info'):
        for f in self:
            uids = f.mapped('partner_id.user_ids.id')
            self.env['bus.bus'].sendone('polimex', {
                'm_type': 'notify',
                'title': title,
                'subtitle': subtitle,
                'message': message,
                'sticky': sticky,
                'type': m_type,
                'uids': uids,
            })

        # for follower in self:
        #     if follower.partner_id:
        #         msg['uids'] = follower.partner_id.user_ids
        #     self.env['bus.bus'].sendone('polimex', msg)
            # self.env['bus.bus'].sendone(
            #     (self._cr.dbname, 'res.partner', follower.partner_id.id),
            #     {'type': 'simple_notification', 'title': title, 'message': message,
            #      'sticky': sticky, 'warning': warning})
