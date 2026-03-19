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
        ("production", "Ordem"),
        ("component", "Componente"),
        ("labor", "Mão de Obra"),
        ("total", "Total")
    ])

    item_name = fields.Char("Item")
    quantity = fields.Float("Quantidade")
    uom_id = fields.Many2one("uom.uom", string="Unidade")

    planned_cost = fields.Monetary("Custo Planejado")
    real_cost = fields.Monetary("Custo Real")
    variance_cost = fields.Monetary("Variação")

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )

    date_finished = fields.Datetime("Finalização")
    display_name = fields.Char("Descrição")
    company_id = fields.Many2one('res.company', string='Empresa')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "mrp_real_cost_report")

        self.env.cr.execute("""
        CREATE OR REPLACE VIEW mrp_real_cost_report AS (
        WITH RECURSIVE production_tree AS (
            -- Nó raiz (OPs sem pai)
            SELECT
                mp.id,
                mp.parent_production_id,
                mp.product_id,
                mp.name,
                mp.date_finished,
                1 as level,
                LPAD(mp.id::text, 10, '0') as path,
                mp.company_id
            FROM mrp_production mp
            WHERE mp.parent_production_id IS NULL

            UNION ALL

            -- Nós filhos
            SELECT
                child.id,
                child.parent_production_id,
                child.product_id,
                child.name,
                child.date_finished,
                pt.level + 1,
                pt.path || '.' || LPAD(child.id::text, 10, '0'),
                child.company_id
            FROM mrp_production child
            JOIN production_tree pt ON pt.id = child.parent_production_id
        ),

        -- Custos dos componentes (matéria-prima)
        component_costs AS (
            SELECT
                sm.raw_material_production_id as production_id,
                sm.product_id,
                SUM(sm.quantity_done) as quantity_done,
                SUM(COALESCE(svl.value, 0)) as real_cost,
                SUM(sm.product_uom_qty * pt.standard_price) as planned_cost
            FROM stock_move sm
            JOIN product_product pp ON pp.id = sm.product_id
            JOIN product_template pt ON pt.id = pp.product_tmpl_id
            LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id
            WHERE sm.state = 'done'
              AND sm.raw_material_production_id IS NOT NULL
            GROUP BY sm.raw_material_production_id, sm.product_id
        ),

        -- Custos de mão de obra
        labor_costs AS (
            SELECT
                wo.production_id,
                SUM((wo.duration / 60.0) * wc.costs_hour) as real_cost,
                SUM((wo.duration_expected / 60.0) * wc.costs_hour) as planned_cost
            FROM mrp_workorder wo
            JOIN mrp_workcenter wc ON wc.id = wo.workcenter_id
            WHERE wo.state = 'done'
            GROUP BY wo.production_id
        ),

        -- Totais por ordem
        order_totals AS (
            SELECT
                pt.id,
                pt.path,
                pt.level,
                COALESCE(SUM(cc.real_cost), 0) + COALESCE(SUM(lc.real_cost), 0) as total_real,
                COALESCE(SUM(cc.planned_cost), 0) + COALESCE(SUM(lc.planned_cost), 0) as total_planned
            FROM production_tree pt
            LEFT JOIN component_costs cc ON cc.production_id = pt.id
            LEFT JOIN labor_costs lc ON lc.production_id = pt.id
            GROUP BY pt.id, pt.path, pt.level
        )

        -- LINHAS DAS ORDENS DE PRODUÇÃO
        SELECT
            -- ID único
            pt.id::bigint as id,

            pt.id as production_id,
            pt.parent_production_id,
            pt.product_id,

            pt.level,
            pt.path as production_path,

            'production'::varchar as cost_type,

            repeat('   ', pt.level-1) || pt.name as item_name,

            1.0 as quantity,
            NULL::int as uom_id,

            COALESCE(ot.total_planned, 0.0) as planned_cost,
            COALESCE(ot.total_real, 0.0) as real_cost,
            COALESCE(ot.total_real - ot.total_planned, 0.0) as variance_cost,

            pt.date_finished,
            pt.name as display_name,
            pt.company_id

        FROM production_tree pt
        LEFT JOIN order_totals ot ON ot.id = pt.id

        UNION ALL

        -- COMPONENTES (MATÉRIA-PRIMA)
        SELECT
            (1000000 + sm.id)::bigint as id,

            pt.id as production_id,
            pt.parent_production_id,
            pt.product_id,

            pt.level,
            pt.path || '.' || LPAD(sm.id::text, 10, '0') as production_path,

            'component'::varchar as cost_type,

            repeat('   ', pt.level) || COALESCE(pt_tmpl.name, 'Componente') as item_name,

            sm.quantity_done as quantity,
            sm.product_uom as uom_id,

            (sm.product_uom_qty * pt_tmpl.standard_price) as planned_cost,
            COALESCE(svl.value, 0.0) as real_cost,
            COALESCE(svl.value, 0.0) - (sm.product_uom_qty * pt_tmpl.standard_price) as variance_cost,

            pt.date_finished,
            COALESCE(pt_tmpl.name, 'Componente') as display_name,
            pt.company_id

        FROM stock_move sm
        JOIN production_tree pt ON pt.id = sm.raw_material_production_id
        JOIN product_product pp ON pp.id = sm.product_id
        JOIN product_template pt_tmpl ON pt_tmpl.id = pp.product_tmpl_id
        LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id
        WHERE sm.state = 'done'
          AND sm.raw_material_production_id IS NOT NULL

        UNION ALL

        -- MÃO DE OBRA
        SELECT
            (2000000 + wo.id)::bigint as id,

            pt.id as production_id,
            pt.parent_production_id,
            pt.product_id,

            pt.level,
            pt.path || '.' || LPAD(wo.id::text, 10, '0') as production_path,

            'labor'::varchar as cost_type,

            repeat('   ', pt.level) || 'Mão de Obra: ' || wo.name as item_name,

            (wo.duration / 60.0) as quantity,
            NULL::int as uom_id,

            (wo.duration_expected / 60.0) * wc.costs_hour as planned_cost,
            (wo.duration / 60.0) * wc.costs_hour as real_cost,
            ((wo.duration / 60.0) - (wo.duration_expected / 60.0)) * wc.costs_hour as variance_cost,

            pt.date_finished,
            'Mão de Obra: ' || wo.name as display_name,
            pt.company_id

        FROM mrp_workorder wo
        JOIN production_tree pt ON pt.id = wo.production_id
        JOIN mrp_workcenter wc ON wc.id = wo.workcenter_id
        WHERE wo.state = 'done'

        UNION ALL

        -- TOTAIS POR ORDEM
        SELECT
            (3000000 + pt.id)::bigint as id,

            pt.id as production_id,
            pt.parent_production_id,
            pt.product_id,

            pt.level,
            pt.path || '.999' as production_path,

            'total'::varchar as cost_type,

            repeat('   ', pt.level) || 'TOTAL DA ORDEM' as item_name,

            0.0 as quantity,
            NULL::int as uom_id,

            ot.total_planned as planned_cost,
            ot.total_real as real_cost,
            ot.total_real - ot.total_planned as variance_cost,

            pt.date_finished,
            'TOTAL DA ORDEM' as display_name,
            pt.company_id

        FROM production_tree pt
        JOIN order_totals ot ON ot.id = pt.id
        );
        """)