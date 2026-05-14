from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'tasksdb'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASSWORD', 'password123')
    )

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "db-api"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, created_at FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": t[0], "title": t[1], "description": t[2], "created_at": str(t[3])} for t in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id", (data['title'], data.get('description', '')))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "message": "Task created"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
