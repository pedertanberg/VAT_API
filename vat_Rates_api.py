from datetime import datetime
import csv
import re
import pandas as pd
import flask
from flask import Flask, jsonify, request, make_response
import math

df = pd.read_excel('C:/Users/Bruger Power/Desktop/hello/.vscode/TEDB - VAT Search.xlsx')
#print(df)

nan_value = float("NaN")
df.replace("1", nan_value, inplace=True)
headers = list(df.columns.values)
df = df.fillna(0)
#print(df)

headersWithoutDate = headers[1:42]
country_long=""
length = len(df)
list1=[]
cleanedlist=[]
standard_list=[]
reduced_list =[]

for index,row in df.iterrows():
    country = row["Country"]
    mva_type = row["Type"]
    VAT_rate = row["Rate"]
    reduced_type = row["Category"]
    lenght= len(country)
    country = country[5:lenght]
    if  reduced_type==0:
        #print("Not here")
        temp=[country,VAT_rate,"Standard"]
        standard_list.append(temp)
    elif VAT_rate!="0" or VAT_rate!="EXEMPTED":
        text = str(reduced_type)
        sep = " "
        stripped_type = text.split(sep,1)[0]
        if VAT_rate!="EXEMPTED" and VAT_rate!=0 and VAT_rate!="NOT_APPLICABLE":
            temp=[country,VAT_rate,stripped_type]
        if temp not in reduced_list:
            reduced_list.append(temp)
        

#print(reduced_list)
print(standard_list)


#Instansierer flask (til API hosting)
app = flask.Flask(__name__)
app.config["DEBUG"] = True
#Flask, når dataen skal hostes, skal den sorteres slik som dataen er i listen
app.config['JSON_SORT_KEYS'] = False



@app.route('/FreeVAT', methods=['GET'])
def api_base():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'country' in request.args:
            country = str(request.args['country'])
            print(country)
        else:
            return "Error: No base field provided. Please specify an base."

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []

        #Looper gjennom dataen og finner matchene resultater med vat_number
        for transaction in standard_list:            
            if transaction[0] == country:
                results.append(transaction)

        for transaction in reduced_list:
            if transaction[0] == country:
                if transaction not in results:
                    if transaction[2] not in results:
                        results.append(transaction)
        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(results)

#http://127.0.0.1:5000/VAT/Good_type?goodtype=reduced&country=Belgium
@app.route('/VAT/Good_type', methods=['GET'])
def api_goodtype():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'goodtype' and 'country' in request.args:
            goodtype = str(request.args['goodtype'])
            country = str(request.args['country'])
            print(goodtype)
        else:
            return "Error: No base field provided. Please specify an base."

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []

        #Looper gjennom dataen og finner matchene resultater med vat_number
        if goodtype=="standard":
            for transaction in standard_list:            
                if transaction[0] == country:
                    if transaction not in results:
                        results.append(transaction)
        elif goodtype=="reduced":
            for transaction in reduced_list:
                if transaction[0] == country:
                    if transaction not in results:
                        if transaction[2] not in results:
                            results.append(transaction)
        else:
            results.append("No data to show")
        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(results)
app.run()
