from flask import render_template
import psycopg2



config = {
    "db_host": "localhost",
    "db_database": "iot",
    "db_user": "postgres",
    "db_password": "postgres"
}


def get_recent_data():

    conn = psycopg2.connect(
        host=config["db_host"], 
        database=config["db_database"], 
        user=config["db_user"], 
        password=config["db_password"]
    )
    cur = conn.cursor()
    cur.execute("SELECT temperatura, umidade FROM dados_sensor ORDER BY data_hora DESC LIMIT 10")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return row[0], row[1]
    else:
        return None, None

def create_dashboard(app):

    @app.route('/')
    def dashboard():
        temperatura, umidade = get_recent_data()
        if temperatura is not None and umidade is not None:
            return render_template('dashboard.html', temperatura=temperatura, umidade=umidade)
        else:
            return render_template('dashboard.html', erro='Nenhum dado disponível.')