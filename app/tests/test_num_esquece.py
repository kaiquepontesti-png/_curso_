from app.extensions import db
from app.models.num_esquece import NumEsquece
from app.models.shopping import ShoppingItem, ShoppingList, User


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"NumEsquece" in response.data


def test_register_user_with_cpf_and_password_validation(client):
    response = client.post(
        "/register",
        data={
            "nome": "Maria Souza",
            "email": "maria@email.com",
            "cpf": "123.456.789-09",
            "password": "Abcdef12!",
            "confirm_password": "Abcdef12!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Cadastro realizado com sucesso" in response.data
    assert User.query.count() == 1
    assert User.query.first().cpf == "12345678909"


def test_create_record(client):
    response = client.post(
        "/registros/novo",
        data={
            "titulo": "Reunião de planejamento",
            "descricao": "Definir cronograma e meta do projeto.",
            "categoria": "Operacional",
            "status": "pendente",
            "data_vencimento": "2026-11-20",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Registro criado com sucesso" in response.data
    assert NumEsquece.query.count() == 1


def test_update_and_delete_record(client):
    client.post(
        "/registros/novo",
        data={
            "titulo": "Tarefa inicial",
            "descricao": "Registrar checklist inicial do projeto.",
            "categoria": "Atendimento",
            "status": "pendente",
            "data_vencimento": "2026-11-15",
        },
        follow_redirects=True,
    )

    record = NumEsquece.query.first()
    update_response = client.post(
        f"/registros/{record.id}/editar",
        data={
            "titulo": "Tarefa atualizada",
            "descricao": "Checklist revisado e aprovado.",
            "categoria": "Atendimento",
            "status": "concluido",
            "data_vencimento": "2026-11-18",
        },
        follow_redirects=True,
    )

    assert update_response.status_code == 200
    assert b"Registro atualizado com sucesso" in update_response.data
    assert db.session.get(NumEsquece, record.id).titulo == "Tarefa atualizada"

    delete_response = client.post(f"/registros/{record.id}/excluir", follow_redirects=True)
    assert delete_response.status_code == 200
    assert b"Registro removido com sucesso" in delete_response.data
    assert NumEsquece.query.count() == 0


def test_selected_list_page_includes_csrf_token_for_item_updates(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    user = User(
        nome="João da Silva",
        email="joao@email.com",
        cpf="12345678909",
    )
    user.set_password("Abcdef12!")
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as session:
        session["_user_id"] = str(user.id)
        session["_fresh"] = True

    shopping_list = ShoppingList(titulo="Lista de mercado", descricao="Itens básicos", user_id=user.id)
    db.session.add(shopping_list)
    db.session.flush()
    db.session.add(
        ShoppingItem(
            shopping_list_id=shopping_list.id,
            nome="Leite",
            quantidade="1",
            categoria="mercado",
            preco="10,00",
            comprado=False,
        )
    )
    db.session.commit()

    list_response = client.get(f"/listas/{shopping_list.id}/iniciar-selecionada")
    assert list_response.status_code == 200
    assert b'name="csrf_token"' in list_response.data

    update_response = client.post(
        f"/listas/{shopping_list.id}/iniciar-selecionada",
        data={
            "item_id": shopping_list.items[0].id,
            "quantidade": "2",
            "preco": "15,00",
        },
        follow_redirects=False,
    )

    assert update_response.status_code == 200
    assert b"Lista selecionada" in update_response.data
    assert shopping_list.items[0].quantidade == "2"
