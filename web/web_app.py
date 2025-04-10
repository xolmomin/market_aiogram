import os

import uvicorn
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import conf
from database import User, Product, Category, base
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY)
]

app = Starlette(middleware=middleware)

logo_url = 'https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-host-and-admin-marketing-job-vacancies-vector-png-image_6480101.png'
admin = Admin(
    engine=base.db._engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider()
)


class ProductModelView(ModelView):
    exclude_fields_from_list = ('cart_items', 'order_items', 'created_at', 'updated_at')
    exclude_fields_from_create = ('cart_items', 'order_items', 'created_at', 'updated_at')
    exclude_fields_from_edit = ('cart_items', 'order_items', 'created_at', 'updated_at')


class UserModelView(ModelView):
    exclude_fields_from_list = ('carts', 'orders', 'referrals', 'created_at', 'updated_at')
    exclude_fields_from_create = ('carts', 'orders', 'referrals', 'created_at', 'updated_at')
    exclude_fields_from_edit = ('carts', 'orders', 'referrals', 'created_at', 'updated_at')


class CategoryModelView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Category))
admin.add_view(ProductModelView(Product))

# Mount admin to your app
admin.mount_to(app)

# Configure Storage
os.makedirs("./media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
