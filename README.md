# mrp_production_overview

## Visão Geral de Consumo — Ordens de Produção
### Odoo 16 Community Edition

---

## 📋 Descrição

Módulo que adiciona um **dashboard interativo** ao módulo MRP do Odoo 16 CE,
exibindo a comparação entre o **consumo previsto** (definido na Lista de Materiais)
e o **consumo realizado** registrado nos movimentos de matéria-prima das Ordens de Produção.

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---|---|
| **KPIs globais** | Total de ordens, componentes únicos, eficiência de consumo, ordens com desvio |
| **Gráfico de barras** | Top 15 componentes: previsto vs realizado |
| **Tabela detalhada** | Todas as ordens com status, datas, consumo e eficiência |
| **Drill-down** | Expande cada ordem para ver o detalhamento por componente |
| **Filtros** | Por período (data início/fim) e status da ordem |
| **Busca** | Pesquisa em tempo real por nome de ordem ou produto |
| **Indicadores visuais** | Badges de desvio com cores (verde ≤5%, âmbar ≤15%, vermelho >15%) |

---

## 🚀 Instalação

### 1. Copiar o módulo

```bash
# Copie a pasta para o diretório de addons do seu Odoo
cp -r mrp_production_overview /opt/odoo/addons/
# ou para o diretório de addons customizados configurado no odoo.conf
```

### 2. Atualizar a lista de módulos

```
Menu: Configurações → Ativar modo desenvolvedor
Menu: Configurações → Técnico → Atualizar lista de módulos
```

### 3. Instalar o módulo

```
Menu: Aplicativos → Pesquisar "MRP Production Overview" → Instalar
```

---

## 📌 Dependências

- `mrp` (Fabricação — nativo Odoo)
- `stock` (Estoque — nativo Odoo)

---

## 📍 Onde acessar

Após instalação, o dashboard estará disponível em:

- **Fabricação → Visão Geral de Consumo → Consumo Previsto vs Realizado**
- **Fabricação → Relatórios → Consumo de Materiais (OP)**

---

## 🔑 Permissões

| Grupo | Acesso |
|---|---|
| Usuário de Fabricação (`mrp.group_mrp_user`) | Leitura e uso do dashboard |
| Gerente de Fabricação (`mrp.group_mrp_manager`) | Acesso completo |

---

## 🧮 Lógica de Cálculo

### Consumo Previsto
Soma de `product_uom_qty` dos movimentos de matéria-prima (`move_raw_ids`)
com estado relevante (confirmed, progress, to_close, done).

### Consumo Realizado
Soma de `quantity_done` dos mesmos movimentos.

### Desvio (%)
```
desvio_pct = ((realizado - previsto) / previsto) * 100
```

### Eficiência
```
eficiência = (realizado / previsto) * 100
```

### Classificação de Desvio
| Faixa | Cor | Significado |
|---|---|---|
| ≤ 5% | 🟢 Verde | Dentro do esperado |
| 5–15% | 🟡 Âmbar | Atenção requerida |
| > 15% | 🔴 Vermelho | Desvio crítico |

---

## 🛠 Estrutura do Módulo

```
mrp_production_overview/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   └── mrp_production_overview.py   # Lógica de negócio / RPC
├── views/
│   ├── mrp_production_overview_views.xml   # Action + Template QWeb
│   └── mrp_production_overview_menus.xml   # Menus
├── security/
│   └── ir.model.access.csv
└── static/src/
    ├── css/
    │   └── mrp_overview.css             # Estilos do dashboard
    └── js/
        └── mrp_overview_widget.js       # Componente OWL + Chart.js
```

---

## ⚠️ Observações

- O módulo usa **Chart.js** carregado via CDN na primeira renderização.
  Em ambientes sem acesso à internet, faça o download de
  `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
  e inclua no bundle estático do módulo.

- O modelo `mrp.production.overview` é **TransientModel** (sem persistência).
  Todos os dados são calculados em tempo real a partir das ordens de produção.

- Compatível com **Odoo 16 CE** (Community Edition).

---

## 📄 Licença

LGPL-3
