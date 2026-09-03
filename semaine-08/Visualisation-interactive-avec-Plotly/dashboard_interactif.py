import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 1. Création du dataset

data = {
    "date": pd.date_range(
        start="2026-01-01",
        periods=12,
        freq="MS",
    ),
    "marche": [
        "France",
        "France",
        "France",
        "France",
        "France",
        "France",
        "Mali",
        "Mali",
        "Mali",
        "Mali",
        "Mali",
        "Mali",
    ],
    "prix": [
        120,
        125,
        130,
        128,
        135,
        140,
        100,
        105,
        110,
        108,
        115,
        120,
    ],
    "volume": [
        80,
        90,
        95,
        100,
        110,
        120,
        70,
        75,
        85,
        90,
        100,
        105,
    ],
}

df = pd.DataFrame(data)


# 2. Création de la figure avec 3 subplots

fig = make_subplots(
    rows=3,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=(
        "Évolution du prix",
        "Volume des ventes",
        "Distribution des prix",
    ),
)


# 3. Ajout des graphiques

marches = df["marche"].unique()


# Graphique 1 : évolution du prix
for marche in marches:

    donnees_marche = df[df["marche"] == marche]

    fig.add_trace(
        go.Scatter(
            x=donnees_marche["date"],
            y=donnees_marche["prix"],
            mode="lines+markers",
            name=f"Prix - {marche}",
            visible=(marche == marches[0]),
        ),
        row=1,
        col=1,
    )


# Graphique 2 : volume
for marche in marches:

    donnees_marche = df[df["marche"] == marche]

    fig.add_trace(
        go.Bar(
            x=donnees_marche["date"],
            y=donnees_marche["volume"],
            name=f"Volume - {marche}",
            visible=(marche == marches[0]),
        ),
        row=2,
        col=1,
    )


# Graphique 3 : distribution des prix
for marche in marches:

    donnees_marche = df[df["marche"] == marche]

    fig.add_trace(
        go.Histogram(
            x=donnees_marche["prix"],
            name=f"Distribution - {marche}",
            visible=(marche == marches[0]),
            nbinsx=6,
        ),
        row=3,
        col=1,
    )



# 4. Création du dropdown

nombre_marches = len(marches)

boutons = []

for index, marche in enumerate(marches):

    visibilite = [False] * (nombre_marches * 3)

    # Graphique 1
    visibilite[index] = True

    # Graphique 2
    visibilite[nombre_marches + index] = True

    # Graphique 3
    visibilite[(2 * nombre_marches) + index] = True

    boutons.append(
        {
            "label": marche,
            "method": "update",
            "args": [
                {"visible": visibilite},
                {
                    "title": (
                        f"Dashboard interactif - Marché : {marche}"
                    )
                },
            ],
        }
    )


# 5. Création du slider de période

dates = sorted(df["date"].unique())

slider_steps = []

for date in dates:

    date_fin = pd.Timestamp(date)

    slider_steps.append(
        {
            "label": date_fin.strftime("%b %Y"),
            "method": "relayout",
            "args": [
                {
                    "xaxis.range": [
                        df["date"].min(),
                        date_fin,
                    ],
                    "xaxis2.range": [
                        df["date"].min(),
                        date_fin,
                    ],
                    "xaxis3.range": [
                        df["date"].min(),
                        date_fin,
                    ],
                }
            ],
        }
    )


# 6. Configuration du dashboard

fig.update_layout(
    title="Dashboard interactif des ventes",
    height=1000,
    template="plotly_white",
    hovermode="x unified",

    updatemenus=[
        {
            "buttons": boutons,
            "direction": "down",
            "showactive": True,
            "x": 0.01,
            "xanchor": "left",
            "y": 1.12,
            "yanchor": "top",
        }
    ],

    sliders=[
        {
            "active": len(slider_steps) - 1,
            "currentvalue": {
                "prefix": "Période : "
            },
            "pad": {
                "t": 50
            },
            "steps": slider_steps,
        }
    ],
)


# 7. Labels des axes

fig.update_xaxes(
    title_text="Date",
    row=1,
    col=1,
)

fig.update_xaxes(
    title_text="Date",
    row=2,
    col=1,
)

fig.update_xaxes(
    title_text="Prix",
    row=3,
    col=1,
)

fig.update_yaxes(
    title_text="Prix (€)",
    row=1,
    col=1,
)

fig.update_yaxes(
    title_text="Volume",
    row=2,
    col=1,
)

fig.update_yaxes(
    title_text="Nombre",
    row=3,
    col=1,
)


# 8. Export HTML autonome

fig.write_html(
    "dashboard_interactif.html",
    include_plotlyjs=True,
    full_html=True,
)

print("Dashboard créé : dashboard_interactif.html")