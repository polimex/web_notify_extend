from odoo import fields, models, api, _
from odoo.exceptions import UserError


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

    def notify_web(self, title, subtitle='', message='', sticky=False, m_type='info'):
        self.env['bus.bus'].sendone('polimex', {
            'm_type': 'notify',
            'title': title,
            'subtitle': subtitle,
            'message': message,
            'sticky': sticky,
            'type': m_type,
            'uids': self.mapped('id'),
        })

    def notify_browser(self, title, message, icon='', require_interaction=False):
        self.env['bus.bus'].sendone('polimex', {
            'm_type': 'browser',
            'title': title,
            'message': message,
            'icon':icon,
            'requireInteraction': require_interaction,
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

class UserNotifyWizard(models.TransientModel):
    _name = 'res.users.notify'

    def _get_users_ids(self):
        return self.env['res.users'].browse(self._context.get('active_ids'))

    user_ids = fields.Many2many(comodel_name='res.users', default=_get_users_ids)
    notify_type = fields.Selection([
        ('notify_info', 'Notify with Information'),
        ('notify_success', 'Notify with Success'),
        ('notify_warning', 'Notify with Warning'),
        ('notify_danger', 'Notify with Warning'),
        ('notify_browser', 'Browser Notification'),
    ], required=True)
    sticky = fields.Boolean(default=True)
    title = fields.Char(help='Message title', required=True)
    subtitle = fields.Char(help='Message subtitle')
    msg = fields.Text(help='Message body', required=True)

    def send(self):
        if not self.user_ids:
            UserError(_('No user to send message'))
        for user_id in self.user_ids:
            if self.notify_type == 'notify_browser':
                user_id.notify_browser(title=self.title, message=self.msg)
            else:
                m_type = self.notify_type.split('_')[1]
                user_id.notify_web(title=self.title,
                                   subtitle=self.subtitle,
                                   message=self.msg,
                                   sticky=self.sticky,
                                   m_type=m_type
                )



