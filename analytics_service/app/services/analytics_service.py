from app.infrastructure.models import ProductAnalytics, OrderAnalytics


def process_event(event, db):
    event_type = event.get("event_type")
    data = event.get("data")

    if event_type in ["order_created", "order_paid", "order_payment_failed"]:
        db_order = (
            db.query(OrderAnalytics)
            .filter(OrderAnalytics.order_id == data["order_id"])
            .first()
        )

        if not db_order:
            db_order = OrderAnalytics(
                order_id=data["order_id"],
                user_id=data["user_id"],
                total_amount=data.get("total", 0.0),
                status=data.get("status", "pending"),
                payment_status=(
                    "paid"
                    if event_type == "order_paid"
                    else "failed" if event_type == "order_payment_failed" else "pending"
                ),
            )
            db.add(db_order)
        else:
            db_order.status = data.get("status", db_order.status)
            db_order.payment_status = data.get(
                "payment_status", db_order.payment_status
            )

    elif event_type in [
        "product_created",
        "product_updated",
        "product_stock_updated",
    ]:
        db_product = (
            db.query(ProductAnalytics)
            .filter(ProductAnalytics.product_id == data["id"])
            .first()
        )

        if not db_product:
            db_product = ProductAnalytics(
                product_id=data["id"],
                name=data.get("name", ""),
                stock=data.get("stock", 0),
                price=data.get("price", 0.0),
                category=(
                    data.get("category", {}).get("name")
                    if data.get("category")
                    else None
                ),
                # category=(
                #     data.get("category", {}).get("name")
                #     if data.get("category")
                #     else None
                # ),
                # which one is correct? - The category field should store the category name for easier querying and
                # analytics. The original code had a redundant category field that stored the entire category object, which is not necessary for analytics purposes. Therefore, we should keep the line that extracts the category name and remove the redundant one.
                tags=",".join([t["name"] for t in data.get("tags", [])]),
                active_promotions=(
                    ",".join([p["name"] for p in data.get("promotions", [])])
                    if data.get("promotions")
                    else ""
                ),
            )
            db.add(db_product)
        else:

            db_product.name = data.get("name", db_product.name)
            db_product.stock = data.get("stock", db_product.stock)
            db_product.price = data.get("price", db_product.price)
            db_product.category = (
                data.get("category", {}).get("name")
                if data.get("category")
                else db_product.category
            )
            db_product.tags = (
                ",".join([t["name"] for t in data.get("tags", [])])
                if data.get("tags")
                else db_product.tags
            )
            db_product.active_promotions = (
                ",".join([p["name"] for p in data.get("promotions", [])])
                if data.get("promotions")
                else db_product.active_promotions
            )

    elif event_type in ["promotion_created", "promotion_updated", "promotion_deleted"]:
        product_id = data.get("product_id")
        if product_id:
            db_product = (
                db.query(ProductAnalytics)
                .filter(ProductAnalytics.product_id == product_id)
                .first()
            )
            if db_product:
                # recompute active promotions
                db_product.active_promotions = (
                    data.get("name") if event_type != "promotion_deleted" else ""
                )

    """
    Maintains up-to-date product and order summaries

    Can be extended to aggregate revenue, stock trends, or promotion effectiveness
    """
