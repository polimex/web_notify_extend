from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

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

    def web_notify_followers(self, title, subtitle='', message='', sticky=False, m_type='info'):
        self.env['bus.bus'].sendone('polimex', {
            'm_type': 'notify',
            'title': title,
            'subtitle': subtitle,
            'message': message,
            'sticky': sticky,
            'type': m_type,
            'uids': self.mapped('id'),
        })

        # for follower in self:
        #     if follower.partner_id:
        #         msg['uids'] = follower.partner_id.user_ids
        #     self.env['bus.bus'].sendone('polimex', msg)
        # self.env['bus.bus'].sendone(
        #     (self._cr.dbname, 'res.partner', follower.partner_id.id),
        #     {'type': 'simple_notification', 'title': title, 'message': message,
        #      'sticky': sticky, 'warning': warning})



