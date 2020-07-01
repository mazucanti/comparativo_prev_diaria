#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:35:30 2020

@author: mazucanti
"""

import pandas as pd
import datetime as dt
from pathlib import Path
import os

from sincrawl.implementa import RodaPDP

aranha = RodaPDP()
aranha.roda()


def main():
    df1, df2 = importa_planilhas()
    df1 = trata_planilha(df1)
    df2 = trata_planilha(df2)
    comp = []
    for i in range(len(df1)):
        comp.append(df2[i] - df1[i])
        comp[i].dropna(axis=1, inplace=True)
    exporta_df([df1,df2,comp])
   
    

def formata_nome(começo, final):
    nome = "Relatorio_previsao_diaria_%s_%s_%s_para_%s_%s_%s.xls" % (
        '0'+str(começo.day) if começo.day<10 else str(começo.day),
        '0'+str(começo.month) if começo.month<10 else str(começo.month),
        str(começo.year),
        '0'+str(final.day) if final.day<10 else str(final.day),
        '0'+str(final.month) if final.month<10 else str(final.month),
        str(final.year))
    return nome


def importa_planilhas():
    hoje = dt.date.today()
    ontem = hoje - dt.timedelta(days=1)
    final1 = hoje + dt.timedelta(days=2)
    final2 = ontem + dt.timedelta(days=2)
    nome_hoje = formata_nome(hoje, final1)
    nome_ontem = formata_nome(ontem,final2)
    local = Path('entradas')
    local_h = local / nome_hoje
    local_o = local / nome_ontem
    h_pt1 = pd.read_excel(local_h, sheet_name = "Diária_6", header = 4)
    h_pt2 = pd.read_excel(local_h, sheet_name = "Diária_7", header = 4)
    o_pt1 = pd.read_excel(local_o, sheet_name = "Diária_6", header = 4)
    o_pt2 = pd.read_excel(local_o, sheet_name = "Diária_7", header = 4)
    df_h = pd.concat([h_pt1, h_pt2])
    df_o = pd.concat([o_pt1, o_pt2])
    return df_h, df_o


def trata_planilha(df):
    local = Path('entradas/postos.csv')
    postos = pd.read_csv(local, index_col = 0)
    tabelas = []
    subm = postos['sub_mer']
    ree = postos['ree']
    bac = postos['bacia']
    df.dropna(axis = 0, inplace = True)
    df.set_index(['Cód.'], inplace = True)
    df.drop(['Cód.'], axis = 0, inplace = True)
    df.drop(['APROVEITAMENTO / RESERVATÓRIO'], axis = 1, inplace = True)
    subm = (pd.concat([df,subm], axis = 1)).groupby('sub_mer').sum()
    subm.sort_index(ascending = False, inplace = True)
    tabelas.append(subm)
    ree = (pd.concat([df,ree], axis = 1)).groupby('ree').sum()
    tabelas.append(ree)
    bac = (pd.concat([df,bac], axis = 1)).groupby('bacia').sum()
    tabelas.append(bac)
    return tabelas


def exporta_df(tabelas):
    nomes = []
    data = dt.date.today()
    nomes.append("Previsão_diária_%d-%d-%d" % (data.year,data.month,data.day))
    data = data - dt.timedelta(days = 1)
    nomes.append("Previsão_diária_%d-%d-%d" % (data.year,data.month,data.day))
    nomes.append("Comparativo")
    local = Path('saídas/comparativo_previsao_diaria.xls')
    formato = [0,6,20]
    with pd.ExcelWriter(local) as writer:
        for i, tabela in enumerate(tabelas):
            for j, df in enumerate(tabela):
                df.to_excel(writer, sheet_name = nomes[i], startrow = formato[j])
        
    
main()