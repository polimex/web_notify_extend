import logging

from werkzeug.urls import url_encode

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = 'base'

    # _log_access = True  # Include magic fields

    @api.model
    def internal_link(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].search([
            ('view_mode', '=', 'form'),
            ('binding_model_id', '=', self._name)
        ])
        url = '/web#%s' % url_encode({
            'action': action,
            'active_id': self.id,
            'active_model': self._name,
            'form_type': 'form',
            # 'menu_id': self.env.ref('hr.menu_hr_root').id,
        })
        return '<a href="{url}" class="o_redirect" t-att-data-oe-model="{model}" t-att-data-oe-id="{id}">#{name}</a>'.format(
            url=url,
            model=self._name,
            id=self.id,
            name=self.name
        )

    def refresh_views(self, model=None, ids=None, user=None, create=False):
        """ Informs the web client to refresh the views that belong to the 
            corresponding model by sending a message to the bus.

            There are two ways to use this method. First by calling it
            without any parameters. In this case, the views are determined
            and updated using the current records in self. Alternatively,
            the method can also be called with corresponding parameters
            to explicitly update a view from another model.

            :param model: The model of the records is used to find the
                corresponding views
            :param ids: IDs of the records are used to determine which
                records have been updated
            :param user: The user (res.users) is used to determine whether
                the current one has caused the refresh
            :param create: Indicates whether the record has been newly
                created or updated
        """
        if self.exists() or ids:
            record = next(iter(self)) if len(self) > 1 else self

            if not ids and self._log_access:
                create = record.exists() and record.create_date == record.write_date or False
            _logger.info('Sending refresh for {}'.format(model or self._name))
            self.env['bus.bus']._sendone(user and user.id or False if ids else self.env.user.id, 'polimex', {
                'm_type': 'refresh',
                'create': create,
                'model': model or self._name,
                'uid': user and user.id or False if ids else self.env.user.id,
                'ids': ids or self.mapped('id')
            })
