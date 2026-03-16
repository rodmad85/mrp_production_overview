from odoo import models, fields, tools


class MrpRealCostReport(models.Model):
    _name = "mrp.real.cost.report"
    _description = "Relatório de Custos de Produção"
    _auto = False
    _order = "production_id"

    production_id = fields.Many2one("mrp.production", string="Ordem")
    product_id = fields.Many2one("product.product", string="Produto", related="production_id.product_id")

    cost_type = fields.Selection([
        ("component", "Componente"),
        ("labor", "Mão de obra"),
    ])

    item_name = fields.Char("Item")

    quantity = fields.Float("Quantidade")

    planned_cost = fields.Float("Custo Planejado")

    real_cost = fields.Float("Custo Real")

    variance_cost = fields.Float("Variação")

    date_finished = fields.Datetime("Finalização")

    def init(self):

        tools.drop_view_if_exists(self.env.cr, "mrp_real_cost_report")

        self.env.cr.execute("""

        CREATE VIEW mrp_real_cost_report AS (

        /* COMPONENTES */

        SELECT

            sm.id as id,

            mp.id as production_id,

            mp.product_id,

            'component' as cost_type,

            pt.name::text as item_name,

            sm.quantity_done as quantity,

            COALESCE(ip.value_float,0) * sm.quantity_done as planned_cost,

            COALESCE(svl.value,0) as real_cost,

            COALESCE(svl.value,0) -
            (COALESCE(ip.value_float,0) * sm.quantity_done) as variance_cost,

            mp.date_finished

        FROM stock_move sm

        JOIN mrp_production mp
            ON mp.id = sm.raw_material_production_id

        JOIN product_product pp
            ON pp.id = sm.product_id

        JOIN product_template pt
            ON pt.id = pp.product_tmpl_id

        LEFT JOIN ir_property ip
            ON ip.res_id = 'product.product,' || pp.id
            AND ip.name = 'standard_price'

        LEFT JOIN stock_valuation_layer svl
            ON svl.stock_move_id = sm.id

        WHERE sm.state = 'done'


        UNION ALL


        /* MÃO DE OBRA */

        SELECT

            wo.id + 100000000 as id,

            mp.id as production_id,

            mp.product_id,

            'labor' as cost_type,

            wc.name as item_name,

            wo.duration / 60.0 as quantity,

            (wo.duration_expected / 60.0) * wc.costs_hour as planned_cost,

            (wo.duration / 60.0) * wc.costs_hour as real_cost,

            ((wo.duration / 60.0) * wc.costs_hour) -
            ((wo.duration_expected / 60.0) * wc.costs_hour) as variance_cost,

            mp.date_finished

        FROM mrp_workorder wo

        JOIN mrp_production mp
            ON mp.id = wo.production_id

        JOIN mrp_workcenter wc
            ON wc.id = wo.workcenter_id

        WHERE wo.state='done'

        )

        """)