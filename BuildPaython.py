-*- coding: iso-8859-1 -*- 

import pandas as pd   

import numpy as np   

import scrapy as scr   

import seaborn as sns 

from matplotlib import pyplot as plt  

 

# Importazione file csv covid19_italy_province.csv 

file="./covid19_italy_province.csv"  

covid_province=pd.read_csv(file,sep=",",index_col="SNo") 

 

# Per queste analisi non ci servono le colonne Country, Latitude e Longitude 

province = covid_province.drop(['Country', 'Latitude', 'Longitude'],axis=1) 

 

# Eliminiamo le righe che contengono valori nulli 

covid_province = province.dropna() 

 

# Importazione file csv covid19_italy_region.csv 

file="./covid19_italy_region.csv"  

covid_regioni=pd.read_csv(file,sep=",",index_col="SNo") 

 

# Per queste analisi non ci servono le colonne Latitude e Longitude 

covid_regioni=covid_regioni.drop(["Latitude","Longitude"],axis=1) 

 

# Rendere in formato data le date 

covid_regioni["Date"]=pd.to_datetime(covid_regioni["Date"]) 

covid_regioni['Mese'] = covid_regioni['Date'].dt.month 

 

# Aggregazione dati per giorno 

dati_italia=covid_regioni.groupby("Date").sum() 

 

# Grafico temporale del 2020 in Italia relativo ai positivi giornalieri Covid-19 

plt.figure(figsize=(13,6))  

sns.lineplot(dati_italia,x="Date",y="NewPositiveCases")  

plt.title("Grafico temporale dei nuovi positivi giornalieri in Italia Covid-19")  

plt.show() 

 

# Aggregazione dati nuovi positivi per mese fino al 6 Dicembre 2020 

covid_regioni['mese'] = covid_regioni['Date'].dt.to_period('M')  

somma_per_mese = covid_regioni.groupby('mese')['NewPositiveCases'].sum().reset_index() 

 

# Progressione temporale (per mese) casi positivi Covid-19 

plt.plot(somma_per_mese['mese'].astype(str), somma_per_mese['NewPositiveCases'], marker='o')  

plt.xticks(rotation=45)  

plt.title("Progressione temporale (per mese) casi positivi Covid-19") 

plt.show()  

 

# Trovare il numero totale di morti in Italia fino al 6 Dicembre 2020  

tot_morti=covid_regioni.groupby(["RegionName"])["Deaths"].max().sum()  

print(f"Il numero totale di morti in Italia fino al 6 Dicembre 2020 è di {tot_morti}")  

 

# Trovare il numero totale di positivi in Italia fino al 6 Dicembre 2020  

tot_positivi=covid_regioni.groupby(["Country"])["NewPositiveCases"].sum().reset_index()  

total_positive_cases=covid_regioni.groupby(["RegionName"])["TotalPositiveCases"].max().reset_index()  

print(f"Il numero totale di positivi in Italia fino al 6 Dicembre 2020 è di\n{tot_positivi["NewPositiveCases"].sum()} (prendendo la colonna \'NewPositiveCases\')\n{total_positive_cases["TotalPositiveCases"].sum()} (prendendo la colonna \'TotalPositiveCases\')")  

 

# Trovare il numero totale di guariti in Italia fino al 6 Dicembre 2020 

tot_guariti=covid_regioni.groupby(["RegionName"])["Recovered"].max().sum()  

print(f"Il numero totale di guariti in Italia fino al 6 Dicembre 2020 è di {tot_guariti}") 

 

# Variazione giornaliera positivi Covid-19 

somma_positivi_per_giorno = covid_regioni.groupby('Date')['NewPositiveCases'].sum() 

incremento_giornalierio = somma_positivi_per_giorno.diff().reset_index() 

print(incremento_giornalierio) 

plt.figure(figsize=(13, 6)) 

sns.lineplot(data=incremento_giornalierio, x='Date', y='NewPositiveCases', label='Variazione casi positivi') 

plt.title("Variazione giornaliera positivi Covid-19") 

plt.show() 

 

# Variazione mensile positivi Covid-19 fino al 6 Dicembre 2020 

somma_positivi_per_mese = covid_regioni.groupby('Mese')['NewPositiveCases'].sum() 

incremento_mensile = covid_regioni['Incremento'] = somma_positivi_per_mese.diff() 

print(incremento_mensile) 

 

# Raggruppiamo i numeri di positivi per provincia (prendendo i massimi della colonna "TotalPositiveCases" perchè quest'ultima ha valori progressivi) 

max_per_provincia = covid_province.groupby('ProvinceName')['TotalPositiveCases'].max().sort_values(ascending = True) 

print(max_per_provincia) 

# Maggior e minor numero di casi di covid per provincia nel 2020 

max_assoluto_province = max_per_provincia.max() 

nome_province_max = max_per_provincia.idxmax() 

min_assoluto_province = max_per_provincia.min() 

nome_province_min = max_per_provincia.idxmin() 

print(f"La provincia che ha il maggior numero di casi nel 2020 è quella di {nome_province_max}, con {max_assoluto_province} casi") 

print(f"La provincia che ha il minor numero di casi nel 2020 è quella di {nome_province_min}, con {min_assoluto_province} casi") 

 

# Media, mediana e quantili dei positivi Covid-19 per provincia 

# Media 

media_provincia = max_assoluto_province.mean() 

print(f'La media dei casi di Covid19 per provincia è {media_provincia}') 

# Mediana   

mediana_provincia = max_per_provincia.median() 

print(f'La mediana dei positivi Covid19 per provincia è {mediana_provincia}') 

# Quartile 0.25 

primo_quartile = max_per_provincia.quantile(q= 0.25) 

print(f"Il primo quartile (0.25) corrisponde a {primo_quartile}") 

# Quartile 0,75 

terzo_quartile = max_per_provincia.quantile(q= 0.75) 

print(f"Il terzo quartile (0.75) corrisponde a {terzo_quartile}") 

 

# Grafico Boxplot della distribuzione dei positivi nelle Province 

plt.figure(figsize=(7,7)) 

sns.boxplot(max_per_provincia) 

plt.title("Distribuzione numeri massimi di positivi Covid-19 delle diverse province") 

plt.xlabel("Province italiane") 

plt.show() 

 

# Raggruppare i nuovi positivi per regione nel 2020 

somma_positivi_regioni=covid_regioni.groupby(["RegionName"])["NewPositiveCases"].sum().reset_index().set_index("RegionName") 

print(somma_positivi_regioni) 

 

# La regione con meno casi nuovi nell'arco del 2020 

nome_regione_min=somma_positivi_regioni.idxmin() 

regione_min=somma_positivi_regioni.min() 

print(f"La regione con meno nuovi positivi nell'arco del 2020 è:\n{nome_regione_min}\nnumero di casi:\n{regione_min}") 

 

# Troviamo la regione con più casi nuovi nell'arco del 2020 

nome_regione_max=somma_positivi_regioni.idxmax() 

regione_max=somma_positivi_regioni.max() 

print(f"La regione con più nuovi positivi nell'arco del 2020 è:\n{nome_regione_max}\nnumero di casi:\n{regione_max}") 

 

# Numero medio di nuovi casi nell'arco del 2020 per regione   

media_regioni=somma_positivi_regioni.mean()  

print(f"Il numero medio di nuovi casi nell'arco del 2020 è:\n{media_regioni}")  

 

# Regione mediana tra i nuovi casi suddivisi per ogni regione (riga scritta più per controllo che per output) 

mediana_regioni=somma_positivi_regioni.sort_values(by="NewPositiveCases",ascending=True).median() 

# Trovare l'indice della mediana 

indice_mediana_regioni=(len(somma_positivi_regioni)-1)/2 

# Ordinare la tabella somma_positivi_regioni in ordine crescente per numero di positivi 

ordinamento_regioni=somma_positivi_regioni.sort_values(by="NewPositiveCases",ascending=True).reset_index() 

# Trovare il nome della regione per la quale il valore risulta essere la mediana 

nome_mediana_regioni=ordinamento_regioni.iloc[int(indice_mediana_regioni),0] 

valore_mediana_regioni=ordinamento_regioni.iloc[int(indice_mediana_regioni),1] 

print(f"La regione mediana della tabella con i nuovi casi suddivisa per regione è:\n{nome_mediana_regioni} con un valore di {valore_mediana_regioni} nuovi casi")  

 

# Grafico temporale giornaliero dei nuovi positivi per ogni regione nel 2020 

plt.figure(figsize=(13,6))  

sns.lineplot(covid_regioni,x="Date",y="NewPositiveCases",hue="RegionName")  

plt.legend(ncol=2)  

plt.title("Grafico temporale dei nuovi positivi per ogni regione")  

plt.show() 

 

# Grafico a barre suddiviso per regione del numero totale dei positivi fino al 6 Dicembre 2020 

somma_positivi_regioni=somma_positivi_regioni.reset_index() 

plt.figure(figsize=(10, 6)) 

plt.bar(somma_positivi_regioni["RegionName"], somma_positivi_regioni["NewPositiveCases"], color='g') 

plt.title('Totale positivi Covid-19 suddivisi per regione') 

plt.xlabel('Regione') 

plt.ylabel('Totale positivi') 

plt.xticks(rotation=45, ha="right") 

plt.subplots_adjust(bottom=0.20) 

plt.show() 

 

# il totale delle terapie intensive per regione 

terapie_intensive_per_regione=covid_regioni.groupby("RegionName")["IntensiveCarePatients"].max() 

 

# regione con piu terapie intensive 

valore_massimo = terapie_intensive_per_regione.max() 

regione_valore_massimo = terapie_intensive_per_regione.idxmax() 

print("La regione con più posti occupati in terapia intensiva è" , regione_valore_massimo, "con", valore_massimo) 

  

# Regione con meno terapie intensive 

valore_minimo= terapie_intensive_per_regione.min() 

regione_valore_minimo= terapie_intensive_per_regione.idxmin() 

print("La regione con meno posti occupati in terapia intensiva è", regione_valore_minimo,"con", valore_minimo,"posti occupati") 

media = terapie_intensive_per_regione.mean() 

print(f"La media dei posti occupati in terapia intensiva in Italia è {media}") 

statistiche= terapie_intensive_per_regione.describe() 

print(statistiche) 

# ordiniamo i dati e poi ci calcoliamo la mediana 

terapie_intensive_per_regione = terapie_intensive_per_regione 

median = np.median(terapie_intensive_per_regione.sort_values()) 

print("Mediana:", median) 

 

# Grafico giornaliero terapie intensive nel 2020 in Italia 

plt.figure(figsize=(13,6))  

sns.lineplot(dati_italia,x="Date",y="IntensiveCarePatients")  

plt.title("Grafico temporale del numero giornaliero di posti occupati in terapia intensiva in Italia")  

plt.show() 

 

 

# Raggruppiamo i dati per regione e per mese, sommando i posti di terapia intensiva 

terapia_intensiva_regioni_mesi = covid_regioni.groupby(["RegionName", "Mese"])["IntensiveCarePatients"].max().reset_index() 

 

# Grafico terapie intensive nel 2020 per mese e per regione 

plt.figure(figsize=(13, 6)) 

sns.lineplot(terapia_intensiva_regioni_mesi, x= 'Mese' , y ='IntensiveCarePatients', hue = 'RegionName') 

plt.title("Posti occupati in terapia intensiva nel 2020 suddivisi per mese e per regione") 

plt.legend(ncol=2) 

plt.show() 

 

# Rapporto morti/positivi per covid 

regioni_morti=covid_regioni.groupby(["RegionName"])["Deaths"].max().reset_index().set_index("RegionName") 

somma_positivi_regioni=somma_positivi_regioni.set_index("RegionName") 

rapporto_positivi_morti=somma_positivi_regioni["NewPositiveCases"]/regioni_morti["Deaths"] 

print(rapporto_positivi_morti) 

 

# Rapporto percentuale tra numero positivi e abitanti per regione 

 

# importiamo il file excel che contiene la popolazione del 2020 (preso dal istat),  

# se può essere utile, il link per scaricare il file excel è questo: https://1drv.ms/x/s!AiUcVo4trr2Jh0lBTRWN3SLAim2t?e=lNj54B 

popolazione = pd.read_excel('./Popolazione_2020_per_regione.xlsx') 

popolazione2020= popolazione.sort_values(by='RegionName') 

 

# Uniamo le due tabelle somma_positivi_regioni e popolazione2020 

tabella_positivi_abitanti= pd.merge(somma_positivi_regioni, popolazione2020, on='RegionName', how='right') 

 

 

# Per calcolare l'incidenza positivi/abitanti abbiamo due modi: creare una nuova tabella oppure creare una nuova colonna nella tabella preesistente. 

 

# Metodo 1: calcoliamo la percentuale di incidenza creando una nuova tabella 

 

incidenza_positivi= tabella_positivi_abitanti['NewPositiveCases'] / tabella_positivi_abitanti['Abitanti'] *100 

colonnaRegioni = tabella_positivi_abitanti[['RegionName']] 

tabella_incidenza_positivi = pd.concat([colonnaRegioni,incidenza_positivi], axis=1 )  

print(tabella_incidenza_positivi) 

 

# Metodo 2: aggiungiamo una colonna alla tabella unita (tabella_positivi_abitanti) con i valori calcolati al suo interno 

tabella_positivi_abitanti['Rapporto Abitanti/Positivi'] = round((tabella_positivi_abitanti['NewPositiveCases']/tabella_positivi_abitanti['Abitanti']*100), 2)  

print(tabella_positivi_abitanti) 

 

# Raggruppamento dati totali progressivi positivi in Italia e dei dati totali progressivi test, entrambi suddivisi per regione  

test_progressivi_regioni= covid_regioni.groupby(["RegionName"])[["TotalPositiveCases","TestsPerformed"]].max().reset_index() 

print(test_progressivi_regioni) 

 

# Grafico totale progressivo dei tamponi fatti, suddivisi per regione 

plt.figure(figsize=(13,6)) 

plt.bar(test_progressivi_regioni.sort_values(by="TestsPerformed",ascending=False)["RegionName"],height=test_progressivi_regioni.sort_values(by="TestsPerformed",ascending=False)["TestsPerformed"]) 

plt.title("N° di tamponi fatti suddiviso per regione") 

plt.xticks(rotation=45, ha="right") 

plt.subplots_adjust(bottom=0.20) 

plt.show() 

 

# Rapporto fra positivi e test eseguiti 

test_progressivi_regioni["Rapporto positivi/test"]=test_progressivi_regioni["TotalPositiveCases"]/test_progressivi_regioni["TestsPerformed"] 

print(test_progressivi_regioni.sort_values(by="TestsPerformed",ascending=False)) 

 

# Grafico rapporto tra n° di positivi e n° di tamponi fatti suddiviso per regione 

plt.figure(figsize=(13,6)) 

plt.bar(test_progressivi_regioni.sort_values(by="Rapporto positivi/test",ascending=False)["RegionName"],height=test_progressivi_regioni.sort_values(by="Rapporto positivi/test",ascending=False)["Rapporto positivi/test"]) 

plt.title("Rapporto tra n° di positivi e n° di tamponi fatti suddiviso per regione") 

plt.xticks(rotation=45, ha="right") 

plt.subplots_adjust(bottom=0.20) 

plt.show() 

 

# Vogliamo calcolare l'incidenza dei posti totali di terapia intensiva per regione con la popolazione regionale 

 

# Incidenza delle terapie intensive sui positivi per regione 

incidenza_terapie_intensive = round(((terapie_intensive_per_regione/somma_positivi_regioni["NewPositiveCases"])*100),2) 

print(incidenza_terapie_intensive) 

 

# Raggruppamento dati della terapia intensiva per mese e per regione 

terapia_intensiva_regioni_mesi = covid_regioni.groupby(["RegionName", "Mese"])["IntensiveCarePatients"].max().reset_index()  

print(terapia_intensiva_regioni_mesi) 

 

 

# Creo nuova tabella da covid_regioni per ottenere soltanto le colonne Date, RegionName e TotalHospitalizedPatients 

selezione_colonne = ['Date', 'RegionName', 'TotalHospitalizedPatients']  

new_tab = covid_regioni[selezione_colonne]  

 

# La data con il maggior numero di persone ricoverate in ospedale per ogni regione  

indice_max_ospedalizzati = new_tab.groupby("RegionName")["TotalHospitalizedPatients"].idxmax()  

massimo_per_regione = new_tab.loc[indice_max_ospedalizzati]  

massimo_per_regione = massimo_per_regione.sort_values(by="Date",ascending=True).set_index('Date')  

print(massimo_per_regione) 

 

# Numero totale nel 2020 di test fatti per ogni regione  

test_totali_regioni = covid_regioni.groupby("RegionName")["TestsPerformed"].max().sum()  

print(f"In tutta Italia sono stati eseguiti fino al 6 Dicembre {test_totali_regioni} test") 

 

# Creazione tabella dei test progressivi in Italia suddivisi per mese  

test_progressivi_regioni= covid_regioni.groupby(["RegionName","Mese"])["TestsPerformed"].max().reset_index() 

print(test_progressivi_regioni) 

test_progressivi= test_progressivi_regioni.groupby("Mese")["TestsPerformed"].sum().reset_index()  

print(test_progressivi) 

 

# Grafici temporali Italia combinati (ospedalizzati, terapia intensiva e quarantenati) 

plt.figure(figsize=(13,6)) 

sns.lineplot(dati_italia,x="Date",y="TotalHospitalizedPatients",label="Persone ricoverate") 

sns.lineplot(dati_italia,x="Date",y="IntensiveCarePatients",label="Persone in terapia intensiva") 

sns.lineplot(dati_italia,x="Date",y="HomeConfinement",label="Persone in quarantena") 

plt.title("Grafici temporali combinati dati italiani") 

plt.show() 

 

 

#creazione tabella dei totali progressivi positivi in Italia suddivisi per regione e per mese 

totali_progressivi_regioni= covid_regioni.groupby(["RegionName","Mese"])["TotalPositiveCases"].max().reset_index() 

totali_progressivi= totali_progressivi_regioni.groupby("Mese")["TotalPositiveCases"].sum().reset_index() 

print(totali_progressivi) 

 

# Grafico numero progressivo di positivi e numero progressivo dei test effettuati in Italia 

plt.figure(figsize=(6, 4)) 

sns.lineplot(test_progressivi, x="Mese", y="TestsPerformed", label = "Test Progressivi") 

sns.lineplot(totali_progressivi, x="Mese", y="TotalPositiveCases", label = "Totale Positivi") 

plt.title("Andamento totale tamponi e totale positivi") 

plt.show() 