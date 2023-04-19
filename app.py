from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name="customers")

app = Flask(__name__)

@app.route('/')
def home():
    lista=list(set(list(df['city'])))
    return render_template('home.html',list=lista)

@app.route('/es1', methods=['POST'])
def es1():
    nome=request.form["nome"]
    cognome=request.form["cognome"]
    trovato=df[(df['first_name'].str.lower()==nome.lower())&(df['last_name'].str.lower()==cognome.lower())].to_html()
    return render_template('risultato.html',lista=trovato)

@app.route('/es2/<cit>')
def es2(cit):
    trovato=df[df['city'].str.lower()==cit.lower()].to_html()
    return render_template('risultato.html',lista=trovato)
    
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)