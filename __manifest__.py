# -*- coding: utf-8 -*-
{
    'name': 'MRP Production Overview - Consumo de Materiais',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Visão geral das Ordens de Produção com consumo previsto vs realizado (MRP)',
    'description': """
Visualização completa do consumo de materiais das Ordens de Produção,
comparando o consumo previsto (Lista de Materiais) com o consumo realizado
registrado no módulo MRP do Odoo 16 Community Edition.

Funcionalidades:

- KPIs: total de ordens, componentes, eficiência de consumo
- Tabela detalhada por Ordem de Produção com expand de componentes
- Custos de componentes e ordens de serviço
- Relatório PDF para impressão
- Filtros por status, período e produto
    """,
    'author': 'Customização Odoo CE',
    'depends': ['mrp', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_production_overview.xml',
        'views/mrp_production_overview_views.xml',
        'views/mrp_production_overview_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrp_production_overview/static/src/js/mrp_overview_widget.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
