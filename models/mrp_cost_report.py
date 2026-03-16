from odoo import models, fields, tools


class MrpRealCostReport(models.Model):
    _name = "mrp.real.cost.report"
    _description = "MRP Real Production Cost"
    _auto = False

    production_id = fields.Many2one("mrp.production")
    product_id = fields.Many2one("product.product")
    cost_type = fields.Char()
    item_name = fields.Char()
    quantity = fields.Float()
    unit_cost = fields.Float()
    total_cost = fields.Float()
    date_finished = fields.Datetime()

    def init(self):

        tools.drop_view_if_exists(self.env.cr, 'mrp_real_cost_report')

        self.env.cr.execute("""

        CREATE VIEW mrp_real_cost_report AS (

        SELECT

            sm.id as id,
            mp.id as production_id,
            mp.product_id as product_id,

            'Componente' as cost_type,

            pt.name->>'pt_BR' as item_name,

            sm.quantity_done as quantity,

            COALESCE(svl.unit_cost,0) as unit_cost,

            COALESCE(svl.value,0) as total_cost,

            mp.date_finished as date_finished

        FROM stock_move sm

        JOIN mrp_production mp
            ON mp.id = sm.raw_material_production_id

        JOIN product_product pp
            ON pp.id = sm.product_id

        JOIN product_template pt
            ON pt.id = pp.product_tmpl_id

        LEFT JOIN stock_valuation_layer svl
            ON svl.stock_move_id = sm.id

        WHERE sm.state='done'

        UNION ALL

        SELECT

            wo.id + 100000000 as id,
            mp.id as production_id,
            mp.product_id as product_id,

            'Serviço' as cost_type,

            wc.name as item_name,

            wo.duration / 60.0 as quantity,

            wc.costs_hour as unit_cost,

            (wo.duration / 60.0) * wc.costs_hour as total_cost,

            mp.date_finished as date_finished

        FROM mrp_workorder wo

        JOIN mrp_production mp
            ON mp.id = wo.production_id

        JOIN mrp_workcenter wc
            ON wc.id = wo.workcenter_id

        WHERE wo.state='done'

        )

        """)