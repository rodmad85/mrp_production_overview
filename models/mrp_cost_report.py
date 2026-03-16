from odoo import models, fields, tools


class MrpRealCostReport(models.Model):

    _name = "mrp.real.cost.report"
    _description = "Relatório de Custos de Produção"
    _auto = False
    _order = "production_path, cost_type"

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

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "mrp_real_cost_report")

        self.env.cr.execute("""

        CREATE VIEW mrp_real_cost_report AS (

        WITH RECURSIVE production_tree AS (

            SELECT
                mp.id,
                mp.parent_production_id,
                mp.product_id,
                mp.id as root_production_id,
                1 as level,
                LPAD(mp.id::text, 10, '0') as path
            FROM mrp_production mp
            WHERE mp.parent_production_id IS NULL
        
            UNION ALL
        
            SELECT
                child.id,
                child.parent_production_id,
                child.product_id,
                pt.root_production_id,
                pt.level + 1,
                pt.path || '.' || LPAD(child.id::text, 10, '0')
            FROM mrp_production child
            JOIN production_tree pt
                ON pt.id = child.parent_production_id
        )

        /* ========================= */
        /* COMPONENTES               */
        /* ========================= */

        SELECT

            sm.id as id,

            ptree.id as production_id,
            ptree.parent_production_id,
            ptree.product_id,

            ptree.level,
            ptree.path as production_path,

            'component' as cost_type,

            COALESCE(pt.name->>'pt_BR', pt.name->>'en_US') as item_name,

            sm.quantity_done as quantity,

            ROUND((COALESCE(ip.value_float,0) * sm.quantity_done)::numeric,2) as planned_cost,

            ROUND(COALESCE(svl.value,0)::numeric,2) as real_cost,

            ROUND(
                ROUND(COALESCE(svl.value,0)::numeric,2) -
                ROUND((COALESCE(ip.value_float,0) * sm.quantity_done)::numeric,2)
            ,2) as variance_cost,

            mp.date_finished

        FROM stock_move sm
        
        JOIN production_tree ptree
            ON ptree.id = sm.raw_material_production_id
        
        JOIN mrp_production mp
            ON mp.id = ptree.id
        
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
        
        /* REMOVE APENAS COMPONENTES QUE VIRARAM OP FILHA */
        
        AND NOT EXISTS (
            SELECT 1
            FROM mrp_production child
            WHERE child.parent_production_id = mp.id
            AND child.product_id = sm.product_id
        )

        UNION ALL


        /* ========================= */
        /* MÃO DE OBRA               */
        /* ========================= */

        SELECT

            wo.id + 100000000 as id,

            ptree.id as production_id,
            ptree.parent_production_id,
            ptree.product_id,

            ptree.level,
            ptree.path as production_path,

            'labor' as cost_type,

            wc.name as item_name,

            wo.duration / 60.0 as quantity,

            ROUND(((wo.duration_expected / 60.0) * wc.costs_hour)::numeric,2) as planned_cost,

            ROUND(((wo.duration / 60.0) * wc.costs_hour)::numeric,2) as real_cost,

            ROUND(
                ROUND(((wo.duration / 60.0) * wc.costs_hour)::numeric,2) -
                ROUND(((wo.duration_expected / 60.0) * wc.costs_hour)::numeric,2)
            ,2) as variance_cost,

            mp.date_finished

        FROM mrp_workorder wo

        JOIN production_tree ptree
            ON ptree.id = wo.production_id

        JOIN mrp_production mp
            ON mp.id = ptree.id

        JOIN mrp_workcenter wc
            ON wc.id = wo.workcenter_id

        WHERE wo.state='done'

        )

        """)