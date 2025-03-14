from fastapi import status

def test_get_post_by_id(test_client, setup_test_data):
    post_id = setup_test_data.id
    response = test_client.get(f"/posts/{post_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == post_id




def test_get_statistics(test_client, setup_test_data):
    post_date = setup_test_data.date.split(" ")[0].replace("/", "-")
    response = test_client.get(f"/statistics?post_date={post_date}")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert "post_total" in response.json()
        assert response.json()["post_total"] == 1


def test_create_post(test_client, db_session):

    post = {
        "board_name": "board_name for testing",
        "title": "New Test Post",
        "link": "https://newtestpost.com/",
        "author_ptt_id": "author_ptt_id for testing",
        "date": "2024-10-08T12:34:10",
        "author_nickname": "author_nickname for testing",
        "content": "New test content"
    }

    response = test_client.post("/api/posts", json=post)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == post['title']


def test_update_post(test_client, setup_test_data):
    post_id = setup_test_data.id
    updated_post = {
        "board_name": "board_name for testing",
        "title": "Updated Title",
        "link": "https://updatedlink.com/",
        "author_ptt_id": "author_ptt_id for testing",
        "date": "2024-10-08T12:34:10",
        "author_nickname": "author_nickname for testing",
        "content": "Updated content"
    }
    response = test_client.put(f"/api/posts/{post_id}", json=updated_post)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Title"
#


def test_get_posts(test_client, setup_test_data):
    response = test_client.get("/posts")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["id"] == 1
#
    response = test_client.get("/posts", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
#
    response = test_client.get("/posts", params={"offset": 1})
    assert response.status_code == status.HTTP_200_OK
#
    response = test_client.get("/posts", params={"board_name": "board_name for testing"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["board_id"] == 1
#
    response = test_client.get("/posts", params={"author_ptt_id": "author_ptt_id for testing"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["author_id"] == 1
#

    response = test_client.get("/posts", params={"start_date": "2024-10-08", "end_date": "2024-10-08"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
#
    response = test_client.get("/posts", params={"board_name": "non_existent_board"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = test_client.get("/posts", params={'start_date':"1998-10-08", "end_date":"1998-10-08"})
    assert len(response.json()) == 0

def test_delete_post(test_client, setup_test_data):
    post_id = setup_test_data.id
    response = test_client.delete(f"/delete/{post_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "文章刪除成功"


    response = test_client.get(f"/delete/{post_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED