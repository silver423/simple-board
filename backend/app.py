from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os 
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

# --- 기본 설정 및 데이터 ---
app = Flask(__name__)
CORS(app)

# SQLite 설정: 컨테이너 내부의 /app/instance/app.db 파일에 저장
# instance 폴더는 Docker Volume을 통해 호스트에 영구 저장됩니다.
DB_DIR = '/app/data'
DB_PATH = os.path.join(DB_DIR, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------------------------------
# SQLAlchemy 모델 정의
# -----------------------------------------------------
class Post(db.Model):
    # 자동으로 테이블 이름은 'post'로 설정됨
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        # API 응답을 위한 딕셔너리 변환 메서드
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }

# --- 모니터링 설정 ---
REQUESTS = Counter('simple_app_requests_total', 'Total HTTP requests', ['method','endpoint'])

@app.before_request
def before():
    REQUESTS.labels(method=request.method, endpoint=request.path).inc()

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# --- API 엔드포인트: 데이터베이스 연동으로 변경 ---

# 1. 목록 조회 (READ ALL)
@app.route("/api/posts", methods=["GET"])
def get_posts():
    # 데이터베이스에서 모든 게시글을 조회
    all_posts = Post.query.all()
    # 딕셔너리 리스트로 변환하여 JSON 응답
    return jsonify([post.to_dict() for post in all_posts])

# 2. 게시글 생성 (CREATE)
@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json() 
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content are required."}), 400
    
    # 새 Post 객체 생성 및 DB에 추가
    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({"message": "Post created", "post": new_post.to_dict()}), 201

# 3. 게시글 수정 (UPDATE)
@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    # ID로 게시글 조회
    post = Post.query.get(post_id)
    
    if post is None:
        return jsonify({"error": "Post not found"}), 404
        
    # 데이터 업데이트 및 DB에 반영
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()
    
    return jsonify({"message": f"Post {post_id} updated", "post": post.to_dict()})

# 4. 게시글 삭제 (DELETE)
@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    if post is None:
        return jsonify({"error": "Post not found"}), 404
        
    # DB에서 삭제 및 반영
    db.session.delete(post)
    db.session.commit()
        
    return jsonify({"message": f"Post {post_id} deleted"}), 200

# 서버 실행 전 DB 초기화 및 테이블 생성
with app.app_context():
    # 데이터베이스 파일이 저장될 디렉토리 생성 (Docker Volume 매핑 경로)
    os.makedirs(DB_DIR, exist_ok=True) 
    # 테이블 생성 (이미 존재하면 건너뜀)
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
