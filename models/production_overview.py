# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import float_round


class MrpProductionOverview(models.TransientModel):
    _name = 'mrp.production.overview'
    _description = 'Visão Geral de Consumo - Ordens de Produção'

    date_from = fields.Date(string='Data Início', default=fields.Date.context_today)
    date_to = fields.Date(string='Data Fim', default=fields.Date.context_today)
    product_ids = fields.Many2many('product.product', string='Produtos Finais')
    state_filter = fields.Selection([
        ('all', 'Todos'), ('confirmed', 'Confirmadas'),
        ('progress', 'Em Progresso'), ('to_close', 'A Encerrar'), ('done', 'Concluídas'),
    ], string='Status', default='all')

    # ── helpers de custo ────────────────────────────────────────────────────

    def _get_product_cost(self, product):
        """Retorna custo unitário do produto na moeda da empresa."""
        return product.standard_price or 0.0

    def _format_currency(self, amount):
        """Arredonda para exibição."""
        return float_round(amount, precision_digits=2)

    # ── helpers de workcenter (ordens de serviço) ───────────────────────────

    def _get_workorder_data(self, prod):
        """
        Retorna lista de ordens de serviço (mrp.workorder) da OP,
        com tempo previsto, realizado e custo de mão de obra.
        """
        workorders = []
        total_planned_hours = 0.0
        total_real_hours = 0.0
        total_wo_cost = 0.0

        for wo in prod.workorder_ids:
            planned_h = float_round((wo.duration_expected or 0.0) / 60.0, precision_digits=2)
            real_h = float_round((wo.duration or 0.0) / 60.0, precision_digits=2)

            # Custo por hora do centro de trabalho
            cost_per_hour = wo.workcenter_id.costs_hour if wo.workcenter_id else 0.0
            wo_cost = self._format_currency(real_h * cost_per_hour)

            total_planned_hours += planned_h
            total_real_hours += real_h
            total_wo_cost += wo_cost

            deviation_h = real_h - planned_h
            deviation_h_pct = 0.0
            if planned_h > 0:
                deviation_h_pct = float_round((deviation_h / planned_h) * 100, precision_digits=1)

            workorders.append({
                'id': wo.id,
                'name': wo.name,
                'workcenter': wo.workcenter_id.name if wo.workcenter_id else '—',
                'state': wo.state,
                'planned_hours': planned_h,
                'real_hours': real_h,
                'deviation_hours': float_round(deviation_h, precision_digits=2),
                'deviation_pct': deviation_h_pct,
                'cost_per_hour': cost_per_hour,
                'total_cost': wo_cost,
            })

        return {
            'workorders': workorders,
            'total_planned_hours': float_round(total_planned_hours, precision_digits=2),
            'total_real_hours': float_round(total_real_hours, precision_digits=2),
            'total_cost': self._format_currency(total_wo_cost),
        }

    # ── helpers de componentes ───────────────────────────────────────────────

    def _build_component_data(self, prod, chart_products, components_set, include_children=False):
        """
        Retorna (components_list, order_planned, order_done, order_cost_planned, order_cost_done).
        Se include_children=True, expande filhas recursivamente.
        """
        components_data = []
        order_planned = 0.0
        order_done = 0.0
        order_cost_planned = 0.0
        order_cost_done = 0.0

        child_map = {}
        if include_children:
            for child in prod.child_production_ids:
                child_map[child.product_id.id] = child

        for move in prod.move_raw_ids:
            product = move.product_id
            planned_qty = move.product_uom_qty
            done_qty = move.quantity_done
            unit_cost = self._get_product_cost(product)

            # Componente tem OP filha → expande recursivamente
            if include_children and product.id in child_map:
                child = child_map[product.id]
                child_comps, cp, cd, ccp, ccd = self._build_component_data(
                    child, chart_products, components_set, include_children=True
                )
                order_planned += cp
                order_done += cd
                order_cost_planned += ccp
                order_cost_done += ccd
                for c in child_comps:
                    c['from_child'] = child.name
                    c['child_production_id'] = child.id
                components_data.extend(child_comps)
                continue

            components_set.add(product.id)
            cost_planned = self._format_currency(planned_qty * unit_cost)
            cost_done = self._format_currency(done_qty * unit_cost)

            deviation = 0.0
            deviation_pct = 0.0
            if planned_qty > 0:
                deviation = done_qty - planned_qty
                deviation_pct = float_round((deviation / planned_qty) * 100, precision_digits=2)

            cost_deviation = self._format_currency(cost_done - cost_planned)

            order_planned += planned_qty
            order_done += done_qty
            order_cost_planned += cost_planned
            order_cost_done += cost_done

            key = product.id
            if key not in chart_products:
                chart_products[key] = {
                    'name': product.display_name,
                    'ref': product.default_code or '',
                    'uom': move.product_uom.name,
                    'planned': 0.0,
                    'done': 0.0,
                    'cost_planned': 0.0,
                    'cost_done': 0.0,
                }
            chart_products[key]['planned'] += planned_qty
            chart_products[key]['done'] += done_qty
            chart_products[key]['cost_planned'] += cost_planned
            chart_products[key]['cost_done'] += cost_done

            components_data.append({
                'product_id': product.id,
                'product_name': product.display_name,
                'product_ref': product.default_code or '',
                'uom': move.product_uom.name,
                'unit_cost': unit_cost,
                'planned_qty': float_round(planned_qty, precision_digits=3),
                'done_qty': float_round(done_qty, precision_digits=3),
                'deviation': float_round(deviation, precision_digits=3),
                'deviation_pct': deviation_pct,
                'cost_planned': cost_planned,
                'cost_done': cost_done,
                'cost_deviation': cost_deviation,
                'state': move.state,
                'from_child': None,
                'child_production_id': None,
            })

        return components_data, order_planned, order_done, order_cost_planned, order_cost_done

    def _build_order_data(self, prod, chart_products, components_set):
        components_data, order_planned, order_done, cost_planned, cost_done = \
            self._build_component_data(prod, chart_products, components_set, include_children=True)

        order_efficiency = 0.0
        order_deviation_pct = 0.0
        if order_planned > 0:
            order_efficiency = float_round((order_done / order_planned) * 100, precision_digits=1)
            order_deviation_pct = float_round(
                ((order_done - order_planned) / order_planned) * 100, precision_digits=1
            )

        wo_data = self._get_workorder_data(prod)

        # Custo total = componentes + mão de obra
        total_cost = self._format_currency(cost_done + wo_data['total_cost'])

        children_info = [{
            'id': c.id, 'name': c.name,
            'product_name': c.product_id.display_name,
            'state': c.state,
            'qty_production': c.product_qty,
            'qty_produced': c.qty_produced,
        } for c in prod.child_production_ids]

        return {
            'id': prod.id,
            'name': prod.name,
            'product_name': prod.product_id.display_name,
            'product_ref': prod.product_id.default_code or '',
            'qty_production': prod.product_qty,
            'qty_produced': prod.qty_produced,
            'uom': prod.product_uom_id.name,
            'state': prod.state,
            'state_label': dict(prod._fields['state'].selection).get(prod.state, prod.state),
            'date_planned': prod.date_planned_start.strftime('%d/%m/%Y') if prod.date_planned_start else '',
            'date_finished': prod.date_finished.strftime('%d/%m/%Y') if prod.date_finished else '',
            'planned_components_qty': float_round(order_planned, precision_digits=3),
            'done_components_qty': float_round(order_done, precision_digits=3),
            'efficiency': order_efficiency,
            'deviation_pct': order_deviation_pct,
            'has_deviation': abs(order_deviation_pct) > 5,
            'has_children': bool(prod.child_production_ids),
            'children_info': children_info,
            'components': components_data,
            # custos
            'cost_planned': self._format_currency(cost_planned),
            'cost_done': self._format_currency(cost_done),
            'cost_deviation': self._format_currency(cost_done - cost_planned),
            'total_cost': total_cost,
            # ordens de serviço
            'workorders': wo_data['workorders'],
            'wo_planned_hours': wo_data['total_planned_hours'],
            'wo_real_hours': wo_data['total_real_hours'],
            'wo_cost': wo_data['total_cost'],
        }

    # ── RPC principal ────────────────────────────────────────────────────────

    @api.model
    def get_overview_data(self, domain=None):
        if domain is None:
            domain = []

        valid_states = ['confirmed', 'progress', 'to_close', 'done']
        base_domain = [
            ('state', 'in', valid_states),
            ('parent_production_id', '=', False),
        ] + domain

        productions = self.env['mrp.production'].search(
            base_domain, order='date_planned_start desc'
        )

        orders_data = []
        total_planned = 0.0
        total_done = 0.0
        total_cost_planned = 0.0
        total_cost_done = 0.0
        total_wo_cost = 0.0
        components_set = set()
        orders_with_deviation = 0
        chart_products = {}

        for prod in productions:
            od = self._build_order_data(prod, chart_products, components_set)
            orders_data.append(od)
            total_planned += od['planned_components_qty']
            total_done += od['done_components_qty']
            total_cost_planned += od['cost_planned']
            total_cost_done += od['cost_done']
            total_wo_cost += od['wo_cost']
            if od['has_deviation']:
                orders_with_deviation += 1

        global_efficiency = 0.0
        if total_planned > 0:
            global_efficiency = float_round((total_done / total_planned) * 100, precision_digits=1)

        kpis = {
            'total_orders': len(productions),
            'orders_done': len(productions.filtered(lambda p: p.state == 'done')),
            'orders_in_progress': len(productions.filtered(lambda p: p.state == 'progress')),
            'total_components': len(components_set),
            'total_planned': float_round(total_planned, precision_digits=3),
            'total_done': float_round(total_done, precision_digits=3),
            'global_efficiency': global_efficiency,
            'orders_with_deviation': orders_with_deviation,
            'total_cost_planned': self._format_currency(total_cost_planned),
            'total_cost_done': self._format_currency(total_cost_done),
            'total_cost_deviation': self._format_currency(total_cost_done - total_cost_planned),
            'total_wo_cost': self._format_currency(total_wo_cost),
            'grand_total_cost': self._format_currency(total_cost_done + total_wo_cost),
        }

        # Top 15 por custo realizado
        chart_list = sorted(
            chart_products.values(), key=lambda x: x['cost_done'], reverse=True
        )[:15]

        chart_data = {
            'labels': [c['name'] for c in chart_list],
            'refs': [c['ref'] for c in chart_list],
            'planned': [c['planned'] for c in chart_list],
            'done': [c['done'] for c in chart_list],
            'uoms': [c['uom'] for c in chart_list],
            'cost_planned': [c['cost_planned'] for c in chart_list],
            'cost_done': [c['cost_done'] for c in chart_list],
        }

        return {'kpis': kpis, 'orders': orders_data, 'chart_data': chart_data}



    @api.model
    def action_open_overview(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'mrp_production_overview',
            'name': 'Visão Geral - Ordens de Produção',
            'target': 'current',
        }

    def action_print_report(self):
        """
        Retorna a action do relatório para o cliente.
        Chamado pelo JS via doAction — o prt_report_attachment_preview
        intercepta e abre o visualizador integrado normalmente.
        """
        self.ensure_one()
        return self.env.ref(
            'mrp_production_overview.action_report_mrp_production_overview'
        ).report_action(self)

    # ── Relatório PDF ────────────────────────────────────────────────────────

    def _fmt_cost(self, v):
        """Formata valor monetário em BRL."""
        if not v and v != 0:
            return '—'
        return 'R$ {:,.2f}'.format(v).replace(',', 'X').replace('.', ',').replace('X', '.')

    def _fmt_num(self, v, digits=None):
        """Formata número com separador pt-BR, removendo zeros à direita."""
        if v is None:
            return '—'
        if digits is not None:
            # Decimais fixos solicitados explicitamente
            return '{:,.{d}f}'.format(v, d=digits).replace(',', 'X').replace('.', ',').replace('X', '.')
        # Auto: até 6 casas, remove zeros à direita
        formatted = '{:,.6f}'.format(v)  # ex: "1,234.560000"
        # Remove zeros à direita após o decimal
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        # Converte separadores para pt-BR
        return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')

    def _fmt_dev(self, pct):
        sign = '+' if pct >= 0 else ''
        return '{}{:.1f}%'.format(sign, pct)

    def _dev_color(self, pct):
        a = abs(pct)
        if a == 0:   return '#adb5bd'
        if a <= 5:   return '#28a745'
        if a <= 15:  return '#fd7e14'
        return '#dc3545'

    def _status_style(self, state):
        styles = {
            'done':      ('#d4edda', '#155724'),
            'progress':  ('#cce5ff', '#004085'),
            'confirmed': ('#fff3cd', '#856404'),
            'to_close':  ('#d1ecf1', '#0c5460'),
            'draft':     ('#e2e3e5', '#383d41'),
        }
        return styles.get(state, ('#e2e3e5', '#383d41'))

    def _get_report_data(self):
        """Prepara todos os dados formatados para o template QWeb.

        LÓGICA DE FILTRAGEM:
        - top_components (seção "Top 15 Componentes"): Apenas componentes do gráfico
        - orders_fmt (seção "Detalhamento das Ordens"): TODOS os componentes (sem filtro)
        """
        from datetime import datetime
        # Reutiliza a lógica existente
        domain = []
        data = self.get_overview_data(domain=[])
        kpis = data['kpis']
        chart = data['chart_data']

        # Formata KPIs
        cost_dev = kpis['total_cost_deviation']
        kpis_fmt = dict(kpis)
        kpis_fmt['total_cost_planned_fmt'] = self._fmt_cost(kpis['total_cost_planned'])
        kpis_fmt['total_cost_done_fmt'] = self._fmt_cost(kpis['total_cost_done'])
        kpis_fmt['total_cost_deviation_fmt'] = ('+' if cost_dev >= 0 else '') + self._fmt_cost(cost_dev)
        kpis_fmt['cost_dev_color'] = self._dev_color(cost_dev)
        kpis_fmt['total_wo_cost_fmt'] = self._fmt_cost(kpis['total_wo_cost'])
        kpis_fmt['grand_total_cost_fmt'] = self._fmt_cost(kpis['grand_total_cost'])
        kpis_fmt['global_efficiency'] = '{:.1f}'.format(kpis['global_efficiency'])

        # ─── FORMATA ORDENS ─────────────────────────────────
        # MANTÉM TODOS OS COMPONENTES, SEM FILTRO
        orders_fmt = []
        for o in data['orders']:
            status_bg, status_color = self._status_style(o['state'])
            dev_color = self._dev_color(o['deviation_pct'])

            # Formata componentes - SEM FILTRO, todos os componentes da ordem
            comps_fmt = []
            for c in o.get('components', []):
                comps_fmt.append(dict(c,
                                      planned_fmt=self._fmt_num(c['planned_qty']) + ' ' + c['uom'],
                                      done_fmt=self._fmt_num(c['done_qty']) + ' ' + c['uom'],
                                      deviation_fmt=self._fmt_dev(c['deviation_pct']),
                                      dev_color=self._dev_color(c['deviation_pct']),
                                      unit_cost_fmt=self._fmt_cost(c['unit_cost']),
                                      cost_planned_fmt=self._fmt_cost(c['cost_planned']),
                                      cost_done_fmt=self._fmt_cost(c['cost_done']),
                                      ))

            # Formata ordens de serviço
            wos_fmt = []
            for w in o.get('workorders', []):
                wos_fmt.append(dict(w,
                                    planned_hours_fmt='{:.2f}'.format(w['planned_hours']),
                                    real_hours_fmt='{:.2f}'.format(w['real_hours']),
                                    deviation_fmt=self._fmt_dev(w['deviation_pct']),
                                    dev_color=self._dev_color(w['deviation_pct']),
                                    cost_per_hour_fmt=self._fmt_cost(w['cost_per_hour']),
                                    total_cost_fmt=self._fmt_cost(w['total_cost']),
                                    ))

            orders_fmt.append(dict(o,
                                   planned_fmt=self._fmt_num(o['planned_components_qty']),
                                   done_fmt=self._fmt_num(o['done_components_qty']),
                                   deviation_fmt=self._fmt_dev(o['deviation_pct']),
                                   dev_color=dev_color,
                                   status_bg=status_bg,
                                   status_color=status_color,
                                   cost_done_fmt=self._fmt_cost(o['cost_done']),
                                   wo_cost_fmt=self._fmt_cost(o['wo_cost']) if o['workorders'] else '—',
                                   total_cost_fmt=self._fmt_cost(o['total_cost']),
                                   components=comps_fmt,
                                   workorders=wos_fmt,
                                   ))

        # ─── TOP 15 COMPONENTES (APENAS DO GRÁFICO) ───────
        # A seção "Top 15 Componentes" é filtrada para incluir APENAS os componentes
        # presentes no gráfico (chart.get('labels')). Isso mantém a coerência entre
        # o gráfico visual e a listagem detalhada de top componentes.
        top_comps = []
        for i, label in enumerate(chart.get('labels', [])):
            top_comps.append({
                'name': label,
                'ref': (chart.get('refs') or [''] * 15)[i],
                'uom': chart['uoms'][i],
                'planned_fmt': self._fmt_num(chart['planned'][i]),
                'done_fmt': self._fmt_num(chart['done'][i]),
                'cost_planned_fmt': self._fmt_cost(chart['cost_planned'][i]),
                'cost_done_fmt': self._fmt_cost(chart['cost_done'][i]),
            })

        # Período e filtros
        fmt_date = lambda d: d.strftime('%d/%m/%Y') if d else '—'
        periodo = '{} a {}'.format(
            fmt_date(self.date_from),
            fmt_date(self.date_to),
        )
        status_labels = {
            'all': 'Todos', 'confirmed': 'Confirmadas',
            'progress': 'Em Progresso', 'to_close': 'A Encerrar', 'done': 'Concluídas',
        }
        filtro_status = '' if self.state_filter == 'all' else status_labels.get(self.state_filter, '')

        return {
            'periodo': periodo,
            'filtro_status': filtro_status,
            'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'kpis': kpis_fmt,
            'orders': orders_fmt,
            'top_components': top_comps,
        }


