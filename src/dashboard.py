
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("data/kepler_clean.csv")
bins = [0, 1.25, 2, 4, 6, 14, 100]
labels = ["Rocky", "Super-Earth", "Sub-Neptune", "Neptune", "Sub-Jovian", "Jovian"]
df["size_class"] = pd.cut(df["koi_prad"], bins=bins, labels=labels)
df = df.dropna(subset=["koi_teq", "koi_period", "koi_prad"])

COLOR_MAP = {
    "Rocky": "#e07b54",
    "Super-Earth": "#00e5ff",
    "Sub-Neptune": "#00bcd4",
    "Neptune": "#0097a7",
    "Sub-Jovian": "#80deea",
    "Jovian": "#b2ebf2",
}

BG = "#010b13"
CARD = "#0d1f2d"
BORDER = "#0d2b3e"
ACCENT = "#00e5ff"
MUTED = "#4a7a8a"
TEXT = "#e0f7fa"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;600&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#010b13; color:#e0f7fa; font-family:Inter,sans-serif; overflow-x:hidden; }
::-webkit-scrollbar{width:6px} ::-webkit-scrollbar-track{background:#010b13} ::-webkit-scrollbar-thumb{background:#00e5ff44;border-radius:3px}
#landing { position:relative; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; overflow:hidden; text-align:center; }
.planet { position:absolute; border-radius:50%; animation:floatPlanet linear infinite; z-index:1; }
@keyframes floatPlanet { 0%{transform:translateY(110vh);opacity:0} 5%{opacity:0.7} 95%{opacity:0.7} 100%{transform:translateY(-20vh);opacity:0} }
.landing-content { position:relative; z-index:2; display:flex; flex-direction:column; align-items:center; gap:18px; padding:20px; }
.landing-title { font-family:Orbitron,sans-serif; font-size:clamp(1.8rem,4vw,3.5rem); font-weight:900; color:#00e5ff; letter-spacing:2px; }
.landing-sub { font-size:1rem; color:#80deea; font-weight:300; max-width:560px; line-height:1.7; }
.pill { background:rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.25); border-radius:50px; padding:7px 20px; font-size:0.85rem; color:#00e5ff; display:inline-block; margin:4px; }
.scroll-cta { margin-top:16px; color:#4a7a8a; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase; animation:pulse 2s ease-in-out infinite; }
.arrow { width:20px; height:20px; border-right:2px solid #00e5ff55; border-bottom:2px solid #00e5ff55; transform:rotate(45deg); margin:8px auto 0; animation:bounce 1.5s ease-in-out infinite; }
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}
@keyframes bounce{0%,100%{transform:rotate(45deg) translateY(0)}50%{transform:rotate(45deg) translateY(6px)}}
#dashboard { padding:0 28px 60px; }
.stats-row { display:flex; gap:14px; flex-wrap:wrap; padding:24px 0; }
.stat-card { flex:1; min-width:130px; background:#0d1f2d; border:1px solid #0d2b3e; border-radius:12px; padding:14px 18px; position:relative; overflow:hidden; }
.stat-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; background:linear-gradient(90deg,transparent,#00e5ff,transparent); }
.stat-val { font-family:Orbitron,sans-serif; font-size:1.3rem; color:#00e5ff; font-weight:700; }
.stat-lbl { font-size:0.7rem; color:#4a7a8a; margin-top:4px; text-transform:uppercase; letter-spacing:1px; }
.controls { display:flex; gap:32px; flex-wrap:wrap; background:#0d1f2d; border:1px solid #0d2b3e; border-radius:14px; padding:18px 24px; margin-bottom:18px; align-items:center; }
.ctrl-lbl { font-size:0.72rem; color:#4a7a8a; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
.charts-row { display:flex; gap:18px; margin-bottom:18px; flex-wrap:wrap; }
.card { background:#0d1f2d; border:1px solid #0d2b3e; border-radius:14px; padding:20px; flex:1; min-width:280px; }
.chart-title { font-size:0.88rem; color:#00e5ff; margin-bottom:3px; font-weight:600; letter-spacing:.5px; }
.chart-hint { font-size:0.7rem; color:#4a7a8a; margin-bottom:10px; }
"""

app = Dash(__name__)

app.index_string = """<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>Kepler Exoplanet Explorer</title>
{%favicon%}
{%css%}
<style>""" + CSS + """</style>
</head>
<body>
{%app_entry%}
{%config%}
{%scripts%}
{%renderer%}
<script>
(function(){
  var colors = ['#00e5ff','#e07b54','#80deea','#0097a7','#b2ebf2','#00bcd4'];
  var landing = document.getElementById('landing');
  if(!landing) return;
  for(var i=0;i<10;i++){
    var p = document.createElement('div');
    p.className = 'planet';
    var size = Math.random()*80+20;
    var color = colors[Math.floor(Math.random()*colors.length)];
    var dur = Math.random()*18+10;
    var delay = Math.random()*-25;
    p.style.cssText = 'width:'+size+'px;height:'+size+'px;left:'+Math.random()*100+'%;background:radial-gradient(circle at 35% 35%,'+color+'cc,'+color+'22);box-shadow:0 0 30px 6px '+color+'44;animation-duration:'+dur+'s;animation-delay:'+delay+'s;';
    landing.appendChild(p);
  }
})();
document.addEventListener('DOMContentLoaded', function(){
  var btn = document.getElementById('scroll-btn');
  if(btn){
    btn.addEventListener('click', function(){
      document.getElementById('dashboard').scrollIntoView({behavior:'smooth'});
    });
    btn.addEventListener('mouseover', function(){ this.style.background='rgba(0,229,255,0.2)'; this.style.boxShadow='0 0 20px rgba(0,229,255,0.3)'; });
    btn.addEventListener('mouseout',  function(){ this.style.background='rgba(0,229,255,0.1)'; this.style.boxShadow='none'; });
  }
});
</script>
</body>
</html>"""

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div("🪐", style={"fontSize":"3.5rem","marginBottom":"10px"}),
            html.H1("Kepler Exoplanet Explorer", className="landing-title"),
            html.P("Exploring 4,600+ worlds discovered by NASA's Kepler Space Telescope", className="landing-sub"),
            html.Div([
                html.Span("4,618 Exoplanets", className="pill"),
                html.Span("359 Habitable Candidates", className="pill"),
                html.Span("Real NASA Data", className="pill"),
            ]),
            html.Div([
            html.Button("Scroll to Explore", id="scroll-btn",
                style={"background":"rgba(0,229,255,0.1)","border":"1px solid rgba(0,229,255,0.4)",
                       "color":"#00e5ff","padding":"12px 32px","borderRadius":"50px","cursor":"pointer",
                       "fontSize":"0.9rem","letterSpacing":"2px","textTransform":"uppercase",
                       "fontFamily":"Inter,sans-serif","marginBottom":"12px",
                       "transition":"all 0.3s ease"}),
            html.Div(className="arrow"),
        ], className="scroll-cta"),
        dcc.Location(id="url", refresh=False),
        ], className="landing-content"),
    ], id="landing"),

    html.Div([
        html.Div(id="stats-bar", className="stats-row"),
        html.Div([
            html.Div([
                html.Div("Filter by Planet Type", className="ctrl-lbl"),
                dcc.Checklist(
                    id="size-filter",
                    options=[{"label": html.Span(l, style={"color":COLOR_MAP[l],"marginRight":"14px","fontWeight":"600"}), "value":l} for l in labels],
                    value=labels, inline=True,
                ),
            ], style={"flex":"1"}),
            html.Div([
                html.Div("Orbital Period Range (days)", className="ctrl-lbl"),
                dcc.RangeSlider(id="period-slider", min=0, max=500, step=10, value=[0,500],
                    marks={0:"0",100:"100",200:"200",300:"300",400:"400",500:"500+"},
                    tooltip={"placement":"bottom"}),
            ], style={"flex":"1"}),
        ], className="controls"),

        html.Div([
            html.Div([
                html.Div("3D Planet Explorer", className="chart-title"),
                html.Div("Drag to rotate  |  Scroll to zoom  |  Hover for details", className="chart-hint"),
                dcc.Graph(id="scatter-3d", style={"height":"460px"}),
            ], className="card", style={"flex":"2"}),
            html.Div([
                html.Div("Orbital Period vs Planet Size", className="chart-title"),
                html.Div("Each dot is a real exoplanet", className="chart-hint"),
                dcc.Graph(id="scatter-2d", style={"height":"460px"}),
            ], className="card", style={"flex":"1"}),
        ], className="charts-row"),

        html.Div([
            html.Div([
                html.Div("Planet Type Distribution", className="chart-title"),
                html.Div("How common is each type?", className="chart-hint"),
                dcc.Graph(id="bar-chart", style={"height":"280px"}),
            ], className="card"),
            html.Div([
                html.Div("Temperature + Habitable Zone", className="chart-title"),
                html.Div("Green band = liquid water possible", className="chart-hint"),
                dcc.Graph(id="temp-hist", style={"height":"280px"}),
            ], className="card"),
            html.Div([
                html.Div("Orbital Simulation", className="chart-title"),
                html.Div("Top 20 shortest-period planets", className="chart-hint"),
                dcc.Graph(id="orbit-chart", style={"height":"280px"}),
            ], className="card"),
        ], className="charts-row"),

    ], id="dashboard"),
], style={"background":BG,"minHeight":"100vh"})


@app.callback(
    Output("stats-bar","children"),
    Output("scatter-3d","figure"),
    Output("scatter-2d","figure"),
    Output("bar-chart","figure"),
    Output("temp-hist","figure"),
    Output("orbit-chart","figure"),
    Input("size-filter","value"),
    Input("period-slider","value"),
)
def update(selected, period_range):
    filtered = df[df["size_class"].isin(selected) & (df["koi_period"]>=period_range[0]) & (df["koi_period"]<=period_range[1])]
    hz = filtered[(filtered["koi_teq"]>=200)&(filtered["koi_teq"]<=320)]

    stats = [("🪐",f"{len(filtered):,}","Planets Shown"),("🌡",f"{filtered['koi_teq'].mean():.0f} K","Avg Temperature"),
             ("📅",f"{filtered['koi_period'].mean():.1f}d","Avg Orbital Period"),("🌍",f"{len(hz):,}","Habitable Candidates"),
             ("📏",f"{filtered['koi_prad'].mean():.2f} Re","Avg Radius")]
    stat_cards = [html.Div([html.Div(icon,style={"fontSize":"1.3rem","marginBottom":"5px"}),html.Div(val,className="stat-val"),html.Div(lbl,className="stat-lbl")],className="stat-card") for icon,val,lbl in stats]

    dark = dict(paper_bgcolor=BG,plot_bgcolor=BG,font=dict(color=TEXT,family="Inter"),margin=dict(l=40,r=20,t=10,b=40))
    grid = dict(gridcolor=BORDER,zerolinecolor=BORDER)

    fig3d = go.Figure()
    for pt in selected:
        sub = filtered[filtered["size_class"]==pt]
        fig3d.add_trace(go.Scatter3d(x=sub["koi_period"],y=sub["koi_prad"],z=sub["koi_teq"],mode="markers",name=pt,
            marker=dict(size=np.clip(sub["koi_prad"]*1.5,2,12),color=COLOR_MAP[pt],opacity=0.85,line=dict(width=0)),
            hovertemplate="Period: %{x:.1f}d<br>Radius: %{y:.2f} Re<br>Temp: %{z:.0f}K<extra>"+pt+"</extra>"))
    fig3d.update_layout(paper_bgcolor=BG,font=dict(color=TEXT),margin=dict(l=0,r=0,t=0,b=0),
        scene=dict(bgcolor=BG,xaxis=dict(title="Period (days)",backgroundcolor=BG,gridcolor=BORDER,color=MUTED),
                   yaxis=dict(title="Radius (Re)",backgroundcolor=BG,gridcolor=BORDER,color=MUTED),
                   zaxis=dict(title="Temp (K)",backgroundcolor=BG,gridcolor=BORDER,color=MUTED)),
        legend=dict(bgcolor="rgba(0,0,0,0)"))

    fig2d = px.scatter(filtered,x="koi_period",y="koi_prad",color="size_class",color_discrete_map=COLOR_MAP,
        log_x=True,log_y=True,labels={"koi_period":"Orbital Period (days)","koi_prad":"Planet Radius (Re)","size_class":"Type"})
    fig2d.update_traces(marker=dict(size=5,opacity=0.65))
    fig2d.update_layout(**dark,xaxis=dict(**grid,color=MUTED),yaxis=dict(**grid,color=MUTED),legend=dict(bgcolor="rgba(0,0,0,0)"))

    counts = filtered["size_class"].value_counts().reindex(labels).fillna(0)
    figbar = go.Figure(go.Bar(x=counts.index.tolist(),y=counts.values,marker=dict(color=[COLOR_MAP[l] for l in labels],line=dict(width=0))))
    figbar.update_layout(**dark,xaxis=dict(**grid,color=MUTED),yaxis=dict(**grid,color=MUTED))

    fighist = go.Figure()
    fighist.add_trace(go.Histogram(x=filtered["koi_teq"],nbinsx=50,name="All",marker_color="#1a3a4a",opacity=0.9))
    fighist.add_trace(go.Histogram(x=hz["koi_teq"],nbinsx=20,name="Habitable Zone",marker_color=ACCENT,opacity=0.9))
    fighist.add_vrect(x0=200,x1=320,fillcolor=ACCENT,opacity=0.07,line_width=0)
    fighist.update_layout(**dark,barmode="overlay",xaxis=dict(**grid,color=MUTED),yaxis=dict(**grid,color=MUTED),legend=dict(bgcolor="rgba(0,0,0,0)"))

    sample = filtered.nsmallest(20,"koi_period").reset_index(drop=True)
    theta = np.linspace(0,2*np.pi,120)
    figorbit = go.Figure()
    figorbit.add_trace(go.Scatter(x=[0],y=[0],mode="markers",marker=dict(size=22,color="#ffe066",line=dict(color="#ffcc00",width=2)),name="Star",hoverinfo="skip"))
    for _,row in sample.iterrows():
        r = np.log1p(row["koi_period"])*14
        figorbit.add_trace(go.Scatter(x=r*np.cos(theta),y=r*np.sin(theta),mode="lines",line=dict(color=BORDER,width=1),showlegend=False,hoverinfo="skip"))
        ang = np.random.uniform(0,2*np.pi)
        pt = str(row.get("size_class","Rocky"))
        figorbit.add_trace(go.Scatter(x=[r*np.cos(ang)],y=[r*np.sin(ang)],mode="markers",
            marker=dict(size=max(5,min(row["koi_prad"]*3,16)),color=COLOR_MAP.get(pt,ACCENT),line=dict(color=ACCENT,width=1)),
            hovertemplate=f"Period: {row['koi_period']:.1f}d<br>Radius: {row['koi_prad']:.2f} Re<extra></extra>",showlegend=False))
    figorbit.update_layout(paper_bgcolor=BG,plot_bgcolor=BG,margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(visible=False,range=[-130,130]),yaxis=dict(visible=False,range=[-130,130],scaleanchor="x"),showlegend=False)

    return stat_cards,fig3d,fig2d,figbar,fighist,figorbit

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 8050))
app.run(debug=False, host="0.0.0.0", port=port)
