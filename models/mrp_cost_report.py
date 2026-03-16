from odoo import models, fields


class MrpRealCostReport(models.Model):
    _name = "mrp.real.cost.report"
    _description = "MRP Real Cost Report"
    _auto = False
    _order = "production_id"

    production_id = fields.Many2one("mrp.production", string="Ordem Produção")
    product_id = fields.Many2one("product.product", string="Produto")

    component_id = fields.Many2one("product.product", string="Componente")

    level = fields.Integer("Nível LDM")

    bom_qty = fields.Float("Qtd Planejada")
    consumed_qty = fields.Float("Qtd Consumida")

    planned_cost = fields.Float("Custo Planejado")
    real_cost = fields.Float("Custo Real")

    variance_cost = fields.Float("Variação")

    date_finished = fields.Datetime("Data Produção")

    def init(self):

        self.env.cr.execute("""

            CREATE OR REPLACE VIEW mrp_real_cost_report AS (
                
                SELECT
                
                    sm.id as id,
                
                    mp.id as production_id,
                    mp.product_id as product_id,
                
                    sm.product_id as component_id,
                
                    1 as level,
                
                    bl.product_qty as bom_qty,
                
                    sm.quantity_done as consumed_qty,
                
                    (bl.product_qty * COALESCE(svl.unit_cost,0)) as planned_cost,
                
                    svl.value as real_cost,
                
                    (svl.value - (bl.product_qty * COALESCE(svl.unit_cost,0))) as variance_cost,
                
                    mp.date_finished as date_finished
                
                FROM stock_move sm
                
                JOIN mrp_production mp
                    ON mp.id = sm.raw_material_production_id
                
                LEFT JOIN mrp_bom_line bl
                    ON bl.product_id = sm.product_id
                    AND bl.bom_id = mp.bom_id
                
                LEFT JOIN stock_valuation_layer svl
                    ON svl.stock_move_id = sm.id
                
                WHERE sm.state = 'done'
                
                )
        """)