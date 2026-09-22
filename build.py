from data import *
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
 'Pregunta retadora': 'Gana por retorno y por volumen. El conjunto de escala es el único que no se desgastó (frecuencia 2,54, CTR 2,21%) y la versión mediana a $123K/día sostiene 8,98.',
 'Historia de consistencia': 'Se recuperó al salir del conjunto grande: la misma creatina de Jaime rinde 9,22 en el conjunto mediano y 5,21 en el de escala (frecuencia 5,05).',
 'Validadores profesionales': 'Yeyo solo va en 6,02; Alejandra (55% del gasto del ángulo) lo arrastra a 4,65. Es un problema de reparto, no del ángulo.',
 'Rutina real': 'Cayó del segundo al último lugar: el conjunto de escala pasó de 5,60 a 4,62 con el CPM más caro de la campaña ($14.419) y dos videos flojos adentro.',
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
 'exio_creatina': 'Casi todo en el conjunto mediano (16,08). Señal fuerte, muestra corta.',
 'sammy_creatina_costosa': 'El mejor video con muestra sólida. Vive en el conjunto mediano.',
 'luisa_rutina_v1': '10,63 en mediano, 3,25 en escala. Probar de nuevo en mediano.',
 'natalia_rutina_v2': '11,15 en mediano, 5,96 en escala, 0,96 en la v2. Ganador que Meta subestimó.',
 'yeyo_curiosidad': '12,64 en mediano con CPA $13.601, el más barato de la campaña.',
 'yeyo_pregunta_frecuente': 'Sube a 9,05 en mediano; en escala cuesta $29.067 por compra.',
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
                <div class="chip"><b>{cop(TOTAL['spend'])}</b><span>Inversión total</span><em>+{mill(inc_s)} desde el 4 sep</em></div>
                <div class="chip"><b>{TOTAL['compras']}</b><span>Compras</span><em>+{inc_c} desde el 4 sep</em></div>
                <div class="chip"><b>{r2(TOTAL['roas'])}</b><span>ROAS de la campaña</span><em>Venía en 5,43</em></div>
                <div class="chip"><b>{cop(TOTAL['cpa'])}</b><span>Costo por compra</span><em class="up">Venía en $21.532</em></div>
            </div>
            <p style="margin-top:18px">La campaña casi duplicó la inversión desde el corte anterior y el retorno subió: lo invertido después del 4 de septiembre rindió <strong>ROAS {r2(inc_roas)}</strong>. La señal a corregir es el costo por compra, que subió un 16%. Y ese costo tiene una causa clara:</p>

            <div class="split">
                <div><div class="st">Conjuntos de escala · {E['share']:.0f}% del gasto</div><div class="sr">ROAS {r2(E['roas'])}</div><div class="sm">{cop(E['cpa'])} por compra · CPM {cop(cpm_e)} · presupuestos de $80K a $310K diarios</div></div>
                <div class="hi"><div class="st">Conjuntos medianos ("iso low") · {L['share']:.0f}% del gasto</div><div class="sr">ROAS {r2(L['roas'])}</div><div class="sm">{cop(L['cpa'])} por compra · CPM {cop(cpm_l)} · presupuestos de $38K a $123K diarios</div></div>
            </div>
            <div class="kpi-star" style="margin-top:14px">
                <span class="kpi-star-tag">El hallazgo</span>
                <span class="kpi-star-text">Con <b>los mismos videos</b>, los conjuntos medianos compran a <b>casi la mitad del CPM</b> y rinden <b>el doble de ROAS</b> que los conjuntos grandes. Con el {L['share']:.0f}% de la plata generaron el {100*L['val']/(E['val']+L['val']):.0f}% de las ventas. El problema de la campaña no es el contenido: es que el presupuesto está concentrado en pocos conjuntos grandes que se saturan.</span>
            </div>
        </section>

        <section>
            <h2>Ranking de ángulos</h2>
            <div class="rtable-wrap"><table class="rtable">
                <thead><tr><th>Ángulo</th><th>Inversión</th><th>Compras</th><th>Costo / compra</th><th>ROAS escala</th><th>ROAS mediano</th><th>ROAS total</th></tr></thead>
                <tbody>{ang_rows}</tbody>
            </table></div>
            <div class="rcap">ROAS total ponderado por inversión sumando los conjuntos de escala y medianos de cada ángulo. Verde ≥ 6, amarillo 5–6, rojo &lt; 5.</div>
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
            <h2>Qué hacer para seguir escalando</h2>
            <ol class="steps">
                <li class="win"><b>Escalar en horizontal, no en vertical.</b> Dejar de subir presupuesto a conjuntos grandes. Montar conjuntos de $80K a $125K diarios, uno por video ganador, y crecer duplicando conjuntos, no presupuesto. La prueba ya existe: el conjunto mediano de Pregunta retadora corre a $123K/día y sostiene 8,98 con 92 compras. Regla: conjunto con frecuencia mayor a 4 se refresca o se apaga.</li>
                <li><b>Poner la plata en los cinco videos ganadores.</b> Creatina costosa (Sammy), Rutina v2 (Natalia), Pregunta v2 (Gabriela), Curiosidad y Pregunta frecuente (Yeyo). Hoy tienen el {gwin['share']:.0f}% del gasto y rinden {r2(gwin['roas'])} a {cop(gwin['cpa'])} por compra. Cada uno con su conjunto propio para que Meta no vuelva a concentrar la entrega en el video de mejor clic.</li>
                <li><b>Apagar cinco videos.</b> Creatina de Alejandra (3,39), Rutina v1 de Natalia (3,64), Triatlón de Camila (3,75), Snack de Gabriela (3,92) y Creencias de Yeyo (4,25). Suman {cop(goff['spend'])} ({goff['share']:.0f}% del gasto) a ROAS {r2(goff['roas'])}. Esa misma plata en los ganadores serían unos {mill(uplift)} más en ventas.</li>
                <li><b>Ponerle tope a los dos videos más caros.</b> "Pagar más" de David y "Proteína" de Alejandra son el 25% del gasto y rinden 5,15 y 5,17, por debajo del promedio. No se apagan ("Pagar más" tiene el mejor CTR y CPC de la campaña) pero ninguno vuelve a pasar del 10% del presupuesto. La creatina de Jaime sigue, pero en conjunto mediano: allí rinde 9,22 y a escala está en frecuencia 5,05.</li>
                <li><b>Segunda tanda de contenido con los que ya vendieron.</b> Repiten Sammy, Natalia, Gabriela, Yeyo y Jaime (nueva versión de creatina: la v1 está agotada). Los hooks a replicar son Creatina costosa, Rutina v2 y Pregunta. Luisa y Exio se prueban en conjunto mediano antes de decidir (10,63 y 16,08 allí, pero con muestra corta). Alejandra y Camila no repiten. Del material en crudo pueden salir versiones nuevas sin producción adicional.</li>
            </ol>
            <div class="guarantee">
                <span class="g-tag">En una frase</span>
                <p>El contenido ya demostró que vende: <b>ROAS {r2(inc_roas)} en lo invertido del último ciclo</b>. Lo que frena el crecimiento es la estructura. Muchos conjuntos medianos con los videos ganadores, tope a los videos caros y una segunda tanda con los creadores que ya vendieron.</p>
            </div>
        </section>

        <div class="next">
            <h2>Siguiente paso</h2>
            <p>Sobre la mesa en la próxima revisión con el equipo de pauta: <b>aprobar la reestructura a conjuntos medianos</b>, definir el presupuesto de la segunda tanda de contenido y cruzar estos números con el reporte de Shopify. Todos los datos de este informe vienen de Meta Ads; la decisión final se toma contra el costo por compra real de la tienda.</p>
            <a class="cta" href="https://wa.me/573043148428?text=Hola%20Juanfe%2C%20tengo%20una%20duda%20sobre%20el%20an%C3%A1lisis%20de%20la%20campa%C3%B1a%20UGC" target="_blank">
                <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                ¿Dudas? Escríbenos
            </a>
        </div>

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
