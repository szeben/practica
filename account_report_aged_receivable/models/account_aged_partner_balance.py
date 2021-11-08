# -*3- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = 'account.aged.partner'

    report_date = fields.Date(group_operator='max')
    journal_code = fields.Char(group_operator='max')
    account_name = fields.Char(group_operator='max')
    expected_pay_date = fields.Date(string='Exp. Date')

    period1 = fields.Monetary(string='1 - 15')
    #period01 = fields.Monetary(string='16 - 30')
    period2 = fields.Monetary(string='16 - 30')
    period3 = fields.Monetary(string='31 - 60')
    period4 = fields.Monetary(string='61 - 90')
    period5 = fields.Monetary(string='Más Antiguos')
    #issue_days = fields.Float(string='Días de Emisión',)
    today = fields.Date.today()

####################################################
    # QUERIES
    ####################################################

    @api.model
    def _get_query_period_table(self, options):
        ''' Compute the periods to handle in the report.
        E.g. Suppose date = '2019-01-09', the computed periods will be:

        Name                | Start         | Stop
        --------------------------------------------
        As of 2019-01-09    | 2019-01-09    |
        1 - 30              | 2018-12-10    | 2019-01-08
        31 - 60             | 2018-11-10    | 2018-12-09
        61 - 90          ()   | 2018-10-11    | 2018-11-09
        91 - 120            | 2018-09-11    | 2018-10-10
        Older               |               | 2018-09-10

        Then, return the values as an sql floating table to use it directly in queries.

        :return: A floating sql query representing the report's periods.
        '''
        
        def minus_days(date_obj, days):
            return fields.Date.to_string(date_obj - relativedelta(days=days))

        date_str = options['date']['date_to']
        date = fields.Date.from_string(date_str)
        period_values = [
            (False,                  date_str),
            (minus_days(date, 1),    minus_days(date, 15)),
            #(minus_days(date, 16),    minus_days(date, 30)),
            (minus_days(date, 31),   minus_days(date, 60)),
            (minus_days(date, 61),   minus_days(date, 90)),
            (minus_days(date, 91),   minus_days(date, 120)),
            (minus_days(date, 121),  False),
        ]

        period_table = ('(VALUES %s) AS period_table(date_start, date_stop, period_index)' %
                        ','.join("(%s, %s, %s)" for i, period in enumerate(period_values)))
        params = list(chain.from_iterable(
            (period[0] or None, period[1] or None, i)
            for i, period in enumerate(period_values)
        ))
        return self.env.cr.mogrify(period_table, params).decode(self.env.cr.connection.encoding)
    

    ####################################################
    # COLUMNS/LINES
    ####################################################
    @api.model
    def _get_column_details(self, options):
        return [
            self._header_column(),
            self._field_column('report_date' ,name='Fecha del Informe'),
            self._field_column('journal_code', name="Journal"),
            self._field_column('account_name', name="Account"),
            self._custom_column(
                name=_('Días de Emisión'),
                classes=['number'],
                formatter=self.format_value,
                getter=(lambda v: (v['today'] - v['expected_pay_date']).days),
                sortable=True,
                ),
            self._field_column('expected_pay_date', name="Fecha de exp."),
            self._field_column('period0', name=_("As of: %s") % format_date(self.env, options['date']['date_to'])),
            self._field_column('period1', sortable=True),
            #self._field_column('period01', sortable=True),
            self._field_column('period2', sortable=True),
            self._field_column('period3', sortable=True),
            self._field_column('period4', sortable=True),
            self._field_column('period5', sortable=True),
            self._custom_column(  # Avoid doing twice the sub-select in the view
                name=_('Total'),
                classes=['number'],
                formatter=self.format_value,
                getter=(lambda v: v['period0'] + v['period1']+ v['period2'] + v['period3'] + v['period4'] + v['period5']),
                sortable=True,
            ),

        ]

    def _show_line(self, report_dict, value_dict, current, options):
        # Don't display an aml report line with all zero amounts.
        all_zero = all(
            self.env.company.currency_id.is_zero(value_dict[f])
            for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5']
        )
        return super()._show_line(report_dict, value_dict, current, options) and not all_zero