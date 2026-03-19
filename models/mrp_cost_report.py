from odoo import models, fields, tools


class MrpRealCostReport(models.Model):

    _name = "mrp.real.cost.report"
    _description = "Relatório de Custos de Produção"
    _auto = False
    _order = "production_path"

    production_id = fields.Many2one("mrp.production", string="Ordem")
    parent_production_id = fields.Many2one("mrp.production", string="OP Pai")

    product_id = fields.Many2one("product.product", string="Produto")

    level = fields.Integer("Nível")
    production_path = fields.Char("Path")

    cost_type = fields.Selection([
        ("component","Componente"),
        ("labor","Mão de obra")
    ])

    item_name = fields.Char("Item")

    quantity = fields.Float("Quantidade")

    planned_cost = fields.Monetary("Custo Planejado")
    real_cost = fields.Monetary("Custo Real")
    variance_cost = fields.Monetary("Variação")

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self:self.env.company.currency_id
    )

    date_finished = fields.Datetime("Finalização")
    display_name = fields.Char("Descrição")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "mrp_real_cost_report")

        self.env.cr.execute("""

        CREATE VIEW mrp_real_cost_report AS (

        WITH RECURSIVE production_tree AS (

            SELECT
                mp.id,
                mp.parent_production_id,
                mp.product_id,
                1 as level,
                LPAD(mp.id::text, 10, '0') as path
            FROM mrp_production mp
            WHERE mp.parent_production_id IS NULL

            UNION ALL

            SELECT
                child.id,
                child.parent_production_id,
                child.product_id,
                pt.level + 1,
                pt.path || '.' || LPAD(child.id::text, 10, '0')
            FROM mrp_production child
            JOIN production_tree pt
                ON pt.id = child.parent_production_id
        ),

        /* ========================= */
        /* BASE DE CUSTOS            */
        /* ========================= */

        base_costs AS (

            /* COMPONENTES */

            SELECT
                ptree.id as production_id,
                'component' as cost_type,
                ROUND(COALESCE(svl.value,0)::numeric,2) as real_cost

            FROM stock_move sm
            JOIN production_tree ptree ON ptree.id = sm.raw_material_production_id
            LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id

            WHERE sm.state = 'done'


            UNION ALL

            /* MÃO DE OBRA */

            SELECT
                ptree.id as production_id,
                'labor' as cost_type,
                ROUND(((wo.duration / 60.0) * wc.costs_hour)::numeric,2)

            FROM mrp_workorder wo
            JOIN production_tree ptree ON ptree.id = wo.production_id
            JOIN mrp_workcenter wc ON wc.id = wo.workcenter_id

            WHERE wo.state='done'
        ),

        /* ========================= */
        /* CONSOLIDAÇÃO              */
        /* ========================= */

        aggregated_costs AS (

            SELECT
                ptree.id,
                ptree.path,
                SUM(CASE WHEN bc.cost_type='component' THEN bc.real_cost ELSE 0 END) as comp_cost,
                SUM(CASE WHEN bc.cost_type='labor' THEN bc.real_cost ELSE 0 END) as labor_cost,
                SUM(bc.real_cost) as total_cost

            FROM production_tree ptree

            LEFT JOIN base_costs bc
                ON bc.production_id = ptree.id

            GROUP BY ptree.id, ptree.path
        )

        /* ========================= */
        /* LINHA DA OP               */
        /* ========================= */

        SELECT

            mp.id + 200000000 as id,

            ptree.id as production_id,
            ptree.parent_production_id,
            ptree.product_id,

            ptree.level,
            ptree.path as production_path,

            'production' as cost_type,

            repeat('   ', ptree.level-1) || mp.name as item_name,

            0 as quantity,
            0 as planned_cost,
            0 as real_cost,
            0 as variance_cost,

            mp.date_finished

        FROM production_tree ptree
        JOIN mrp_production mp ON mp.id = ptree.id


        UNION ALL


        /* ========================= */
        /* COMPONENTES DETALHE       */
        /* ========================= */

        SELECT

            sm.id as id,

            ptree.id as production_id,
            ptree.parent_production_id,
            ptree.product_id,

            ptree.level,
            ptree.path as production_path,

            'component' as cost_type,

            repeat('   ', ptree.level) ||
            COALESCE(pt.name->>'pt_BR', pt.name->>'en_US') as item_name,

            sm.quantity_done,

            0 as planned_cost,

            ROUND(COALESCE(svl.value,0)::numeric,2),

            0 as variance_cost,

            mp.date_finished

        FROM stock_move sm
        JOIN production_tree ptree ON ptree.id = sm.raw_material_production_id
        JOIN mrp_production mp ON mp.id = ptree.id
        JOIN product_product pp ON pp.id = sm.product_id
        JOIN product_template pt ON pt.id = pp.product_tmpl_id
        LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id

        WHERE sm.state='done'

        AND NOT EXISTS (
            SELECT 1 FROM mrp_production child
            WHERE child.parent_production_id = mp.id
            AND child.product_id = sm.product_id
        )


        UNION ALL


        /* ========================= */
        /* TOTAL DA OP               */
        /* ========================= */

        SELECT

            ac.id + 300000000 as id,

            ac.id as production_id,
            NULL,
            NULL,

            ptree.level,
            ptree.path || '.999' as production_path,

            'total' as cost_type,

            repeat('   ', ptree.level) || 'TOTAL OP',

            0,

            0,

            ac.total_cost,

            0,

            NULL

        FROM aggregated_costs ac
        JOIN production_tree ptree ON ptree.id = ac.id

        )

        """)