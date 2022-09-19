from odoo import fields, models, api, _, exceptions
from odoo.addons.bus.models.bus import channel_with_db, json_dump

DEFAULT_MESSAGE = "Default message"

SUCCESS = "success"
DANGER = "danger"
WARNING = "warning"
INFO = "info"
DEFAULT = "default"
BROWSER = "browser"
class Users(models.Model):
    _inherit = 'res.users'

    @api.depends("create_date")
    def _compute_channel_names(self):
        for record in self:
            record.notify_success_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )
            record.notify_danger_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )
            record.notify_warning_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )
            record.notify_info_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )
            record.notify_default_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )
            record.notify_browser_channel_name = json_dump(
                channel_with_db(self.env.cr.dbname, record.partner_id)
            )

    notify_success_channel_name = fields.Char(compute="_compute_channel_names")
    notify_danger_channel_name = fields.Char(compute="_compute_channel_names")
    notify_warning_channel_name = fields.Char(compute="_compute_channel_names")
    notify_info_channel_name = fields.Char(compute="_compute_channel_names")
    notify_default_channel_name = fields.Char(compute="_compute_channel_names")
    notify_browser_channel_name = fields.Char(compute="_compute_channel_names")

    def _notify_channel(
        self,
        type_message=DEFAULT,
        message=DEFAULT_MESSAGE,
        title=None,
        sticky=False,
        target=None,
    ):
        # pylint: disable=protected-access
        if not self.env.user._is_admin() and any(
            user.id != self.env.uid for user in self
        ):
            raise exceptions.UserError(
                _("Sending a notification to another user is forbidden.")
            )
        if not target:
            target = self.env.user.partner_id
        bus_message = {
            "type": type_message,
            "message": message,
            "title": title,
            "sticky": sticky,
        }

        notifications = [[partner, "web.notify", [bus_message]] for partner in target]
        self.env["bus.bus"]._sendmany(notifications)

    def notify_web(self, title=None, subtitle='', message='', sticky=False, m_type='info'):
        # self.env['bus.bus']._sendone('polimex', {
        #     'm_type': 'notify',
        #     'title': title,
        #     'subtitle': subtitle,
        #     'message': message,
        #     'sticky': sticky,
        #     'type': m_type,
        #     'uids': self.mapped('id'),
        # })
        # self._notify_channel(m_type, message, title, sticky, target)
        self._notify_channel(m_type, message, title, sticky, None)

    def notify_success(
        self, message="Default message", title=None, sticky=False, target=None
    ):
        title = title or _("Success")
        self._notify_channel(SUCCESS, message, title, sticky, target)

    def notify_danger(
        self, message="Default message", title=None, sticky=False, target=None
    ):
        title = title or _("Danger")
        self._notify_channel(DANGER, message, title, sticky, target)

    def notify_warning(
        self, message="Default message", title=None, sticky=False, target=None
    ):
        title = title or _("Warning")
        self._notify_channel(WARNING, message, title, sticky, target)

    def notify_info(
        self, message="Default message", title=None, sticky=False, target=None
    ):
        title = title or _("Information")
        self._notify_channel(INFO, message, title, sticky, target)

    def notify_default(
        self, message="Default message", title=None, sticky=False, target=None
    ):
        title = title or _("Default")
        self._notify_channel(DEFAULT, message, title, sticky, target)

    def notify_browser(
        self, title=None, message="Default message", icon=None, sticky=False, target=None
    ):
        title = title or _("Browser")
        self._notify_channel('browser', message, title, sticky, target)

    # def notify_browser(self, title, message, icon='', require_interaction=False):
    #     self.env['bus.bus'].sendone('polimex', {
    #         'm_type': 'browser',
    #         'title': title,
    #         'message': message,
    #         'icon': icon,
    #         'requireInteraction': require_interaction,
    #         'uids': self.mapped('id'),
    #     })

class UserNotifyWizard(models.TransientModel):
    _name = 'users.notify.wiz'
    _description = 'Web Users notification Wizard'

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
            exceptions.UserError(_('No user to send message'))
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



