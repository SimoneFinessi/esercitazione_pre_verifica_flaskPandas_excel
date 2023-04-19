from flask import Flask, render_template, request,Response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
import io
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

@app.route('/es3', methods=['POST'])
def es3():
    trovato=df.groupby("state").count()[["customer_id"]].to_html()
    return render_template('risultato.html',lista=trovato)

@app.route('/es4', methods=['POST'])
def es4():
    trovato=df.groupby("state").count()[["customer_id"]]
    massimo=trovato[trovato["customer_id"]==trovato["customer_id"].max()].to_html()
    return render_template('risultato.html',lista=massimo)

@app.route('/es5', methods=['POST'])
def es5():
    return render_template('risultato_immagini.html')

@app.route("/immagine1")
def immagine1():
    stat=df.groupby("state").count()[["customer_id"]]
    fig,ax =plt.subplots()
    ax.bar(stat.index,stat["customer_id"])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
   
@app.route("/immagine2")
def immagine2():
    stat=df.groupby("state").count()[["customer_id"]]
    fig,ax =plt.subplots()
    ax.barh(stat.index,stat["customer_id"])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/immagine3")
def immagine3():
    stat=df.groupby("state").count()[["customer_id"]]
    fig,ax =plt.subplots()
    ax.pie(stat["customer_id"], labels = stat.index)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)