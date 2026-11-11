from app.extensions import db
from app.models.num_esquece import NumEsquece
from app.models.shopping import CompletedPurchase, ShoppingItem, ShoppingList, User
from app.routes.shopping_routes import sync_shopping_list_to_library


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"NumEsquece Lista" in response.data


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


def test_register_user_rejects_repeated_digits_cpf(client):
    response = client.post(
        "/register",
        data={
            "nome": "Usuário Teste",
            "email": "usuario.teste@email.com",
            "cpf": "000.000.000-00",
            "password": "Abcdef12!",
            "confirm_password": "Abcdef12!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Cadastro realizado com sucesso" not in response.data
    assert User.query.filter_by(cpf="00000000000").count() == 0


def test_register_user_rejects_invalid_check_digits_cpf(client):
    response = client.post(
        "/register",
        data={
            "nome": "Usuário Teste",
            "email": "usuario.teste@email.com",
            "cpf": "123.456.789-99",
            "password": "Abcdef12!",
            "confirm_password": "Abcdef12!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Cadastro realizado com sucesso" not in response.data
    assert User.query.filter_by(cpf="12345678999").count() == 0


def test_register_user_rejects_numeric_and_fake_email(client):
    for fake_email in ["00000000000", "00000000000@00000000000.com", "00000000000@gmail.com", "test@test"]:
        response = client.post(
            "/register",
            data={
                "nome": "Usuário Teste",
                "email": fake_email,
                "cpf": "529.982.247-25",
                "password": "Abcdef12!",
                "confirm_password": "Abcdef12!",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Cadastro realizado com sucesso" not in response.data
        assert User.query.filter_by(email=fake_email).count() == 0


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


def test_finalize_list_saves_the_purchase_history(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    user = User(
        nome="Ana Souza",
        email="ana@email.com",
        cpf="98765432100",
    )
    user.set_password("Abcdef12!")
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as session:
        session["_user_id"] = str(user.id)
        session["_fresh"] = True

    shopping_list = ShoppingList(titulo="Lista do mês", descricao="Compras domésticas", user_id=user.id)
    db.session.add(shopping_list)
    db.session.flush()
    db.session.add_all(
        [
            ShoppingItem(
                shopping_list_id=shopping_list.id,
                nome="Leite",
                quantidade="2",
                categoria="mercado",
                preco="10,00",
                comprado=False,
            ),
            ShoppingItem(
                shopping_list_id=shopping_list.id,
                nome="Pão",
                quantidade="1",
                categoria="mercado",
                preco="7,50",
                comprado=False,
            ),
        ]
    )
    db.session.commit()

    response = client.post(
        f"/listas/{shopping_list.id}/finalizar",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Hist\xc3\xb3rico" in response.data
    assert b"Leite" in response.data
    assert CompletedPurchase.query.count() == 1
    assert CompletedPurchase.query.first().total_compra == "R$ 27,50"
    assert db.session.get(ShoppingList, shopping_list.id).finalizado is True


def test_delete_shopping_list_with_items_and_library_record(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    user = User(
        nome="Carlos Silva",
        email="carlos@email.com",
        cpf="11144477735",
    )
    user.set_password("Abcdef12!")
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as session:
        session["_user_id"] = str(user.id)
        session["_fresh"] = True

    shopping_list = ShoppingList(titulo="Lista para deletar", descricao="Teste exclusão", user_id=user.id)
    db.session.add(shopping_list)
    db.session.flush()

    sync_shopping_list_to_library(shopping_list)
    db.session.add(
        ShoppingItem(
            shopping_list_id=shopping_list.id,
            nome="Café",
            quantidade="1",
            categoria="mercado",
            preco="15,00",
            comprado=False,
        )
    )
    db.session.commit()

    list_id = shopping_list.id
    assert NumEsquece.query.filter_by(shopping_list_id=list_id).count() == 1

    delete_response = client.post(f"/listas/{list_id}/excluir", follow_redirects=True)
    assert delete_response.status_code == 200
    assert b"Lista removida com sucesso" in delete_response.data
    assert db.session.get(ShoppingList, list_id) is None
    assert NumEsquece.query.filter_by(shopping_list_id=list_id).count() == 0
    assert ShoppingItem.query.filter_by(shopping_list_id=list_id).count() == 0
