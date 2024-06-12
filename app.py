import pandas as pd
import streamlit as st
import datetime as dt
import plotly.express as px
from random import randint, random, uniform
import faker


uploaded_file = st.file_uploader('Input data', type='xls')

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df['year'] = df['Game Start'].dt.year
    df['month'] = df['Game Start'].dt.month
    df['year-month'] = df['Game Start'].dt.strftime('%Y-%m')
    df['amount'] = df['Travel'] + df['Accreditation'] + df['Extra'] + df['Earnings']
else:
    st.header('EXEMPLE')
    list = []
    sport = 'Soccer'
    coverage = 'LIVE'
    game_confirmation = 'Confirmed by Scout'
    play_state = 'Finished'
    gmt = 'GMT-3'
    country = 'Brazil'
    competition = ['Serie A', 'Serie B', 'Libertadores', 'Brazil Cup', 'Estadual']
    competitor = [
    "AA Internacional",
    "ABC Futebol Clube",
    "América Futebol Clube (RN)",
    "Athletico Paranaense",
    "Avaí Futebol Clube",
    "Bahia Esporte Clube",
    "Botafogo de Futebol e Regatas",
    "Ceará Sporting Club",
    "Clube Atlético Mineiro",
    "Clube de Regatas do Flamengo",
    "Corinthians Paulista",
    "Coritiba Foot-Ball Club",
    "Criciúma Esporte Clube",
    "Cruzeiro Esporte Clube",
    "Cuiabá Esporte Clube",
    "EC Bahia",
    "EC Juventude",
    "Esporte Clube Goiás",
    "Fortaleza Esporte Clube",
    "Goiás Esporte Clube",
    "Grêmio Esportivo Brasil",
    "Guarani Futebol Clube",
    "Internacional",
    "Ituano Futebol Clube",
    "Jacuipense Esporte Clube",
    "Joinville Esporte Clube",
    "Londrina Esporte Clube",
    "Madureira Esporte Clube",
    "Náutico Futebol Clube",
    "Oeste Futebol Clube",
    "Paraná Clube",
    "Paysandu Sport Club",
    "Red Bull Bragantino",
    "Red Bull Brasil",
    "Remo Esporte Clube",
    "Sampaio Corrêa Futebol Clube",
    "Santos Futebol Clube",
    "São Bento Futebol Clube",
    "São Caetano Esporte Clube",
    "São Paulo Futebol Clube",
    "SER Caxias",
    "Sport Club do Recife",
    "Vitória Esporte Clube",
]	
    venue = [
    "Maracanã (Rio de Janeiro)",
    "Estádio Mané Garrincha (Brasília)",
    "Morumbi (São Paulo)",
    "Mineirão (Belo Horizonte)",
    "Arena Castelão (Fortaleza)",
    "Kleber Andrade (Cariacica)",
    "Arena da Baixada (Curitiba)",
    "Estádio Beira-Rio (Porto Alegre)",
    "Estádio Serra Dourada (Goiânia)",
    "Estádio do Pacaembu (São Paulo)",
]
    fake = faker.Faker()
    currency = '$'	
    accreditation = 0
    extra = 0
    confirmed = 'Ok'
    for n in range(0,150):
        random_month = randint(1, 12)
        if random_month in [4, 6, 9, 11]:
            max_day = 30
        elif random_month == 2:
            max_day = 28
        else:
            max_day = 31
        random_day = randint(1, max_day)
        game_start =  dt.datetime(2024, random_month, random_day)
        data = {
        'Sport': sport,
        'Coverage':	coverage,
        'Game Confirmation':game_confirmation,
        'Play State': play_state,
        'ID': randint(10000,99999),
        'Game Start': game_start,
        'GMT Offset': gmt,
        'Country': country,
        'Competition': competition[randint(0,4)],
        'Competitor 1': competitor[randint(0,39)],
        'Competitor 2':	competitor[randint(0,39)],
        'Venue': venue[randint(0,9)],
        'Scout'	: fake.name(),
        'Currency': currency,
        'Travel': uniform(0,10),
        'Ticket': randint(5,30),
        'Accreditation': accreditation,
        'Extra': extra,
        'Earnings': uniform(39,59),
        'Confirmed': confirmed
    }
        list.append(data)
    df = pd.DataFrame(list)
    df['year'] = df['Game Start'].dt.year
    df['month'] = df['Game Start'].dt.month
    df['year-month'] = df['Game Start'].dt.strftime('%Y-%m')
    df['amount'] = df['Travel'] + df['Accreditation'] + df['Extra'] + df['Earnings']

st.header('This Month')

#Metricas
today = dt.datetime.today()
month_actual = today.month

#dfs mes atual e mes anterior
df_month_actual = df[df['month'] == month_actual]
df_month_last_month = df[df['month'] == month_actual - 1]

#qnt_games
qnt_games_actual = int(df_month_actual['ID'].count())
qnt_games_last_month = int(df_month_last_month['ID'].count())
diff_games = qnt_games_actual - qnt_games_last_month

#amount
amount_actual = float(df_month_actual['Earnings'].sum())
amount_last_month = float(df_month_last_month['Earnings'].sum())
diff_amount = amount_actual - amount_last_month

col1, col2 = st.columns(2)
with col1:
    st.metric('Games', value = qnt_games_actual, delta = diff_games , help='vs Last Month')
with col2:
    st.metric('Earnings', value = f'{amount_actual:.2f}', delta = f'{diff_amount:.2f}' , help='vs Last Month')

#Graficos de barras
grouped_data = df[['year-month', 'ID', 'amount']].groupby('year-month')
df_bars = grouped_data.agg({ 'ID': 'count', 'amount': 'sum'})
df_bars = df_bars.reset_index()

st.bar_chart(df_bars, x= 'year-month' , y='amount',use_container_width=True)
st.line_chart(df_bars, x= 'year-month' , y='ID',use_container_width=True)


st.header('All time')
#
grouped_data_stadium = df[['Venue', 'ID']].groupby('Venue')
df_stadium = grouped_data_stadium.agg({ 'ID': 'count'})
df_stadium = df_stadium.reset_index()

#
grouped_data_competition = df[['Competition', 'ID']].groupby('Competition')
df_competition = grouped_data_competition.agg({ 'ID': 'count'})
df_competition = df_competition.reset_index()

#
stadiums, competitions = st.columns(2)
with stadiums:
    fig_stadium = px.bar(df_stadium.sort_values("ID"), x='ID',y='Venue', 
                       title='Games per Stadium',
                        orientation='h',text_auto=True
                          )
    #fig_stadium.update_traces(textfont_size=12, textangle=0, cliponaxis=False)

    st.plotly_chart(fig_stadium)

with competitions:
    fig_competition = px.bar(df_competition.sort_values("ID"), x='ID',y='Competition', 
                       title='Games per Competition',
                        orientation='h',text_auto=True
                          )
    #fig_competition.update_traces(textfont_size=12, textangle=0, cliponaxis=False)

    st.plotly_chart(fig_competition)