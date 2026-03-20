/** @odoo-module **/

// ─── CSS: paleta Odoo 16 (variáveis nativas + overrides mínimos) ─────────────
(function () {
    const STYLE_ID = 'mrp_production_overview_styles';
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
/* Layout raiz — usa bg do Odoo */
.mrp_overview_root {
    font-family: var(--font, 'Roboto', sans-serif);
    background: var(--view-background-color, #f8f8f8);
    min-height: 100vh;
    padding: 24px;
    box-sizing: border-box;
    color: var(--text-color, #212529);
}

/* Header */
.mrp_hdr {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 16px;
    background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
    padding: 16px 20px; margin-bottom: 20px;
}
.mrp_hdr_title { display: flex; align-items: center; gap: 12px; }
.mrp_hdr_title h1 { font-size: 18px; font-weight: 700; margin: 0; color: #212529; }
.mrp_hdr_title p  { font-size: 12px; color: #6c757d; margin: 0; }
.mrp_hdr_icon { font-size: 28px; }
.mrp_filters { display: flex; align-items: flex-end; gap: 10px; flex-wrap: wrap; }
.mrp_fg { display: flex; flex-direction: column; gap: 3px; }
.mrp_fg label { font-size: 11px; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: .05em; }
.mrp_input {
    border: 1px solid #ced4da; border-radius: 4px;
    padding: 5px 10px; font-size: 13px; color: #212529;
    background: #fff; outline: none; min-width: 120px;
    transition: border-color .15s, box-shadow .15s;
}
.mrp_input:focus { border-color: #714b67; box-shadow: 0 0 0 3px rgba(113,75,103,.15); }
.mrp_btn {
    padding: 6px 16px; border-radius: 4px; font-size: 13px; font-weight: 600;
    cursor: pointer; border: 1px solid transparent; transition: all .15s;
}
.mrp_btn_primary { background: #714b67; color: #fff; border-color: #714b67; }
.mrp_btn_primary:hover { background: #5d3d56; }
.mrp_btn_secondary { background: #fff; color: #6c757d; border-color: #ced4da; }
.mrp_btn_secondary:hover { background: #f8f9fa; }

.mrp_btn_print { background: #fff; color: #714b67; border-color: #714b67; }
.mrp_btn_print:hover { background: #714b67; color: #fff; }
.mrp_btn_print:disabled { opacity: .6; cursor: not-allowed; }


/* KPI grid */
.mrp_kpi_grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px; margin-bottom: 20px;
}
.mrp_kpi_card {
    background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
    padding: 16px 18px; position: relative; overflow: hidden;
}
.mrp_kpi_card::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 3px; background: #dee2e6; border-radius: 0 0 8px 8px;
}
.mrp_kpi_card.kpi_purple::after  { background: #714b67; }
.mrp_kpi_card.kpi_green::after   { background: #28a745; }
.mrp_kpi_card.kpi_blue::after    { background: #007bff; }
.mrp_kpi_card.kpi_orange::after  { background: #fd7e14; }
.mrp_kpi_card.kpi_red::after     { background: #dc3545; }
.mrp_kpi_card.kpi_teal::after    { background: #20c997; }
.kpi_icon { font-size: 20px; margin-bottom: 8px; }
.kpi_value { font-size: 24px; font-weight: 700; color: #212529; margin-bottom: 4px; line-height: 1; }
.kpi_label { font-size: 11px; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }
.kpi_sub { font-size: 11px; color: #adb5bd; }
.kpi_bar_wrap { margin-top: 8px; }
.kpi_bar_track { background: #e9ecef; border-radius: 3px; height: 5px; overflow: hidden; }
.kpi_bar_fill  { height: 100%; border-radius: 3px; background: #714b67; transition: width .6s ease; }

/* Cards de custo */
.mrp_cost_grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px; margin-bottom: 20px;
}
.mrp_cost_card {
    background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
    padding: 16px 18px; border-left: 4px solid #714b67;
}
.mrp_cost_card.cc_green  { border-left-color: #28a745; }
.mrp_cost_card.cc_blue   { border-left-color: #007bff; }
.mrp_cost_card.cc_orange { border-left-color: #fd7e14; }
.mrp_cost_card.cc_red    { border-left-color: #dc3545; }
.cost_card_label { font-size: 11px; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }
.cost_card_value { font-size: 22px; font-weight: 700; color: #212529; }
.cost_card_sub   { font-size: 11px; color: #adb5bd; margin-top: 4px; }

/* Seção genérica */
.mrp_section {
    background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
    padding: 20px; margin-bottom: 20px;
}
.mrp_section_hdr {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 8px; margin-bottom: 14px;
    padding-bottom: 10px; border-bottom: 1px solid #f0f0f0;
}
.mrp_section_hdr h2 { font-size: 14px; font-weight: 700; color: #212529; margin: 0; }

/* Top componentes — lista */
.top_comp_list { list-style: none; margin: 0; padding: 0; }
.top_comp_item {
    display: grid;
    grid-template-columns: 24px 1fr auto auto auto;
    align-items: center; gap: 10px;
    padding: 8px 10px; border-radius: 6px;
    transition: background .12s;
}
.top_comp_item:hover { background: #f8f9fa; }
.top_comp_rank { font-size: 11px; font-weight: 700; color: #adb5bd; text-align: center; }
.top_comp_rank.rank_gold   { color: #f4a636; }
.top_comp_rank.rank_silver { color: #9aa0a6; }
.top_comp_rank.rank_bronze { color: #c07850; }
.top_comp_name { font-size: 13px; color: #212529; font-weight: 500; }
.top_comp_ref  { font-size: 11px; color: #adb5bd; }
.top_comp_bar_wrap { width: 100px; }
.top_comp_bar_track { background: #e9ecef; border-radius: 3px; height: 6px; overflow: hidden; }
.top_comp_bar_planned { height: 100%; border-radius: 3px; background: #007bff; opacity:.5; }
.top_comp_bar_done    { height: 3px; border-radius: 3px; background: #28a745; margin-top: 1px; }
.top_comp_qty  { font-size: 12px; color: #495057; text-align: right; white-space: nowrap; min-width: 90px; }
.top_comp_cost { font-size: 12px; font-weight: 700; color: #212529; text-align: right; white-space: nowrap; min-width: 100px; }
.top_comp_sep { border: none; border-top: 1px solid #f0f0f0; margin: 2px 0; }

/* Tabela principal */
.mrp_table_wrap { overflow-x: auto; }
.mrp_table { width: 100%; border-collapse: collapse; font-size: 13px; }
.mrp_table thead th {
    background: #f8f9fa; color: #6c757d;
    font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
    padding: 9px 12px; text-align: left;
    border-bottom: 2px solid #dee2e6; white-space: nowrap;
}
.col_num { text-align: right !important; }
.col_exp { width: 30px; }
.mrp_table tbody tr { border-bottom: 1px solid #f0f0f0; transition: background .12s; }
.mrp_table tbody tr:hover { background: #f8f9fa; }
.mrp_table tbody tr.has_children_row { background: #fafafa; }
.mrp_table td { padding: 10px 12px; color: #212529; vertical-align: middle; }
.td_mono { font-family: 'Roboto Mono', monospace; font-size: 12px; }
.td_num  { text-align: right; font-size: 12px; }
.td_cost { text-align: right; font-size: 12px; font-weight: 600; color: #495057; }

/* Expand button */
.expand_btn {
    width: 20px; height: 20px; border-radius: 3px;
    background: #f8f9fa; border: 1px solid #ced4da;
    color: #6c757d; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; transition: all .15s; user-select: none;
}
.expand_btn:hover    { background: #714b67; color: #fff; border-color: #714b67; }
.expand_btn.expanded { background: #714b67; color: #fff; border-color: #714b67; }

/* Badges de status (padrão Odoo) */
.o_badge {
    display: inline-flex; align-items: center;
    padding: 2px 8px; border-radius: 12px;
    font-size: 11px; font-weight: 600;
}
.badge_done      { background: #d4edda; color: #155724; }
.badge_progress  { background: #cce5ff; color: #004085; }
.badge_confirmed { background: #fff3cd; color: #856404; }
.badge_to_close  { background: #d1ecf1; color: #0c5460; }
.badge_draft     { background: #e2e3e5; color: #383d41; }
.badge_children  { background: #e8d5e8; color: #714b67; font-size: 11px; }

/* Desvio */
.dev_ok   { color: #28a745; font-weight: 600; font-size: 12px; }
.dev_warn { color: #fd7e14; font-weight: 600; font-size: 12px; }
.dev_crit { color: #dc3545; font-weight: 600; font-size: 12px; }
.dev_zero { color: #adb5bd; font-size: 12px; }

/* Barra de eficiência */
.eff_wrap { display: flex; align-items: center; gap: 6px; justify-content: flex-end; }
.eff_bar_track { width: 50px; height: 4px; background: #e9ecef; border-radius: 2px; overflow: hidden; }
.eff_bar_fill  { height: 100%; border-radius: 2px; transition: width .4s; }
.eff_good { background: #28a745; }
.eff_warn { background: #fd7e14; }
.eff_over { background: #dc3545; }
.eff_lbl { font-size: 11px; color: #6c757d; min-width: 38px; text-align: right; }

/* Subrow de componentes */
.comp_subrow td { background: #f8f9fa !important; padding: 0 !important; border-bottom: 2px solid #714b67 !important; }
.comp_inner { padding: 12px 12px 12px 44px; overflow: hidden; max-height: 0; transition: max-height .3s ease; }
.comp_inner.visible { max-height: 9999px; }

/* Tabs dentro do subrow */
.comp_tabs { display: flex; gap: 4px; margin-bottom: 12px; }
.comp_tab {
    padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600;
    cursor: pointer; border: 1px solid #ced4da; background: #fff; color: #6c757d;
    transition: all .12s;
}
.comp_tab.active { background: #714b67; color: #fff; border-color: #714b67; }

/* Tabela de componentes */
.comp_table { width: 100%; border-collapse: collapse; font-size: 12px; }
.comp_table th {
    color: #6c757d; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .05em;
    padding: 5px 8px; text-align: left;
    border-bottom: 1px solid #dee2e6;
}
.comp_table td { padding: 6px 8px; color: #495057; border-bottom: 1px solid #f0f0f0; }
.comp_table .ta_r { text-align: right; }
.comp_origin_badge {
    display: inline-flex; align-items: center;
    background: #e8d5e8; color: #714b67;
    padding: 1px 6px; border-radius: 10px;
    font-size: 10px; font-weight: 600;
}
.comp_parent_badge {
    display: inline-flex; align-items: center;
    background: #e9ecef; color: #6c757d;
    padding: 1px 6px; border-radius: 10px;
    font-size: 10px;
}

/* Tabela de ordens de serviço */
.wo_table { width: 100%; border-collapse: collapse; font-size: 12px; }
.wo_table th {
    color: #6c757d; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .05em;
    padding: 5px 8px; text-align: left;
    border-bottom: 1px solid #dee2e6;
}
.wo_table td { padding: 6px 8px; color: #495057; border-bottom: 1px solid #f0f0f0; }
.wo_table .ta_r { text-align: right; }

/* Loading / empty */
.mrp_loading { text-align: center; padding: 40px; color: #6c757d; }
.mrp_spinner {
    display: inline-block; width: 18px; height: 18px;
    border: 2px solid #dee2e6; border-top-color: #714b67;
    border-radius: 50%; animation: mrp_spin .8s linear infinite;
    vertical-align: middle; margin-right: 8px;
}
@keyframes mrp_spin { to { transform: rotate(360deg); } }
.mrp_empty { text-align: center; padding: 40px; color: #adb5bd; }
.mrp_empty .ei { font-size: 36px; margin-bottom: 8px; }
.mrp_tbl_footer { margin-top: 10px; font-size: 11px; color: #adb5bd; text-align: right; }

.comp_ref_small { font-size: 10px; color: #adb5bd; }
`;
    document.head.appendChild(style);
})();

import { registry }      from "@web/core/registry";
import { useService }    from "@web/core/utils/hooks";
import { Component, onMounted, onWillUnmount, xml } from "@odoo/owl";

// ── Utilitários ──────────────────────────────────────────────────────────────

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 2 });

function fmtNum(n) {
    if (n === undefined || n === null) return '—';
    // Remove zeros à direita mas mantém até 6 casas decimais sem abreviar
    const s = parseFloat(n.toFixed(6));
    return s.toLocaleString('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 6,
    });
}
// Para totalizações de KPIs (pode abreviar em M/k)
function fmtNumShort(n) {
    if (n === undefined || n === null) return '—';
    if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(2).replace('.', ',') + 'M';
    if (Math.abs(n) >= 1000) return n.toLocaleString('pt-BR', { maximumFractionDigits: 3 });
    return parseFloat(n.toFixed(6)).toLocaleString('pt-BR', { maximumFractionDigits: 6 });
}
function fmtCost(n) {
    if (n === undefined || n === null) return '—';
    return BRL.format(n);
}
function getToday()      { return new Date().toISOString().split('T')[0]; }
function getMonthStart() { const d = new Date(); return new Date(d.getFullYear(), d.getMonth(), 1).toISOString().split('T')[0]; }

function devClass(pct) {
    const a = Math.abs(pct);
    if (a === 0) return 'dev_zero';
    if (a <= 5)  return 'dev_ok';
    if (a <= 15) return 'dev_warn';
    return 'dev_crit';
}
function stateClass(s) {
    return { done:'badge_done', progress:'badge_progress', confirmed:'badge_confirmed',
             to_close:'badge_to_close', draft:'badge_draft' }[s] || 'badge_draft';
}
function stateLabel(s) {
    return { done:'Concluída', progress:'Em Progresso', confirmed:'Confirmada',
             to_close:'A Encerrar', draft:'Rascunho' }[s] || s;
}
function effClass(p) {
    if (p >= 95 && p <= 105) return 'eff_good';
    if (p > 105) return 'eff_over';
    return 'eff_warn';
}

// ── Componente ───────────────────────────────────────────────────────────────

export class MrpProductionOverview extends Component {

    static template = xml`
    <div class="mrp_overview_root">

        <!-- Header / Filtros -->
        <div class="mrp_hdr">
            <div class="mrp_hdr_title">
                <span class="mrp_hdr_icon">⚙️</span>
                <div>
                    <h1>Visão Geral — Ordens de Produção</h1>
                    <p>Consumo previsto vs realizado · Custos · Ordens de Serviço</p>
                </div>
            </div>
            <div class="mrp_filters">
                <div class="mrp_fg"><label>De</label><input type="date" id="fDateFrom" class="mrp_input"/></div>
                <div class="mrp_fg"><label>Até</label><input type="date" id="fDateTo"   class="mrp_input"/></div>
                <div class="mrp_fg">
                    <label>Status</label>
                    <select id="fState" class="mrp_input">
                        <option value="all">Todos</option>
                        <option value="confirmed">Confirmadas</option>
                        <option value="progress">Em Progresso</option>
                        <option value="to_close">A Encerrar</option>
                        <option value="done">Concluídas</option>
                    </select>
                </div>
                <button id="btnApply"   class="mrp_btn mrp_btn_primary">Aplicar</button>
                <button id="btnRefresh" class="mrp_btn mrp_btn_secondary">↺</button>
                <button id="btnPrint" class="mrp_btn mrp_btn_print" title="Gerar relatório PDF">🖨 Imprimir</button>
            </div>
        </div>

        <!-- KPIs operacionais -->
        <div class="mrp_kpi_grid">
            <div class="mrp_kpi_card kpi_purple">
                <div class="kpi_icon">📋</div>
                <div class="kpi_value" id="kpiOrders">—</div>
                <div class="kpi_label">Ordens de Produção</div>
                <div class="kpi_sub"  id="kpiOrdersSub"></div>
            </div>
            <div class="mrp_kpi_card kpi_blue">
                <div class="kpi_icon">🔩</div>
                <div class="kpi_value" id="kpiComps">—</div>
                <div class="kpi_label">Componentes únicos</div>
                <div class="kpi_sub"  id="kpiCompsSub"></div>
            </div>
            <div class="mrp_kpi_card kpi_green">
                <div class="kpi_icon">📊</div>
                <div class="kpi_value" id="kpiEff">—</div>
                <div class="kpi_label">Eficiência global</div>
                <div class="kpi_bar_wrap">
                    <div class="kpi_bar_track"><div class="kpi_bar_fill" id="kpiEffBar" style="width:0%"></div></div>
                </div>
            </div>
            <div class="mrp_kpi_card kpi_orange">
                <div class="kpi_icon">⚠️</div>
                <div class="kpi_value" id="kpiDev">—</div>
                <div class="kpi_label">Ordens com desvio &gt;5%</div>
                <div class="kpi_sub"  id="kpiDevSub"></div>
            </div>
        </div>

        <!-- KPIs de custo -->
        <div class="mrp_cost_grid">
            <div class="mrp_cost_card">
                <div class="cost_card_label">Custo Previsto (componentes)</div>
                <div class="cost_card_value" id="costPlanned">—</div>
                <div class="cost_card_sub">Baseado no custo padrão</div>
            </div>
            <div class="mrp_cost_card cc_green">
                <div class="cost_card_label">Custo Realizado (componentes)</div>
                <div class="cost_card_value" id="costDone">—</div>
                <div class="cost_card_sub" id="costDoneSub"></div>
            </div>
            <div class="mrp_cost_card cc_blue">
                <div class="cost_card_label">Custo Mão de Obra (OS)</div>
                <div class="cost_card_value" id="costWO">—</div>
                <div class="cost_card_sub">Tempo real × custo/hora</div>
            </div>
            <div class="mrp_cost_card cc_orange">
                <div class="cost_card_label">Custo Total de Produção</div>
                <div class="cost_card_value" id="costTotal">—</div>
                <div class="cost_card_sub">Componentes + Mão de obra</div>
            </div>
        </div>

        <!-- Tabela de Ordens -->
        <div class="mrp_section">
            <div class="mrp_section_hdr">
                <h2>Detalhamento de Consumo por Ordem de Produção</h2>
                <input type="text" id="tblSearch" class="mrp_input" style="min-width:220px"
                       placeholder="🔍 Buscar ordem, produto..."/>
            </div>
            <div class="mrp_table_wrap">
                <table class="mrp_table">
                    <thead>
                        <tr>
                            <th class="col_exp"></th>
                            <th>Ordem</th>
                            <th>Produto</th>
                            <th>Qtd.</th>
                            <th>Status</th>
                            <th>Data Plan.</th>
                            <th class="col_num">Prev. (un.)</th>
                            <th class="col_num">Real. (un.)</th>
                            <th class="col_num">Desvio %</th>
                            <th class="col_num">Custo Prev.</th>
                            <th class="col_num">Custo Real.</th>
                            <th class="col_num">Custo OS</th>
                            <th class="col_num">Total</th>
                        </tr>
                    </thead>
                    <tbody id="tblBody">
                        <tr><td colspan="13" class="mrp_loading">
                            <span class="mrp_spinner"></span>Carregando...
                        </td></tr>
                    </tbody>
                </table>
            </div>
            <div class="mrp_tbl_footer" id="tblFooter"></div>
        </div>

        <!-- Top 15 Componentes (lista) -->
        <div class="mrp_section">
            <div class="mrp_section_hdr">
                <h2>Top 15 Componentes por Custo Realizado</h2>
                <span style="font-size:11px;color:#adb5bd">Ordenado por custo realizado (componentes diretos)</span>
            </div>
            <ul class="top_comp_list" id="topCompList">
                <li style="color:#adb5bd;font-size:13px;padding:12px">Carregando...</li>
            </ul>
        </div>

    </div>`;

    setup() {
        this.rpc          = useService('rpc');
        this.notification = useService('notification');
        this.actionService = useService('action');
        this.orders       = [];
        this.chartData    = null;
        this.searchTerm   = '';
        this.expandedOrders = new Set();
        this.activeTab    = {};   // orderId → 'components' | 'workorders'
        this.dateFrom     = getMonthStart();
        this.dateTo       = getToday();
        this.stateFilter  = 'all';
        onMounted(() => this._init());
        onWillUnmount(() => {});
    }

    async _init() {
        this._bindFilters();
        await this._load();
    }

    _bindFilters() {
        const g = (id) => document.getElementById(id);
        const from = g('fDateFrom'); if (from) { from.value = this.dateFrom; from.addEventListener('change', e => this.dateFrom = e.target.value); }
        const to   = g('fDateTo');   if (to)   { to.value   = this.dateTo;   to.addEventListener('change',   e => this.dateTo   = e.target.value); }
        const st   = g('fState');    if (st)   { st.addEventListener('change',   e => this.stateFilter = e.target.value); }
        const ba   = g('btnApply');  if (ba)   { ba.addEventListener('click',    () => this._load()); }
        const br   = g('btnRefresh');if (br)   { br.addEventListener('click',    () => this._load()); }
        const sr   = g('tblSearch'); if (sr)   { sr.addEventListener('input',    e => { this.searchTerm = e.target.value.toLowerCase(); this._renderTable(); }); }
        const bp   = g('btnPrint');  if (bp)   { bp.addEventListener('click',    () => this._printReport()); }
    }

    async _load() {
        this._setLoading();
        try {
            const domain = [];
            if (this.dateFrom) domain.push(['date_planned_start', '>=', this.dateFrom + ' 00:00:00']);
            if (this.dateTo)   domain.push(['date_planned_start', '<=', this.dateTo   + ' 23:59:59']);
            if (this.stateFilter && this.stateFilter !== 'all') domain.push(['state', '=', this.stateFilter]);

            const res = await this.rpc('/web/dataset/call_kw', {
                model: 'mrp.production.overview',
                method: 'get_overview_data',
                args: [domain], kwargs: {},
            });
            if (res) {
                this.orders    = res.orders;
                this.chartData = res.chart_data;
                this.expandedOrders = new Set();
                this.activeTab      = {};
                this._renderKPIs(res.kpis);
                this._renderTable();
                this._renderTopList(res.chart_data);
            }
        } catch (e) {
            console.error(e);
            this.notification.add('Erro ao carregar dados.', { type: 'danger' });
        }
    }

    _setLoading() {
        const b = document.getElementById('tblBody');
        if (b) b.innerHTML = `<tr><td colspan="13" class="mrp_loading"><span class="mrp_spinner"></span>Carregando...</td></tr>`;
    }

    // ── KPIs ─────────────────────────────────────────────────────────────────

    _renderKPIs(k) {
        if (!k) return;
        const s = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v ?? '—'; };
        s('kpiOrders',    k.total_orders);
        s('kpiOrdersSub', `${k.orders_done} concluídas · ${k.orders_in_progress} em andamento`);
        s('kpiComps',     k.total_components);
        s('kpiCompsSub',  `em ${k.total_orders} ordens`);
        s('kpiEff',       k.global_efficiency.toFixed(1) + '%');
        s('kpiDev',       k.orders_with_deviation);
        s('kpiDevSub',    `de ${k.total_orders} ordens`);
        const bar = document.getElementById('kpiEffBar');
        if (bar) bar.style.width = Math.min(k.global_efficiency, 100) + '%';

        s('costPlanned', fmtCost(k.total_cost_planned));
        s('costDone',    fmtCost(k.total_cost_done));
        const devCost = k.total_cost_deviation;
        s('costDoneSub', (devCost >= 0 ? '+' : '') + fmtCost(devCost) + ' vs previsto');
        s('costWO',      fmtCost(k.total_wo_cost));
        s('costTotal',   fmtCost(k.grand_total_cost));
    }

    // ── Tabela principal ──────────────────────────────────────────────────────

    _renderTable() {
        const tbody  = document.getElementById('tblBody');
        const footer = document.getElementById('tblFooter');
        if (!tbody) return;

        const orders = (this.orders || []).filter(o => {
            if (!this.searchTerm) return true;
            return o.name.toLowerCase().includes(this.searchTerm)
                || o.product_name.toLowerCase().includes(this.searchTerm)
                || (o.product_ref || '').toLowerCase().includes(this.searchTerm);
        });

        if (!orders.length) {
            tbody.innerHTML = `<tr><td colspan="13"><div class="mrp_empty"><div class="ei">📭</div><p>Nenhuma ordem encontrada.</p></div></td></tr>`;
            if (footer) footer.textContent = '';
            return;
        }

        let html = '';
        for (const o of orders) {
            const sc    = stateClass(o.state);
            const sl    = stateLabel(o.state);
            const dc    = devClass(o.deviation_pct);
            const ds    = o.deviation_pct >= 0 ? '+' : '';
            const ec    = effClass(o.efficiency);
            const exp   = this.expandedOrders.has(o.id);
            const tab   = this.activeTab[o.id] || 'components';
            const hasWO = o.workorders && o.workorders.length > 0;

            html += `
            <tr class="order_row ${o.has_children ? 'has_children_row' : ''}" data-id="${o.id}">
                <td><div class="expand_btn ${exp ? 'expanded' : ''}" data-expand="${o.id}">${exp ? '−' : '+'}</div></td>
                <td class="td_mono">${o.name}</td>
                <td>
                    <div style="font-weight:500">${o.product_name}</div>
                    ${o.product_ref ? `<div class="comp_ref_small">[${o.product_ref}]</div>` : ''}
                </td>
                <td class="td_mono" style="font-size:12px">${fmtNum(o.qty_produced)} / ${fmtNum(o.qty_production)} <span style="color:#adb5bd">${o.uom}</span></td>
                <td>
                    <span class="o_badge ${sc}">${sl}</span>
                    ${o.has_children ? `<span class="o_badge badge_children" style="margin-left:4px">⚙ ${o.children_info.length}f</span>` : ''}
                </td>
                <td class="td_mono" style="color:#6c757d;font-size:12px">${o.date_planned}</td>
                <td class="col_num td_mono">${fmtNum(o.planned_components_qty)}</td>
                <td class="col_num td_mono">${fmtNum(o.done_components_qty)}</td>
                <td class="col_num"><span class="${dc}">${ds}${o.deviation_pct.toFixed(1)}%</span></td>
                <td class="col_num td_cost">${fmtCost(o.cost_planned)}</td>
                <td class="col_num td_cost">${fmtCost(o.cost_done)}</td>
                <td class="col_num td_cost" style="color:#007bff">${hasWO ? fmtCost(o.wo_cost) : '—'}</td>
                <td class="col_num td_cost" style="color:#714b67;font-weight:700">${fmtCost(o.total_cost)}</td>
            </tr>
            <tr class="comp_subrow_tr" data-subrow="${o.id}" style="${exp ? '' : 'display:none'}">
                <td colspan="13">
                    <div class="comp_inner ${exp ? 'visible' : ''}" id="inner_${o.id}">
                        ${this._renderSubrow(o, tab)}
                    </div>
                </td>
            </tr>`;
        }

        tbody.innerHTML = html;
        if (footer) footer.textContent = `Exibindo ${orders.length} de ${this.orders.length} ordens`;

        tbody.querySelectorAll('[data-expand]').forEach(btn => {
            btn.addEventListener('click', e => { e.stopPropagation(); this._toggleExpand(parseInt(btn.dataset.expand)); });
        });
        tbody.querySelectorAll('[data-tab]').forEach(btn => {
            btn.addEventListener('click', e => {
                const oid = parseInt(btn.dataset.order);
                const tab = btn.dataset.tab;
                this.activeTab[oid] = tab;
                const inner = document.getElementById(`inner_${oid}`);
                if (inner) inner.innerHTML = this._renderSubrow(
                    this.orders.find(o => o.id === oid), tab
                );
                // re-bind tabs
                inner && inner.querySelectorAll('[data-tab]').forEach(b2 => {
                    b2.addEventListener('click', ev => {
                        const o2 = parseInt(b2.dataset.order);
                        const t2 = b2.dataset.tab;
                        this.activeTab[o2] = t2;
                        const inn = document.getElementById(`inner_${o2}`);
                        if (inn) inn.innerHTML = this._renderSubrow(this.orders.find(x => x.id === o2), t2);
                    });
                });
            });
        });
    }

    _renderSubrow(o, tab) {
        const hasWO   = o.workorders && o.workorders.length > 0;
        const tabComp = tab === 'components' || !tab;
        const tabsHtml = `
            <div class="comp_tabs">
                <button class="comp_tab ${tabComp ? 'active' : ''}" data-tab="components" data-order="${o.id}">
                    🔩 Componentes (${(o.components || []).length})
                </button>
                ${hasWO ? `<button class="comp_tab ${!tabComp ? 'active' : ''}" data-tab="workorders" data-order="${o.id}">
                    🔧 Ordens de Serviço (${o.workorders.length})
                </button>` : ''}
            </div>`;

        return tabsHtml + (tabComp
            ? this._renderComponents(o.components)
            : this._renderWorkorders(o.workorders));
    }

    _renderComponents(components) {
        if (!components || !components.length)
            return `<p style="color:#adb5bd;font-size:12px;padding:8px">Nenhum componente.</p>`;

        let html = `<table class="comp_table">
            <thead><tr>
                <th>Componente</th>
                <th>OP Origem</th>
                <th class="ta_r">Prev. (un.)</th>
                <th class="ta_r">Real. (un.)</th>
                <th class="ta_r">Desvio %</th>
                <th class="ta_r">Custo Unit.</th>
                <th class="ta_r">Custo Prev.</th>
                <th class="ta_r">Custo Real.</th>
                <th class="ta_r">Δ Custo</th>
            </tr></thead><tbody>`;

        let totCostPlanned = 0, totCostDone = 0;
        for (const c of components) {
            const dc   = devClass(c.deviation_pct);
            const ds   = c.deviation_pct >= 0 ? '+' : '';
            const orig = c.from_child
                ? `<span class="comp_origin_badge">⚙ ${c.from_child}</span>`
                : `<span class="comp_parent_badge">pai</span>`;
            const dCost = c.cost_deviation;
            const dCostColor = dCost > 0 ? '#dc3545' : dCost < 0 ? '#28a745' : '#adb5bd';
            totCostPlanned += c.cost_planned || 0;
            totCostDone    += c.cost_done    || 0;
            html += `<tr>
                <td>
                    <div style="font-weight:500;color:#212529">${c.product_name}</div>
                    ${c.product_ref ? `<div class="comp_ref_small">[${c.product_ref}]</div>` : ''}
                </td>
                <td>${orig}</td>
                <td class="ta_r">${fmtNum(c.planned_qty)} <span style="color:#adb5bd">${c.uom}</span></td>
                <td class="ta_r">${fmtNum(c.done_qty)} <span style="color:#adb5bd">${c.uom}</span></td>
                <td class="ta_r"><span class="${dc}">${ds}${c.deviation_pct.toFixed(1)}%</span></td>
                <td class="ta_r" style="color:#6c757d">${fmtCost(c.unit_cost)}</td>
                <td class="ta_r">${fmtCost(c.cost_planned)}</td>
                <td class="ta_r" style="font-weight:600">${fmtCost(c.cost_done)}</td>
                <td class="ta_r" style="color:${dCostColor};font-weight:600">${dCost >= 0 ? '+' : ''}${fmtCost(dCost)}</td>
            </tr>`;
        }

        const totDev = totCostDone - totCostPlanned;
        html += `<tr style="background:#f8f9fa;font-weight:700">
            <td colspan="6" style="color:#6c757d;font-size:11px;text-transform:uppercase;letter-spacing:.05em">Subtotal componentes</td>
            <td class="ta_r">${fmtCost(totCostPlanned)}</td>
            <td class="ta_r">${fmtCost(totCostDone)}</td>
            <td class="ta_r" style="color:${totDev > 0 ? '#dc3545' : '#28a745'}">${totDev >= 0 ? '+' : ''}${fmtCost(totDev)}</td>
        </tr>`;
        html += `</tbody></table>`;
        return html;
    }

    _renderWorkorders(workorders) {
        if (!workorders || !workorders.length)
            return `<p style="color:#adb5bd;font-size:12px;padding:8px">Nenhuma ordem de serviço.</p>`;

        let html = `<table class="wo_table">
            <thead><tr>
                <th>Operação</th>
                <th>Centro de Trabalho</th>
                <th>Status</th>
                <th class="ta_r">Hs Previstas</th>
                <th class="ta_r">Hs Reais</th>
                <th class="ta_r">Desvio Hs</th>
                <th class="ta_r">Custo/h</th>
                <th class="ta_r">Custo Total</th>
            </tr></thead><tbody>`;

        let totCost = 0, totPlanned = 0, totReal = 0;
        for (const w of workorders) {
            const dc = devClass(w.deviation_pct);
            const ds = w.deviation_pct >= 0 ? '+' : '';
            const sc = { done:'badge_done', progress:'badge_progress', pending:'badge_confirmed',
                         ready:'badge_to_close', cancel:'badge_draft' }[w.state] || 'badge_draft';
            totCost    += w.total_cost || 0;
            totPlanned += w.planned_hours || 0;
            totReal    += w.real_hours || 0;
            html += `<tr>
                <td style="font-weight:500">${w.name}</td>
                <td style="color:#6c757d">${w.workcenter}</td>
                <td><span class="o_badge ${sc}">${w.state}</span></td>
                <td class="ta_r">${w.planned_hours.toFixed(2)}h</td>
                <td class="ta_r">${w.real_hours.toFixed(2)}h</td>
                <td class="ta_r"><span class="${dc}">${ds}${w.deviation_pct.toFixed(1)}%</span></td>
                <td class="ta_r" style="color:#6c757d">${fmtCost(w.cost_per_hour)}/h</td>
                <td class="ta_r" style="font-weight:600;color:#007bff">${fmtCost(w.total_cost)}</td>
            </tr>`;
        }
        html += `<tr style="background:#f8f9fa;font-weight:700">
            <td colspan="3" style="color:#6c757d;font-size:11px;text-transform:uppercase;letter-spacing:.05em">Subtotal mão de obra</td>
            <td class="ta_r">${totPlanned.toFixed(2)}h</td>
            <td class="ta_r">${totReal.toFixed(2)}h</td>
            <td colspan="2"></td>
            <td class="ta_r" style="color:#007bff">${fmtCost(totCost)}</td>
        </tr>`;
        html += `</tbody></table>`;
        return html;
    }

    // ── Top 15 lista ─────────────────────────────────────────────────────────

    _renderTopList(data) {
        const ul = document.getElementById('topCompList');
        if (!ul || !data || !data.labels || !data.labels.length) return;

        const maxCost = Math.max(...data.cost_done, 1);
        let html = '';
        for (let i = 0; i < data.labels.length; i++) {
            const rank     = i + 1;
            const rankCls  = rank === 1 ? 'rank_gold' : rank === 2 ? 'rank_silver' : rank === 3 ? 'rank_bronze' : '';
            const planned  = data.planned[i] || 0;
            const done     = data.done[i] || 0;
            const cPlanned = data.cost_planned[i] || 0;
            const cDone    = data.cost_done[i] || 0;
            const barPct   = Math.min((cDone / maxCost) * 100, 100);
            const donePct  = planned > 0 ? Math.min((done / planned) * 100, 100) : 0;

            if (i > 0) html += `<hr class="top_comp_sep">`;
            html += `<li class="top_comp_item">
                <span class="top_comp_rank ${rankCls}">${rank}</span>
                <div>
                    <div class="top_comp_name">${data.labels[i]}</div>
                    ${data.refs && data.refs[i] ? `<div class="comp_ref_small">[${data.refs[i]}]</div>` : ''}
                </div>
                <div class="top_comp_bar_wrap">
                    <div class="top_comp_bar_track">
                        <div class="top_comp_bar_planned" style="width:${barPct}%"></div>
                    </div>
                    <div class="top_comp_bar_done" style="width:${donePct}%"></div>
                </div>
                <div class="top_comp_qty">
                    ${fmtNum(done)} / ${fmtNum(planned)}
                    <span style="color:#adb5bd"> ${data.uoms[i]}</span>
                </div>
                <div class="top_comp_cost">${fmtCost(cDone)}</div>
            </li>`;
        }
        ul.innerHTML = html;
    }

    // ── Expand ────────────────────────────────────────────────────────────────

    _toggleExpand(orderId) {
        const subrow = document.querySelector(`[data-subrow="${orderId}"]`);
        const inner  = document.getElementById(`inner_${orderId}`);
        const btn    = document.querySelector(`[data-expand="${orderId}"]`);

        if (this.expandedOrders.has(orderId)) {
            this.expandedOrders.delete(orderId);
            if (subrow) subrow.style.display = 'none';
            if (inner)  inner.classList.remove('visible');
            if (btn)    { btn.textContent = '+'; btn.classList.remove('expanded'); }
        } else {
            this.expandedOrders.add(orderId);
            if (subrow) subrow.style.display = '';
            setTimeout(() => inner && inner.classList.add('visible'), 10);
            if (btn)    { btn.textContent = '−'; btn.classList.add('expanded'); }
            // Re-bind tabs após expandir
            if (inner) {
                inner.querySelectorAll('[data-tab]').forEach(b => {
                    b.addEventListener('click', () => {
                        const oid = parseInt(b.dataset.order);
                        const tab = b.dataset.tab;
                        this.activeTab[oid] = tab;
                        const inn = document.getElementById(`inner_${oid}`);
                        if (inn) {
                            inn.innerHTML = this._renderSubrow(this.orders.find(x => x.id === oid), tab);
                            inn.querySelectorAll('[data-tab]').forEach(b2 => {
                                b2.addEventListener('click', () => {
                                    this.activeTab[parseInt(b2.dataset.order)] = b2.dataset.tab;
                                    const i2 = document.getElementById(`inner_${b2.dataset.order}`);
                                    if (i2) i2.innerHTML = this._renderSubrow(this.orders.find(x => x.id === parseInt(b2.dataset.order)), b2.dataset.tab);
                                });
                            });
                        }
                    });
                });
            }
        }
    }
    async _printReport() {
        const btn = document.getElementById('btnPrint');
        if (btn) { btn.disabled = true; btn.textContent = '⏳ Gerando...'; }

        try {
            // 1. Cria o registro transiente com os filtros atuais
            const recId = await this.rpc('/web/dataset/call_kw', {
                model:  'mrp.production.overview',
                method: 'create',
                args:   [{
                    date_from:    this.dateFrom    || false,
                    date_to:      this.dateTo      || false,
                    state_filter: this.stateFilter || 'all',
                }],
                kwargs: {},
            });

            // 2. Chama action_print_report no Python, que usa report_action()
            //    — o mesmo método que o Odoo usa nos botões de impressão nativos.
            //    Retorna um dict ir.actions.report que o actionService processa,
            //    e o prt_report_attachment_preview intercepta normalmente.
            const reportAction = await this.rpc('/web/dataset/call_kw', {
                model:  'mrp.production.overview',
                method: 'action_print_report',
                args:   [[recId]],
                kwargs: {},
            });

            if (this.actionService) {
                await this.actionService.doAction(reportAction);
            } else {
                // Fallback caso actionService nao disponivel
                window.location.href = `/report/pdf/mrp_production_overview.report_production_overview/${recId}`;
            }

        } catch (e) {
            console.error('Erro ao gerar relatório:', e);
            this.notification.add(
                e.message || 'Erro ao gerar o relatório PDF.',
                { type: 'danger' }
            );
        } finally {
            if (btn) { btn.disabled = false; btn.textContent = '🖨 Imprimir'; }
        }
    }

}

registry.category('actions').add('mrp_production_overview', MrpProductionOverview);
