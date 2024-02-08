from flask import Flask, request, jsonify
import psycopg2
from backend import create_dashboard, config

app = Flask(__name__)


conn = psycopg2.connect(
        host=config["db_host"], 
        database=config["db_database"], 
        user=config["db_user"], 
        password=config["db_password"]
    )


@app.route('/get-sensor-data', methods=['GET'])
def post_data():
    print("Requisição recebida")
    temperatura = request.args.get('temperatura')
    umidade = request.args.get('umidade')

    if temperatura is not None and umidade is not None:
        try:
            temperatura = float(temperatura)
            umidade = float(umidade) 

            cur = conn.cursor()
            cur.execute("INSERT INTO dados_sensor (temperatura, umidade) VALUES (%s, %s)", (temperatura, umidade))
            conn.commit()
            cur.close()

            return jsonify({'sucesso': True}), 200
        except (ValueError, psycopg2.DatabaseError) as e:
            return jsonify({'erro': 'Requisição Inválida', 'mensagem': str(e)}), 400
    else:
        return jsonify({'erro': 'Dados Ausentes', 'mensagem': 'Temperatura e Umidade precisam ser solicitadas'}), 400

@app.route('/latest-sensor-data', methods=['GET'])
def latest_sensor_data():
    cur = conn.cursor()
    cur.execute("SELECT temperatura, umidade, data_hora FROM dados_sensor ORDER BY data_hora DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()

    if rows:
        temperatura = [row[0] for row in rows]
        umidade = [row[1] for row in rows]
        data_hora = [row[2].strftime("%Y-%m-%dT%H:%M:%S.%fZ") for row in rows]  # Formato ISO 8601

        return jsonify({'temperatura': temperatura, 'umidade': umidade, 'categorias': data_hora}), 200
    else:
        return jsonify({'erro': 'Nenhum dado disponível'}), 404

create_dashboard(app) 

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)