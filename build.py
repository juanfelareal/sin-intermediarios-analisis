import importlib.util, sys
_spec = importlib.util.spec_from_file_location("data", "datos-corte-2026-09-21.py"); _m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m); globals().update({k:v for k,v in vars(_m).items() if not k.startswith("_")})
from collections import defaultdict
import re

def cop(n): return '$' + f"{round(n):,}".replace(',', '.')
def r2(x): return f"{x:.2f}".replace('.', ',')
def pct(x, d=0): return (f"{x:.{d}f}".replace('.', ',')) + '%'
def mill(n): return '$' + f"{n/1e6:.1f}".replace('.', ',') + 'M'

def agg(rows):
    sp=sum(r[2] for r in rows); c=sum(r[11] for r in rows); val=sum(r[2]*r[10] for r in rows)
    return dict(spend=sp,compras=c,val=val,roas=val/sp if sp else 0,cpa=sp/c if c else 0, share=100*sp/TOTAL['spend'])

AVG = TOTAL['roas']
def cls(roas):
    if roas >= 6.0: return 'ok'
    if roas >= 5.0: return 'mid'
    return 'bad'

# ---------- ángulos ----------
ang=defaultdict(list); angsets=defaultdict(dict)
for k,s in ADSETS.items():
    ang[s[0]].append(('x','x',s[2],s[3],0,0,0,0,s[8],0,s[10],s[11])); angsets[s[0]][s[1]]=angsets[s[0]].get(s[1],[])+[s]
ang_rank = sorted(ang.items(), key=lambda x:-agg(x[1])['roas'])
verdict_ang = {
 'Pregunta retadora': 'Gana por retorno y por volumen. El conjunto grande es el único que no se desgastó (frecuencia 2,54, CTR 2,21%) y el iso low a $123K/día sostiene 8,98.',
 'Historia de consistencia': 'Segundo por retorno gracias al conjunto iso low: la misma creatina de Jaime rinde 9,22 allí y 5,21 en el conjunto grande (frecuencia 5,05, saturado).',
 'Validadores profesionales': 'Yeyo solo va en 6,02; Alejandra (55% del gasto del ángulo) lo arrastra a 4,65. Es un problema de reparto, no del ángulo.',
 'Rutina real': 'Último lugar: el conjunto grande rinde 4,62 con el CPM más caro de la campaña ($14.419) y dos videos flojos adentro (Rutina v1 de Natalia y Snack de Gabriela).',
}
ang_rows=''; ang_verdicts=''
for i,(a,rows) in enumerate(ang_rank,1):
    g=agg(rows); esc=angsets[a].get('escala',[]); low=angsets[a].get('low',[])
    ge=agg([('x','x',s[2],0,0,0,0,0,0,0,s[10],s[11]) for s in esc]); gl=agg([('x','x',s[2],0,0,0,0,0,0,0,s[10],s[11]) for s in low])
    ang_rows += f'''<tr><td class="ad"><span class="dot {cls(g['roas'])}"></span>{i}. {a}</td><td>{cop(g['spend'])}<small>{g['share']:.0f}% del gasto</small></td><td>{g['compras']}</td><td>{cop(g['cpa'])}</td><td>{r2(ge['roas'])}<small>{ge['compras']} compras</small></td><td>{r2(gl['roas'])}<small>{gl['compras']} compras</small></td><td class="roas">{r2(g['roas'])}</td></tr>'''
    ang_verdicts += f'<li><b>{a}.</b> {verdict_ang[a]}</li>'

# ---------- videos ----------
vid=defaultdict(list)
for a in ADS: vid[a[1]].append(a)
vagg={v:agg(rows) for v,rows in vid.items()}
vid_rank=[v for v in sorted(vagg, key=lambda v:-vagg[v]['roas']) if vagg[v]['compras']>=10]
vid_small=[v for v in vagg if vagg[v]['compras']<10]
vnote = {
 'exio_creatina': 'Casi todo en el conjunto iso low (16,08). Señal fuerte, muestra corta.',
 'sammy_creatina_costosa': 'El mejor video con muestra sólida. Vive en el conjunto iso low.',
 'luisa_rutina_v1': '10,63 en iso low, 3,25 en el conjunto grande. Probar de nuevo en iso low.',
 'natalia_rutina_v2': '11,15 en iso low, 5,96 en el conjunto grande, 0,96 en la v2. Ganador que Meta subestimó.',
 'yeyo_curiosidad': '12,64 en iso low con CPA $13.601, el más barato de la campaña.',
 'yeyo_pregunta_frecuente': 'Sube a 9,05 en iso low; en el conjunto grande cuesta $29.067 por compra.',
 'gabriela_pregunta_v2': 'Mejor costo por compra entre los ganadores ($16.416). Corrió apagada y prendida.',
 'jaime_creatina_v1': 'El caballo de batalla: 21% del gasto y 170 compras. Fatigado a escala (frecuencia 5,05).',
 'david_creatina_v3': 'Correcto, sin muestra grande. Segunda opción de David.',
 'sammy_prioridad_alimenticia': 'Mejor CTR de la campaña (2,78%). Solo ha corrido en el conjunto caro de Rutina.',
 'camila_recetas_v2': 'El único video de Camila sobre el promedio del ángulo. Está apagado.',
 'camila_montana_v1': 'Barato ($14.061/compra) pero sin escala.',
 'alejandra_proteina': '10% del gasto a ROAS 5,17 y $30.078 por compra: cara por conversión.',
 'david_pagar_mas': '15% del gasto, el más grande. Mejor CTR (2,31%) y CPC ($423) pero convierte a $27.882.',
 'yeyo_creencias': 'El único Yeyo por debajo de 5. Reemplazarlo por Curiosidad.',
 'gabriela_snack_v3': 'Apagar. La fuerza de Gabriela está en Pregunta, no en Snack.',
 'camila_triatlon_ajuste': 'Apagar. CTR 1,05% y $33.695 por compra.',
 'natalia_rutina_v1': 'Apagar. $37.070 por compra, el peor de la campaña con muestra.',
 'alejandra_creatina': 'Apagar. El ROAS más bajo con muestra sólida.',
}
vid_rows=''
vmain=[v for v in vid_rank if vagg[v]['compras']>=20]; vsig=[v for v in vid_rank if vagg[v]['compras']<20]
for i,v in enumerate(vmain+vsig,1):
    g=vagg[v]; t,c,a=VIDEOS[v]
    if v==vsig[0]: vid_rows += '<tr class="grp"><td colspan="6">Señales con muestra corta (10 a 19 compras)</td></tr>'
    num = f'{i}. ' if v in vmain else ''
    vid_rows += f'''<tr><td class="ad"><span class="dot {cls(g['roas'])}"></span>{num}{t}<small>{c} · {a}</small></td><td>{cop(g['spend'])}<small>{pct(g['share'],1)} del gasto</small></td><td>{g['compras']}</td><td>{cop(g['cpa'])}</td><td class="roas">{r2(g['roas'])}</td><td class="vn">{vnote[v]}</td></tr>'''
small_txt = '; '.join(f"{VIDEOS[v][0]} de {VIDEOS[v][1]} ({r2(vagg[v]['roas'])}, {vagg[v]['compras']} compras)" for v in sorted(vid_small, key=lambda v:-vagg[v]['roas']))

# ---------- creadores ----------
cr=defaultdict(list)
for a in ADS: cr[VIDEOS[a[1]][1]].append(a)
cagg={c:agg(rows) for c,rows in cr.items() if c!='Jaime Cobos'}
cr_rank=sorted(cagg, key=lambda c:-cagg[c]['roas'])
crole={'Sammy Cáceres':'Pregunta retadora · Rutina real','Natalia Múnera':'Pregunta retadora · Rutina real','Gabriela Schiappa':'Pregunta retadora · Rutina real','David Ruiz':'Pregunta retadora','Jaime':'Historia de consistencia','Yeyo Agudelo':'Entrenador · Validadores','Alejandra Barragán':'Nutricionista · Validadores','Camila Vélez':'Rutina real · Historia','Exio':'Historia de consistencia','Luisa Méndez':'Rutina real'}
maxroas=max(g['roas'] for g in cagg.values()); maxshare=max(g['share'] for g in cagg.values())
cr_rows=''
cmain=[c for c in cr_rank if cagg[c]['compras']>=25]; csig=[c for c in cr_rank if cagg[c]['compras']<25]
for i,c in enumerate(cmain+csig,1):
    g=cagg[c]
    if c==csig[0]: cr_rows += '<div class="sublabel" style="margin-top:18px">Señales con muestra corta</div>'
    num = f'{i}. ' if c in cmain else ''
    cr_rows += f'''<div class="rank-row">
  <div class="rank-name">{num}{c}<small>{crole[c]}</small></div>
  <div>
    <div class="bar-label"><span>ROAS ponderado</span><b>{r2(g['roas'])}</b></div>
    <div class="bar"><i class="{cls(g['roas'])}" style="width:{100*g['roas']/maxroas:.0f}%"></i></div>
    <div class="bar-label"><span>% del gasto total</span><b>{g['share']:.0f}%</b></div>
    <div class="bar spend"><i style="width:{100*g['share']/maxshare:.0f}%"></i></div>
  </div>
  <div class="rank-kpis"><b>{g['compras']} compras</b>{cop(g['cpa'])} / compra</div>
</div>'''

# ---------- escala vs low ----------
def sets(t): return agg([('x','x',s[2],0,0,0,0,0,0,0,s[10],s[11]) for s in ADSETS.values() if s[1]==t])
E=sets('escala'); L=sets('low')
cpm_e=1000*sum(s[2] for s in ADSETS.values() if s[1]=='escala')/sum(s[3] for s in ADSETS.values() if s[1]=='escala')
cpm_l=1000*sum(s[2] for s in ADSETS.values() if s[1]=='low')/sum(s[3] for s in ADSETS.values() if s[1]=='low')
# apagar
off=['alejandra_creatina','natalia_rutina_v1','camila_triatlon_ajuste','gabriela_snack_v3','yeyo_creencias']
goff=agg([a for a in ADS if a[1] in off])
win=['sammy_creatina_costosa','natalia_rutina_v2','gabriela_pregunta_v2','yeyo_curiosidad','yeyo_pregunta_frecuente']
gwin=agg([a for a in ADS if a[1] in win])
uplift = goff['spend']*(gwin['roas']-goff['roas'])
ps,pc,pr=11002725,511,5.43
inc_s=TOTAL['spend']-ps; inc_c=TOTAL['compras']-pc; inc_roas=(TOTAL['spend']*TOTAL['roas']-ps*pr)/inc_s
print(f"escala {E['roas']:.2f} cpa {E['cpa']:.0f} cpm {cpm_e:.0f} share {E['share']:.0f} | low {L['roas']:.2f} cpa {L['cpa']:.0f} cpm {cpm_l:.0f} share {L['share']:.0f} val share {100*L['val']/(E['val']+L['val']):.0f}")
print(f"off spend {goff['spend']:,} share {goff['share']:.1f} roas {goff['roas']:.2f} | win spend {gwin['spend']:,} share {gwin['share']:.1f} roas {gwin['roas']:.2f} compras {gwin['compras']} cpa {gwin['cpa']:.0f} | uplift {uplift:,.0f}")
print(f"inc roas {inc_roas:.2f} inc compras {inc_c} inc spend {inc_s:,}")


# ---------- galería de videos top ----------
import os
TOP_VIDEOS = ['sammy_creatina_costosa','natalia_rutina_v2','yeyo_curiosidad','yeyo_pregunta_frecuente','gabriela_pregunta_v2','jaime_creatina_v1']
PH_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4V8z" fill="currentColor" stroke="none"/></svg>'
vcards=''
for v in TOP_VIDEOS:
    g=vagg[v]; t,c,a=VIDEOS[v]; f=f'videos/{v}.mp4'
    if os.path.exists(f):
        media=f'<video controls playsinline preload="metadata" src="{f}"></video>'
    else:
        media=f'<div class="vph">{PH_SVG}<span>Video pendiente</span></div>'
    vcards += f'''<div class="vcard">
  <div class="vmedia">{media}<div class="vroas">{r2(g['roas'])}<small>ROAS</small></div></div>
  <div class="vinfo"><b>{t}</b><span>{c} · {a}</span><div class="piece-stats"><span>{g['compras']} compras</span><span>{cop(g['cpa'])} / compra</span></div></div>
</div>'''

# ---------- galería de creadores top ----------
TOP_CREATORS = ['Sammy Cáceres','Jaime','Yeyo Agudelo','Natalia Múnera','Gabriela Schiappa']
cslug = {'Sammy Cáceres':'sammy_caceres','Jaime':'jaime','Yeyo Agudelo':'yeyo_agudelo','Natalia Múnera':'natalia_munera','Gabriela Schiappa':'gabriela_schiappa'}
cbest = {}
for v,rows in vid.items():
    c=VIDEOS[v][1]
    if vagg[v]['compras']>=10 and (c not in cbest or vagg[v]['roas']>vagg[cbest[c]]['roas']): cbest[c]=v
cnote = {
 'Sammy Cáceres':'El mejor de la campaña con muestra sólida y el único con dos videos ganadores en dos ángulos distintos. Tiene además el mejor CTR de todos (2,78% en Prioridad alimenticia).',
 'Jaime':'El caballo de batalla: un solo video suma 170 compras y el 21% del gasto. Necesita una versión nueva de su creatina porque la v1 ya está saturada.',
 'Yeyo Agudelo':'Tres videos y dos de ellos ganadores. Como entrenador es el validador que sí convierte: su Curiosidad compra a $13.601 en el conjunto iso low.',
 'Natalia Múnera':'Su Rutina v2 es el segundo mejor video de la campaña (8,04); su Rutina v1 es el peor con muestra. Repetir el estilo de la v2.',
 'Gabriela Schiappa':'El costo por compra más bajo entre los creadores del ranking. Su fuerza está en el ángulo Pregunta retadora, no en Rutina.',
}
ccards=''
for c in TOP_CREATORS:
    g=cagg[c]; f=f'videos/creador_{cslug[c]}.mp4'
    media = f'<video controls playsinline preload="metadata" src="{f}"></video>' if os.path.exists(f) else f'<div class="vph">{PH_SVG}<span>Video pendiente</span></div>'
    bv=VIDEOS[cbest[c]][0]; bg=vagg[cbest[c]]
    ccards += f'''<div class="ccard">
  <div class="vmedia">{media}</div>
  <div class="cinfo">
    <div class="cn">{c}</div><div class="cr">{crole[c]} · {g['share']:.0f}% del gasto</div>
    <div class="cbig"><div><b>{r2(g['roas'])}</b><span>ROAS</span></div><div><b>{g['compras']}</b><span>Compras</span></div><div><b>{cop(g['cpa'])}</b><span>Por compra</span></div><div><b>{bv}</b><span>Mejor video · {r2(bg['roas'])}</span></div></div>
    <p>{cnote[c]}</p>
  </div>
</div>'''

head = open('/Users/realjuanfe/Desktop/sin-intermediarios-analisis/index.html').read().split('<body>')[0]
head = head.replace('511 compras con ROAS 5,43 y qué decidimos con cada ángulo', '791 compras con ROAS 5,86. Ranking de ángulos, videos y creadores, y qué hacer para seguir escalando')
extra_css = '''
        .dot { display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:8px; transform:translateY(-1px); }
        .dot.ok, .bar i.ok { background: var(--green); } .dot.mid { background:#f59e0b; } .dot.bad { background:#dc2626; }
        .rtable td small { display:block; font-size:11px; color:#9ca3af; font-weight:600; }
        .rtable .vrow td { text-align:left; white-space:normal; font-size:13px; color:#6b7280; padding:0 14px 14px 31px; border-bottom:1px solid var(--line); }
        .rtable .vn { text-align:left; white-space:normal; font-size:12.5px; color:#6b7280; min-width:260px; line-height:1.4; }
        .rtable .ad small { text-transform:none; letter-spacing:0; }
        .rank-name em { font-style:normal; font-size:10px; font-weight:700; color:#b45309; background:#fef3c7; border-radius:50px; padding:2px 8px; margin-left:6px; vertical-align:middle; }
        .steps { list-style:none; display:grid; gap:12px; counter-reset: s; }
        .steps li { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px 22px 20px 64px; position:relative; font-size:15px; color:#4b5563; line-height:1.55; }
        .steps li::before { counter-increment:s; content: counter(s); position:absolute; left:20px; top:18px; width:30px; height:30px; border-radius:50%; background:var(--navy); color:#fff; font-weight:900; font-size:14px; display:flex; align-items:center; justify-content:center; }
        .steps li b { display:block; color:var(--ink); font-size:16.5px; font-weight:800; letter-spacing:-0.3px; margin-bottom:6px; }
        .steps li.win { border:1.5px solid var(--green); }
        .kpi-chips { grid-template-columns: repeat(4,1fr); }
        .chip em { display:block; font-style:normal; font-size:11.5px; font-weight:700; margin-top:6px; color:var(--green); }
        .chip em.up { color:#dc2626; }
        .split { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:16px; }
        .split > div { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px 22px; }
        .split > div.hi { border:1.5px solid var(--green); }
        .split .st { font-size:11px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted); margin-bottom:10px; }
        .split .sr { font-size:36px; font-weight:900; letter-spacing:-1.5px; line-height:1; color:var(--ink); }
        .split .hi .sr { color:var(--green); }
        .split .sm { font-size:13px; color:#6b7280; margin-top:8px; line-height:1.5; }
        @media (max-width:720px){ .kpi-chips{grid-template-columns:1fr 1fr;} .split{grid-template-columns:1fr;} .steps li{padding:18px 18px 18px 56px;} }

        .vgrid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
        .vcard { background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden; }
        .vmedia { position:relative; aspect-ratio:9/16; background:#0D1B2A; }
        .vmedia video { width:100%; height:100%; object-fit:cover; display:block; }
        .vph { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; color:#94a3b8; font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; background:repeating-linear-gradient(135deg, rgba(255,255,255,0.03) 0 12px, transparent 12px 24px); }
        .vph svg { width:46px; height:46px; }
        .vroas { position:absolute; top:12px; left:12px; background:var(--green); color:#fff; font-weight:900; font-size:15px; letter-spacing:-0.3px; padding:5px 11px; border-radius:50px; }
        .vroas small { font-weight:700; font-size:9.5px; letter-spacing:1px; margin-left:4px; }
        .vinfo { padding:14px 16px 16px; }
        .vinfo b { display:block; font-size:15px; font-weight:800; color:var(--ink); letter-spacing:-0.2px; }
        .vinfo > span { display:block; font-size:12px; color:#9ca3af; font-weight:600; margin:2px 0 10px; }
        .vinfo .piece-stats { gap:5px; } .vinfo .piece-stats span { display:inline-block; margin:0; font-size:10.5px; padding:2px 8px; }
        @media (max-width:720px){ .vgrid{grid-template-columns:1fr 1fr; gap:10px;} .vinfo{padding:12px;} .vinfo b{font-size:13.5px;} }

        .cgrid { display:grid; gap:14px; }
        .ccard { background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden; display:grid; grid-template-columns:150px 1fr; }
        .ccard .vmedia { aspect-ratio:9/16; }
        .cinfo { padding:20px 24px; display:flex; flex-direction:column; justify-content:center; }
        .cinfo .cn { font-size:19px; font-weight:900; color:var(--ink); letter-spacing:-0.5px; }
        .cinfo .cr { font-size:12px; color:#9ca3af; font-weight:600; margin:2px 0 14px; }
        .cinfo .cbig { display:flex; gap:22px; flex-wrap:wrap; margin-bottom:12px; }
        .cinfo .cbig div b { display:block; font-size:24px; font-weight:900; letter-spacing:-0.8px; color:var(--ink); line-height:1.1; }
        .cinfo .cbig div:first-child b { color:var(--green); }
        .cinfo .cbig div span { font-size:11px; font-weight:700; color:#9ca3af; text-transform:uppercase; letter-spacing:0.5px; }
        .cinfo p { font-size:13.5px; color:#6b7280; margin:0; line-height:1.5; }
        @media (max-width:720px){ .ccard{grid-template-columns:1fr;} .ccard .vmedia{aspect-ratio:9/12;} .cinfo{padding:16px;} }
    </style>'''
head = head.replace('    </style>', extra_css, 1)

body = f'''<body>
    <div class="page">

        <header class="doc-head">
            <div style="display:flex;align-items:center;gap:16px;">
                <span class="client-name">SIN INTERMEDIARIOS</span>
                <span style="color:#cbd5e1;font-weight:300;">&times;</span>
                <img class="lareal" src="logo-la-real.png" alt="LA REAL">
            </div>
            <div class="doc-meta">Análisis · Campaña UGC<br>Corte 21 de septiembre 2026</div>
        </header>

        <div class="eyebrow">Informe de resultados</div>
        <h1>Qué escalar, qué apagar y cómo seguir creciendo</h1>
        <p class="lede">Corte al 21 de septiembre del histórico completo de la campaña UGC en Meta Ads. Tres rankings (ángulo, video, creador) y cinco decisiones para el siguiente ciclo.</p>

        <section>
            <h2>Resumen en números</h2>
            <div class="kpi-chips">
                <div class="chip"><b>{cop(TOTAL['spend'])}</b><span>Inversión total</span></div>
                <div class="chip"><b>{TOTAL['compras']}</b><span>Compras</span></div>
                <div class="chip"><b>{r2(TOTAL['roas'])}</b><span>ROAS de la campaña</span></div>
                <div class="chip"><b>{cop(TOTAL['cpa'])}</b><span>Costo por compra</span></div>
            </div>
            <p style="margin-top:18px">Cada ángulo corre en dos tipos de conjunto de anuncios con los mismos videos: un <strong>conjunto grande</strong> de escala (presupuesto de $80K a $310K diarios) y un <strong>conjunto iso low</strong>, más pequeño (de $38K a $123K diarios), que nació como validación. Separarlos es lo que explica el costo por compra de la campaña:</p>

            <div class="split">
                <div><div class="st">Conjuntos grandes · {E['share']:.0f}% del gasto</div><div class="sr">ROAS {r2(E['roas'])}</div><div class="sm">{cop(E['cpa'])} por compra · CPM {cop(cpm_e)} · presupuestos de $80K a $310K diarios</div></div>
                <div class="hi"><div class="st">Conjuntos iso low · {L['share']:.0f}% del gasto</div><div class="sr">ROAS {r2(L['roas'])}</div><div class="sm">{cop(L['cpa'])} por compra · CPM {cop(cpm_l)} · presupuestos de $38K a $123K diarios</div></div>
            </div>
            <div class="kpi-star" style="margin-top:14px">
                <span class="kpi-star-tag">El hallazgo</span>
                <span class="kpi-star-text">Con <b>los mismos videos</b>, los conjuntos iso low compran a <b>casi la mitad del CPM</b> y rinden <b>el doble de ROAS</b> que los conjuntos grandes. Con el {L['share']:.0f}% de la plata generaron el {100*L['val']/(E['val']+L['val']):.0f}% de las ventas. El problema de la campaña no es el contenido: es que el presupuesto está concentrado en pocos conjuntos grandes que se saturan.</span>
            </div>
        </section>

        <section>
            <h2>Ranking de ángulos</h2>
            <div class="rtable-wrap"><table class="rtable">
                <thead><tr><th>Ángulo</th><th>Inversión</th><th>Compras</th><th>Costo / compra</th><th>ROAS conjunto grande</th><th>ROAS conjunto iso low</th><th>ROAS total</th></tr></thead>
                <tbody>{ang_rows}</tbody>
            </table></div>
            <div class="rcap">ROAS total ponderado por inversión sumando el conjunto grande y el iso low de cada ángulo. En Pregunta retadora el conjunto grande incluye la v2. Verde ≥ 6, amarillo 5–6, rojo &lt; 5.</div>
            <ul class="inc" style="margin-top:20px">{ang_verdicts}</ul>
        </section>

        <section>
            <h2>Ranking de videos</h2>
            <p>Cada video sumando todos los conjuntos donde corrió. Ranking por ROAS entre los videos con 20 compras o más; abajo, las señales con muestra corta.</p>
            <div class="rtable-wrap"><table class="rtable">
                <thead><tr><th>Video</th><th>Inversión</th><th>Compras</th><th>Costo / compra</th><th>ROAS</th><th>Lectura</th></tr></thead>
                <tbody>{vid_rows}</tbody>
            </table></div>
            <div class="rcap">Sin muestra suficiente: {small_txt}.</div>
        </section>

        <section>
            <h2>Los videos que más venden</h2>
            <p>Los seis videos con mejor retorno y muestra sólida. Son los que reciben más presupuesto y marcan el estilo de la segunda tanda.</p>
            <div class="vgrid">{vcards}</div>
        </section>

        <section>
            <h2>Ranking de creadores</h2>
            <p>Todas las piezas de cada creador en todos los conjuntos, con 25 compras o más. Barra verde: retorno. Barra oscura: cuánta plata tiene hoy.</p>
            <div class="rank">{cr_rows}</div>
            <div class="rcap">ROAS ponderado por inversión. Jaime Cobos ("Error deportista") queda fuera: 3 compras con $56.593 invertidos.</div>
            <div class="kpi-star" style="margin-top:16px">
                <span class="kpi-star-tag">Lo que sigue al revés</span>
                <span class="kpi-star-text">Jaime, David y Alejandra concentran el <b>52% del gasto</b> con ROAS entre 4,65 y 6,29. Sammy y Yeyo, los dos mejores del ranking, tienen el <b>23%</b>. Y los cinco videos ganadores (Creatina costosa, Rutina v2, Pregunta v2, Curiosidad, Pregunta frecuente) rinden <b>{r2(gwin['roas'])}</b> con apenas el <b>{gwin['share']:.0f}% del presupuesto</b>.</span>
            </div>
        </section>

        <section>
            <h2>Los creadores que más venden</h2>
            <p>Los cinco creadores que repiten en la segunda tanda, con su mejor pieza. El video de cada tarjeta es su pieza más vendedora.</p>
            <div class="cgrid">{ccards}</div>
        </section>

        <section>
            <h2>Qué hacer para seguir escalando</h2>
            <ol class="steps">
                <li class="win"><b>Escalar en horizontal, no en vertical.</b> Dejar de subir presupuesto a conjuntos grandes. Montar conjuntos de $80K a $125K diarios, uno por video ganador, y crecer duplicando conjuntos, no presupuesto. La prueba ya existe: el conjunto iso low de Pregunta retadora corre a $123K/día y sostiene 8,98 con 92 compras. Regla: conjunto con frecuencia mayor a 4 se refresca o se apaga.</li>
                <li><b>Poner la plata en los cinco videos ganadores.</b> Creatina costosa (Sammy), Rutina v2 (Natalia), Pregunta v2 (Gabriela), Curiosidad y Pregunta frecuente (Yeyo). Hoy tienen el {gwin['share']:.0f}% del gasto y rinden {r2(gwin['roas'])} a {cop(gwin['cpa'])} por compra. Cada uno con su conjunto propio para que Meta no vuelva a concentrar la entrega en el video de mejor clic.</li>
                <li><b>Apagar cinco videos.</b> Creatina de Alejandra (3,39), Rutina v1 de Natalia (3,64), Triatlón de Camila (3,75), Snack de Gabriela (3,92) y Creencias de Yeyo (4,25). Suman {cop(goff['spend'])} ({goff['share']:.0f}% del gasto) a ROAS {r2(goff['roas'])}. Esa misma plata en los ganadores serían unos {mill(uplift)} más en ventas.</li>
                <li><b>Ponerle tope a los dos videos más caros.</b> "Pagar más" de David y "Proteína" de Alejandra son el 25% del gasto y rinden 5,15 y 5,17, por debajo del promedio. No se apagan ("Pagar más" tiene el mejor CTR y CPC de la campaña) pero ninguno vuelve a pasar del 10% del presupuesto. La creatina de Jaime sigue, pero en conjunto iso low: allí rinde 9,22 y en el conjunto grande está en frecuencia 5,05.</li>
                <li><b>Segunda tanda de contenido con los que ya vendieron.</b> Repiten Sammy, Natalia, Gabriela, Yeyo y Jaime (nueva versión de creatina: la v1 está agotada). Los hooks a replicar son Creatina costosa, Rutina v2 y Pregunta. Luisa y Exio se prueban en conjunto iso low antes de decidir (10,63 y 16,08 allí, pero con muestra corta). Alejandra y Camila no repiten. Del material en crudo pueden salir versiones nuevas sin producción adicional.</li>
            </ol>
            <div class="guarantee">
                <span class="g-tag">En una frase</span>
                <p>El contenido ya demostró que vende: <b>ROAS 5,86 con $19,7M invertidos</b>. Lo que frena el crecimiento es la estructura. Muchos conjuntos iso low con los videos ganadores, tope a los videos caros y una segunda tanda con los creadores que ya vendieron.</p>
            </div>
        </section>

        <div class="foot">
            <span>Preparado por <img src="logo-la-real.png" alt="LA REAL"> — Agencia digital</span>
            <span>juanfe@larealmarketing.com</span>
        </div>

    </div>
</body>
</html>
'''
open('/Users/realjuanfe/Desktop/sin-intermediarios-analisis/index.html','w').write(head+body)
print('written', len(head+body))
