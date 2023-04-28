import psycopg2, os, requests, json, io
from time import time

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)


conn = psycopg2.connect(
    database=os.environ.get("POSTGRES_NAME", "postgres"), 
    user=os.environ.get("POSTGRES_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD", "postgres"), 
    host=os.environ.get("POSTGRES_HOST", "localhost"), 
    port=int(os.environ.get("POSTGRES_PORT", "5432"))
)

print('DB CONNECTED')

BLOCKED_URL_LISTS = ['favicon.ico',]

@app.route('/')
def hello():
    return 'Flask(WEB PROXY) Server is Running....'


@app.route('/test/<path:endpoint_path>')
@limiter.limit("1 per minute")
def test_api_requests(endpoint_path):
    return endpoint_path


@app.route('/<path:endpoint_path>')
def handle_api_requests(endpoint_path):
    """
    CHECKED BLOCKED URLS FIRST
    CHECK AAAS-TOKEN EXISTS
    DB QUERY TO FETCH BASE_URL & NO_OF_REQUESTS_LEFT
    CHECK IF REQUESTS AVAILABLE
    EXECUTE THE REQUEST TO SELLER SERVER
    DB QUERY TO DECREASE NUMBER OF REQUEST
    RETURN SELLER SERVER RESPONSE
    """
    if endpoint_path in BLOCKED_URL_LISTS:
        return "BLOCKED URL"
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
                "ApiService" APIS ON(P.id=APIS.product_id)
            WHERE token = '{token}';
        """)
        try:
            data = c.fetchall()[0]
            base_url = data[8]
        except Exception as e:
            print(e)
            return f"INVALID AAAS-TOKEN"
        print(data)
        if data[2] > 0:
            r = requests.get(
                base_url+endpoint_path,
            )
            c.execute(f"""
            UPDATE "ClientPackages"
            SET normal_requests_left = {data[2]-1}
            WHERE token = '{token}';
            """)
            conn.commit()
            print(time() - t)
            return (json.loads(r.content), r.status_code)
        else:
            return f"No Requests Available. Please Reactivate the package."
    else:
        return f"NO TOKEN FOUND"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)