
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
#from highlight_text import ax_text, fig_text

# Data import & columns
af=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/stats/players/2020-2021-Big-5-European-Leagues-Stats')[0]
af = af.droplevel(0, axis=1)
af = af[af.Player != 'Player']
af["MP"] = pd.to_numeric(af["MP"])

af["Player+Team"]=af["Player"]+" "+af["Squad"]

af=af[["Player+Team","MP"]]


df=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/shooting/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df = df.droplevel(0, axis=1)
df = df[df.Player != 'Player']
df["90s"] = pd.to_numeric(df["90s"]).round(2)
df["Gls"] = pd.to_numeric(df["Gls"])
df["Sh/90"] = pd.to_numeric(df["Sh/90"])
df["SoT/90"] = pd.to_numeric(df["SoT/90"])

df["Player+Team"]=df["Player"]+" "+df["Squad"]

dfatt=df.join(af.set_index('Player+Team'), on='Player+Team')


df1=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/misc/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df1 = df1.droplevel(0, axis=1)
df1 = df1[df1.Player != 'Player']
df1["90s"] = pd.to_numeric(df1["90s"])
df1["Fls"] = pd.to_numeric(df1["Fls"])
df1["CrdY"] = pd.to_numeric(df1["CrdY"])

df1["Fls/90"]=(df1["Fls"]/df1["90s"]).round(2)
df1["Player+Team"]=df1["Player"]+" "+df1["Squad"]

cols1= ["Player+Team","Comp","CrdY","Fls","Fls/90"] #,"Squad","90s"

df1 = df1[cols1]

df2=pd.read_html('https://fbref.com/en/comps/Big5/2020-2021/defense/players/2020-2021-Big-5-European-Leagues-Stats')[0]
df2 = df2.droplevel(0, axis=1)
df2 = df2[df2.Player != 'Player']

df2.columns.values[14] = "TEST"

df2["90s"] = pd.to_numeric(df2["90s"])
df2["Tkl"] = pd.to_numeric(df2["Tkl"])

df2["Tkl/90"]=(df2["Tkl"]/df2["90s"]).round(2)
df2["Player+Team"]=df2["Player"]+" "+df2["Squad"]

cols2= ["Player+Team","Player","Squad","90s","Tkl","Tkl/90"] #

df2 = df2[cols2]

dfdef=df1.join(df2.set_index('Player+Team'), on='Player+Team')
dfdef=dfdef.join(af.set_index('Player+Team'), on='Player+Team')

dfdef=dfdef[["Player+Team","Comp","Player","Squad","MP","90s","CrdY","Fls","Fls/90","Tkl","Tkl/90"]]
dfatt=dfatt[["Player+Team","Gls","Sh/90","SoT/90"]]

data=dfatt.join(dfdef.set_index('Player+Team'), on='Player+Team')

data=data[["Comp","Player","Squad","MP","90s","Gls","Sh/90","SoT/90","CrdY","Fls","Fls/90","Tkl","Tkl/90"]]

# App

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')

leagues = list(data['Comp'].drop_duplicates())
league_choice = st.sidebar.selectbox(
    "Filter by league:", leagues, index=1)

data=data.loc[(data['Comp'] == league_choice)]


teams = list(data['Squad'].drop_duplicates())
teams=sorted(teams)
teams_choice = st.sidebar.selectbox(
    "Filter by Team:", teams, index=0)

data=data.loc[(data['Squad'] == teams_choice)]

mins_choice = st.sidebar.number_input(
    'Filter by Minimum 90s played:',step=0.5)

data = data[data['90s'] > mins_choice]

teamcolor = st.sidebar.text_input ('Enter team hex colour',
                                    value="red")

teamcolor2 = st.sidebar.text_input ('Enter team hex colour 2',
                                    value="white")

metrics=["Gls","Sh/90","SoT/90","CrdY","Fls/90","Tkl/90"]

choose_metric = st.sidebar.selectbox(
    "Choose metric:", metrics, index=0)
choose_metric = ''.join(choose_metric)

data = data.sort_values(by=[choose_metric],ascending=False)

players = list(data['Player'].drop_duplicates())
#players = sorted(players)

player_choice_1 = st.sidebar.selectbox(
    "Player 1:", players,index=0)
#player_choice_1 = ''.join(player_choice_1)

player_choice_2 = st.sidebar.selectbox(
    "Player 2:", players, index=1)
#player_choice_2 = ''.join(player_choice_2)

player_choice_3 = st.sidebar.selectbox(
    "Player 3:", players, index=2)
#player_choice_3 = ''.join(player_choice_3)

player_choice_4 = st.sidebar.selectbox(
    "Player 4:", players, index=3)
#player_choice_4 = ''.join(player_choice_4)

player_choice_5 = st.sidebar.selectbox(
    "Player 5:", players, index=4)
#player_choice_5 = ''.join(player_choice_5)


data=data[["Player","Squad","MP","90s","Gls","Sh/90","SoT/90","CrdY","Fls","Fls/90","Tkl","Tkl/90"]]
data["Goals"]=data["Gls"]
# Main
st.title(f"Toolkit Builder")

# Main - dataframes
st.markdown("### Selected Team's Stats 2020/21")

st.dataframe(data.sort_values(by=[choose_metric],ascending=False).reset_index(drop=True))


bgcolor="#FAF9F6"
font='Roboto'
textc="#463f3a"

# Create a data frame
cut_frame=data.loc[(data['Player'] == player_choice_1) | (data['Player'] == player_choice_2) | 
                    (data['Player'] == player_choice_3) | (data['Player'] == player_choice_4) |
                    (data['Player'] == player_choice_5)]

variable=choose_metric
databar=cut_frame

# Sort the table
databar = databar.sort_values(by=[variable])

fig, ax = plt.subplots(figsize=(4.5,8),dpi=80)

plt.rcParams['hatch.linewidth'] = 1
plt.rcParams["font.family"] = font
plt.rcParams['text.color'] = textc
plt.rcParams['font.size'] =20

player_last_names =[]
for name in databar['Player']:
    player_last_names.append(name.split()[-1])

plt.barh(y=player_last_names, width=databar[variable],color=teamcolor,edgecolor=teamcolor2,hatch="\\");

plt.xticks(fontsize=16)
plt.yticks(fontsize=20)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

for i, v in enumerate(databar[variable]):
    if v >= 0:
        ax.text(v+0.1, i-0.1, str(v))

ax.set_facecolor(bgcolor)
fig.patch.set_facecolor(bgcolor)

# Add title
#fig_text(s=f"Top Scorers",ha='center',
 #       x=.5, y =.9, fontsize=22,fontfamily=font,color=textc)

st.pyplot(fig)
