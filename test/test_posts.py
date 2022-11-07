from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts_map = list(map(lambda x: schemas.PostOut(**x), res.json()))
    
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/988888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "assrfelsnjv"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/posts/8000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user2, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 200
    assert res.json()['title'] == data['title']
    assert res.json()['content'] == data['content']

def test_update_other_user_post(authorized_client, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
    
