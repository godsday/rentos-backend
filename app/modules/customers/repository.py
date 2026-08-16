from sqlalchemy import or_

from app.db.base_repository import BaseRepository
from app.modules.customers.models import Customer


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db):
        super().__init__(db, Customer)

    def get_by_phone(
        self,
        tenant_id,
        phone,
    ):
        return (
            self.db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id,
                Customer.phone == phone,
                Customer.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_id_and_tenant(
        self,
        tenant_id,
        customer_id,
    ):
        return (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.tenant_id == tenant_id,
                Customer.is_deleted.is_(False),
            )
            .first()
        )

    def get_all_by_tenant(
        self,
        tenant_id,
        page,
        limit,
        search=None,
        is_active=None,
        sort_by="full_name",
        sort_order="asc",
    ):
        query = (
            self.db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id,
                Customer.is_deleted.is_(False),
            )
        )

        # Search by customer name, phone, or email.
        if search:
            search_term = f"%{search}%"

            query = query.filter(
                or_(
                    Customer.full_name.ilike(search_term),
                    Customer.phone.ilike(search_term),
                    Customer.email.ilike(search_term),
                )
            )

        # Filter by active status.
        if is_active is not None:
            query = query.filter(
                Customer.is_active == is_active,
            )

        # Whitelist sortable columns.
        sort_columns = {
            "full_name": Customer.full_name,
            "phone": Customer.phone,
            "email": Customer.email,
            "created_at": Customer.created_at,
            "updated_at": Customer.updated_at,
        }

        sort_column = sort_columns.get(
            sort_by,
            Customer.full_name,
        )

        if sort_order == "desc":
            query = query.order_by(
                sort_column.desc(),
            )
        else:
            query = query.order_by(
                sort_column.asc(),
            )

        total = query.count()

        customers = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return customers, total