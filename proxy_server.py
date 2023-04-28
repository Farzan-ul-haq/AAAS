import psycopg2, os, requests, json, io
from time import time

from flask import Flask, request

app = Flask(__name__)

conn = psycopg2.connect(
    database=os.environ.get("POSTGRES_NAME", "postgres"), 
    user=os.environ.get("POSTGRES_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD", "postgres"), 
    host=os.environ.get("POSTGRES_HOST", "localhost"), 
    port=int(os.environ.get("POSTGRES_PORT", "5432"))
)

print('DB CONNECTED')

@app.route('/')
def hello():
    return 'Flask(WEB PROXY) Server is Running....'

@app.route('/<path:endpoint_path>')
def endpoint(endpoint_path):
    t = time()
    token = request.headers.get('aaas-token', "")
    if token:
        c = conn.cursor()
        c.execute(f"""
            SELECT 
                CP.id, CP.token, CP.normal_requests_left, 
                PP.id, PP.title, PP.service_id, P.id, P.title, 
                APIS.base_url 
            FROM 
                "ClientPackages" CP 
            INNER JOIN 
                "ProductPackage" PP ON(CP.package_id = PP.id) 
            INNER JOIN 
                "Product" P ON(PP.service_id=P.id) 
            INNER JOIN 
                "ApiService" APIS ON(P.id=APIS.product_id);
        """)
        try:
            data = c.fetchall()[0]
            base_url = data[8]

        except Exception as e:
            print(e)
            return f"INVALID TOKEN"
        print(time() - t)
        r = requests.get(
            base_url+endpoint_path,
        )
        # print(json.loads(r.content))
        headers = dict(r.headers)
        headers.pop("Transfer-Encoding")
        print(headers)
        return json.loads(r.content), r.status_code
    else:
        return f"NO TOKEN FOUND"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)