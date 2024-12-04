import unittest
from unittest.mock import patch, MagicMock
from app.routes.ledger import ledger_bp
from app import create_app


class LedgerTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.app_context().push()
        self.app.register_blueprint(ledger_bp, name='ledger_test')
        self.client = self.app.test_client()

    @patch('app.routes.ledger.Users.query')
    @patch('app.routes.ledger.Items.query')
    def test_ledger_route(self, mock_items_query, mock_users_query):
        user1 = MagicMock()
        user1.username = 'Alice'
        user2 = MagicMock()
        user2.username = 'Bob'

        item1 = MagicMock()
        item1.itemName = 'Groceries'
        item1.itemPrice = '10.00'
        item1.date_created.date.return_value = '2024-12-01'
        item1.payerID = 1

        item2 = MagicMock()
        item2.itemName = 'Utilities'
        item2.itemPrice = '50.00'
        item2.date_created.date.return_value = '2024-12-02'
        item2.payerID = 2

        with patch('app.routes.ledger.Users.query.order_by') as mock_users_query, \
             patch('app.routes.ledger.Items.query.order_by') as mock_items_query:
            mock_users_query.return_value.all.return_value = [user1, user2]
            mock_items_query.return_value.all.return_value = [item1, item2]
            
            # Send a GET request to the ledger route
            response = self.client.get('/ledger')
            
            self.assertIn(b"Groceries", response.data)
            self.assertIn(b"Utilities", response.data)
            self.assertIn(b"Alice", response.data)
            self.assertIn(b"Bob", response.data)

    @patch('app.routes.ledger.db.session')
    @patch('app.routes.ledger.Items')
    @patch('app.routes.ledger.UserItem')
    def test_add_item(self, mock_user_item, mock_items, mock_db_session):
        form_data = {
            'itemName': 'Internet Bill',
            'itemPrice': '75',
            'payerID': '1',
            'itemUsers': ['1', '2']
        }

        mock_item_instance = MagicMock(id=1)
        mock_items.return_value = mock_item_instance

        # Send a POST request to the /addItem route
        response = self.client.post('/addItem', data=form_data, follow_redirects=True)

        self.assertTrue(mock_db_session.add.called)
        self.assertTrue(mock_db_session.commit.called)
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.ledger.db.session')
    @patch('app.routes.ledger.Items.query')
    @patch('app.routes.ledger.UserItem.query')
    def test_delete_item(self, mock_user_item_query, mock_items_query, mock_db_session):
        mock_item_instance = MagicMock(id=1)
        mock_items_query.get_or_404.return_value = mock_item_instance

        # Send a GET request to delete an item
        response = self.client.get('/deleteItem/1', follow_redirects=True)

        self.assertTrue(mock_user_item_query.filter_by.called)
        self.assertTrue(mock_db_session.delete.called)
        self.assertTrue(mock_db_session.commit.called)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()