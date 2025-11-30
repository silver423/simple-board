// 백엔드 API의 기본 주소 (로컬 테스트 시)
// const API_BASE_URL = 'http://localhost:5000/api/posts';

// 변경 후: 상대 주소 (Nginx가 /api/를 백엔드로 전달함)
const API_BASE_URL = '/api/posts';

// 1. 목록 조회 및 화면 갱신 (READ)
async function loadPosts() {
    try {
        const response = await fetch(API_BASE_URL);
        const posts = await response.json();

        const listElement = document.getElementById('post-list');
        listElement.innerHTML = ''; // 기존 목록 초기화

        if (posts.length === 0) {
             listElement.innerHTML = '<p>게시글이 없습니다. 작성해주세요.</p>';
             return;
        }

        posts.forEach(post => {
            // 게시글 HTML 요소 생성
            const postDiv = document.createElement('div');
            postDiv.className = 'post-item';
            postDiv.innerHTML = `
                <p><strong>[ID: ${post.id}] ${post.title}</strong></p>
                <p>${post.content}</p>
                
                <div style="margin-top: 10px;">
                    <div style="margin-bottom: 5px;">
                        <input type="text" id="edit-title-${post.id}" placeholder="수정 제목" value="${post.title}" style="width: 400px; padding: 5px;">
                    </div>
                    
                    <div>
                        <textarea id="edit-content-${post.id}" placeholder="수정 내용" style="width: 400px; height: 50px; padding: 5px; resize: vertical; box-sizing: border-box;">${post.content}</textarea>
                    </div>
                    
                    <div style="margin-top: 5px;">
                        <button onclick="handleUpdate(${post.id})">수정</button>
                        <button onclick="handleDelete(${post.id})">삭제</button>
                    </div>
                </div>
            `;
            listElement.appendChild(postDiv);
        });

    } catch (error) {
        console.error('Error fetching posts:', error);
        document.getElementById('post-list').innerHTML = '<p>게시글 로드 실패. 백엔드 서버를 확인하세요.</p>';
    }
}

// 2. 게시글 작성 (CREATE)
async function handleCreate() {
    const title = document.getElementById('new-title').value;
    const content = document.getElementById('new-content').value;

    if (!title || !content) {
        alert("제목과 내용을 입력해주세요.");
        return;
    }

    await fetch(API_BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    });

    // 입력 필드 초기화 및 목록 갱신
    document.getElementById('new-title').value = '';
    document.getElementById('new-content').value = '';
    loadPosts(); 
}

// 3. 게시글 수정 (UPDATE)
async function handleUpdate(postId) {
    const title = document.getElementById(`edit-title-${postId}`).value;
    const content = document.getElementById(`edit-content-${postId}`).value;

    await fetch(`${API_BASE_URL}/${postId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    });

    loadPosts(); 
}

// 4. 게시글 삭제 (DELETE)
async function handleDelete(postId) {
    if (!confirm(`${postId}번 게시글을 정말로 삭제하시겠습니까?`)) {
        return;
    }

    await fetch(`${API_BASE_URL}/${postId}`, {
        method: 'DELETE'
    });

    loadPosts();
}

// 페이지 로드 시 초기 실행
window.onload = loadPosts;
