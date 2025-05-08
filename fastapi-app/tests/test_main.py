import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app, save_todos, TodoItem

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # 테스트 전 초기화 및 후처리로 항상 빈 상태 유지
    save_todos([])
    yield
    save_todos([])

def test_get_todos_empty():
    # To-Do 항목이 비어있을 때 GET 요청 결과가 빈 리스트인지 확인
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_get_todos_with_items():
    # 미리 항목을 저장한 후, GET 요청으로 불러오는지 테스트
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False, due_date="2025-04-06", importance : "medium")
    save_todos([todo.dict()])
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test"

def test_create_todo():
    # POST 요청으로 To-Do 항목을 추가하고 응답을 확인
    todo = {
        "id": 1,
        "title": "Test",
        "description": "Test description",
        "completed": False,
        "due_date": "2025-04-06",
        "importance" : "medium"
    }
    response = client.post("/todos", json=todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Test"

def test_create_todo_invalid():
    # 필수 필드가 누락된 잘못된 요청에 대해 422 오류 확인
    todo = {"id": 1, "title": "Test"}  # description, completed, due_date 누락
    response = client.post("/todos", json=todo)
    assert response.status_code == 422  # validation error

def test_update_todo():
    # 기존 항목을 PUT 요청으로 업데이트 후 값 변경 확인
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False, due_date="2025-04-06", importance="medium")
    save_todos([todo.dict()])
    updated_todo = {
        "id": 1,
        "title": "Updated",
        "description": "Updated description",
        "completed": True,
        "due_date": "2025-05-01",
        "importance" : "medium"
    }
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["completed"] is True

def test_update_todo_not_found():
    # 존재하지 않는 항목을 수정할 경우 404 반환 확인
    updated_todo = {
        "id": 1,
        "title": "Updated",
        "description": "Updated description",
        "completed": True,
        "due_date": "2025-05-01",
        "importance" : "medium"
    }
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 404

def test_delete_todo():
    # 존재하는 항목을 삭제하고 응답 메시지 확인
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False, due_date="2025-04-06", importance : "medium")
    save_todos([todo.dict()])
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "To-Do item deleted"

def test_delete_todo_not_found():
    # 존재하지 않는 항목 삭제 시 404 반환 확인
    response = client.delete("/todos/1")
    assert response.status_code == 404

def test_get_progress_no_todos():
    # 항목이 없을 때 진행률이 0/0인지 확인
    response = client.get("/progress")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "completed": 0, "progress": "0/0"}

def test_get_progress_with_todos():
    # 완료된 항목이 있는 경우, 진행률 계산이 올바른지 테스트
    todos = [
        {"id": 1, "title": "A", "description": "desc", "completed": True, "due_date": "2025-04-06", "importance" : "medium"},
        {"id": 2, "title": "B", "description": "desc", "completed": False, "due_date": "2025-04-10", "importance" : "medium"},
    ]
    save_todos(todos)
    response = client.get("/progress")
    assert response.status_code == 200
    assert response.json() == {"total": 2, "completed": 1, "progress": "1/2"}
