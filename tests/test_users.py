import pytest

USER_REGISTER_DATA = {"email": "prueba@gmail.com",
                      "phone_number": "+123123123",
                      "image_location": "https://duckduckgo.com/assets/common/dax-logo.svg",
                      "display_name": "Probador de Pruebas"}

USER2_REGISTER_DATA = {"email": "marcos@gmail.com",
                       "phone_number": "+999999999999999",
                       "image_location": "https://duckduckgo.com/assets/common/dax-logo.svg",
                       "display_name": "Marcos Marcos"}


def test_register(testapp):
    r = testapp.post('/users', json=USER_REGISTER_DATA,
                     headers={'x-access-token': '1'})

    data = r.get_json()

    assert r.status_code == 201
    assert data["id"] == 1

    for k in USER_REGISTER_DATA.keys():
        assert data[k] == USER_REGISTER_DATA[k]


def test_register2(testapp):
    r = testapp.post('/users', json=USER2_REGISTER_DATA,
                     headers={'x-access-token': '2'})

    data = r.get_json()

    assert r.status_code == 201
    assert data["id"] == 2

    for k in USER2_REGISTER_DATA.keys():
        assert data[k] == USER2_REGISTER_DATA[k]


def test_cant_register_without_token(testapp):
    r = testapp.post('/users', json=USER_REGISTER_DATA)

    assert r.status_code == 400


def test_error_if_missing_field1(testapp):
    r = testapp.post('/users', json={"email": "prueba@gmail.com",
                                     "phone_number": "+123123123",
                                     "image_location": "https://duckduckgo.com/assets/common/dax-logo.svg"}, headers={'x-access-token': '1'})

    assert r.status_code == 400


def test_error_if_missing_field2(testapp):
    r = testapp.post('/users', json={"phone_number": "+123123123",
                                     "image_location": "https://duckduckgo.com/assets/common/dax-logo.svg"}, headers={'x-access-token': '1'})

    assert r.status_code == 400


def test_error_if_missing_field3(testapp):
    r = testapp.post('/users', json={"phone_number": "+123123123",
                                     "email": "prueba@protonmail.com"}, headers={'x-access-token': '1'})

    assert r.status_code == 400


def test_non_existant(testapp):

    r = testapp.get('/users/1123123', headers={'x-access-token': '1'})

    assert r.status_code == 404


def test_get_my_info(testapp):

    r = testapp.get('/users/1', headers={'x-access-token': '1'})

    data = r.get_json()

    assert r.status_code == 200
    assert data["id"] == 1

    for k in USER_REGISTER_DATA.keys():
        assert data[k] == USER_REGISTER_DATA[k]


def test_modify_my_info_name(testapp):

    r = testapp.patch(
        '/users/1', json={"display_name": "Carlos"}, headers={'x-access-token': '1'})

    data = r.get_json()

    print(data)

    assert r.status_code == 200
    assert data["display_name"] == "Carlos"
    assert data["image_location"] == "https://duckduckgo.com/assets/common/dax-logo.svg"
    assert data["email"] == "prueba@gmail.com"
    assert data["phone_number"] == "+123123123"
    assert data["id"] == 1


def test_modify_non_existant(testapp):

    r = testapp.patch(
        '/users/123123', json={"display_name": "Carlos"}, headers={'x-access-token': '123123'})

    assert r.status_code == 404


def test_modify_my_info_phone(testapp):

    r = testapp.patch(
        '/users/1', json={"phone_number": "+456"}, headers={'x-access-token': '1'})

    data = r.get_json()

    print(data)

    assert r.status_code == 200
    assert data["display_name"] == "Carlos"
    assert data["image_location"] == "https://duckduckgo.com/assets/common/dax-logo.svg"
    assert data["email"] == "prueba@gmail.com"
    assert data["phone_number"] == "+456"
    assert data["id"] == 1


def test_modify_my_info_mail(testapp):

    r = testapp.patch(
        '/users/1', json={"email": "carlos@protonmail.com"}, headers={'x-access-token': '1'})

    data = r.get_json()

    print(data)

    assert r.status_code == 200
    assert data["display_name"] == "Carlos"
    assert data["image_location"] == "https://duckduckgo.com/assets/common/dax-logo.svg"
    assert data["email"] == "carlos@protonmail.com"
    assert data["phone_number"] == "+456"
    assert data["id"] == 1


def test_cant_edit_others_info(testapp):

    r = testapp.patch(
        '/users/1', json={"email": "carlos@protonmail.com"}, headers={'x-access-token': '2'})

    assert r.status_code == 401


def test_no_videos_uploaded(testapp):
    r = testapp.get('/users/1/videos', headers={'x-access-token': '1'})

    assert r.status_code == 200
    assert r.get_json() == []



'''
{'users': 
    [
        {
            'email': 'carlos@protonmail.com',
            'display_name': 'Carlos', 
            'phone_number': '+456', 
            'image_location': 'https://duckduckgo.com/assets/common/dax-logo.svg', 
            'id': 1
        },
        {
            'email': 'marcos@gmail.com', 
            'display_name': 'Marcos Marcos', 
            'phone_number': '+999999999999999', 
            'image_location': 'https://duckduckgo.com/assets/common/dax-logo.svg', 
            'id': 2
        }
    ]
}
'''

def test_find_users(testapp):
    r = testapp.get('/users', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 2

def test_filter_name(testapp):
    r = testapp.get('/users?name=Carlos', headers={'x-access-token': '1'})

    data = r.get_json()["users"]
    print(data)

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["display_name"] == "Carlos"

def test_filter_incomplete_name(testapp):
    r = testapp.get('/users?name=Car', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["display_name"] == "Carlos"

def test_no_name_match(testapp):
    r = testapp.get('/users?name=NoExistente', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 0

def test_name_with_spaces(testapp):
    r = testapp.get('/users?name=Marcos Mar', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["display_name"] == "Marcos Marcos"

def test_find_by_email(testapp):
    r = testapp.get('/users?email=carlos@protonmail.com', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["display_name"] == "Carlos"

def test_only_exact_email(testapp):
    r = testapp.get('/users?email=carlos@proton', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 0

def test_find_by_phone(testapp):
    # must encode '+' as '%2B'
    r = testapp.get('/users?phone=%2B456', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["display_name"] == "Carlos"

def test_only_exact_phone(testapp):
    r = testapp.get('/users?phone=%2B45', headers={'x-access-token': '1'})

    data = r.get_json()["users"]

    assert r.status_code == 200
    assert len(data) == 0