from odoo import models, fields, tools


class MrpRealCostSummary(models.Model):

    _name="mrp.real.cost.summary"
    _description="Resumo de Custos"
    _auto=False

    production_id=fields.Many2one("mrp.production")
    product_id=fields.Many2one("product.product")

    component_cost=fields.Monetary("Componentes")
    labor_cost=fields.Monetary("Mão de Obra")

    total_real_cost=fields.Monetary("Custo Real")
    total_planned_cost=fields.Monetary("Planejado")

    total_variance=fields.Monetary("Variação")

    currency_id=fields.Many2one(
        "res.currency",
        default=lambda self:self.env.company.currency_id
    )

    def init(self):

        tools.drop_view_if_exists(self.env.cr,"mrp_real_cost_summary")

        self.env.cr.execute("""

        CREATE VIEW mrp_real_cost_summary AS (

        SELECT

            MIN(id) as id,

            production_id,
            product_id,

            SUM(CASE WHEN cost_type='component'
                THEN real_cost ELSE 0 END) as component_cost,

            SUM(CASE WHEN cost_type='labor'
                THEN real_cost ELSE 0 END) as labor_cost,

            SUM(real_cost) as total_real_cost,

            SUM(planned_cost) as total_planned_cost,

            SUM(variance_cost) as total_variance

        FROM mrp_real_cost_report

        GROUP BY production_id,product_id

        )

        """)