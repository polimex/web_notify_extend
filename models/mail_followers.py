from odoo import models

import logging
_logger = logging.getLogger(__name__)

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

    def notify_web_followers(self, title, subtitle='', message='', sticky=False, m_type='info'):
        for f in self:
            f.partner_id.user_ids.notify_web(title, subtitle, message, sticky, m_type)
            # uids = f.mapped('partner_id.user_ids.id')
            _logger.info('Notify uids: '+str(f.mapped('partner_id.user_ids.id'))+', message: '+ message)
            # self.env['bus.bus'].sendone('polimex', {
            #     'm_type': 'notify',
            #     'title': title,
            #     'subtitle': subtitle,
            #     'message': message,
            #     'sticky': sticky,
            #     'type': m_type,
            #     'uids': uids,
            # })

    def notify_browser_followers(self, title, message):
        for f in self:
            f.partner_id.user_ids.notify_browser(title, message)
            # uids = f.mapped('partner_id.user_ids.id')
            _logger.info('Browser Notify uids: '+str(f.mapped('partner_id.user_ids.id'))+', message: '+ message)
            # self.env['bus.bus'].sendone('polimex', {
            #     'm_type': 'browser',
            #     'title': title,
            #     'message': message,
            #     'uids': uids,
            # })