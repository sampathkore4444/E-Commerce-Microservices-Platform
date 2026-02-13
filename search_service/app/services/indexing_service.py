from typing import Dict, List


# Simulated in-memort index for demo purposes
# class IndexingService:
#     def __init__(self):
#         self.index: Dict[str, List[Dict]] = {}

#     def index_product(self, product: Dict):
#         category = product.get("category", "uncategorized")
#         if category not in self.index:
#             self.index[category] = []
#         self.index[category].append(product)

#     def search(self, query: str) -> List[Dict]:
#         results = []
#         for category, products in self.index.items():
#             for product in products:
#                 if query.lower() in product.get("name", "").lower():
#                     results.append(product)
#         return results


# Simulated in-memort index for demo purposes
INDEX: Dict[int, Dict] = {}


def add_or_update_product(product: Dict):

    product_id = product.get("id")

    if product_id is not None:
        INDEX[product_id] = {
            "id": product_id,
            "name": product.get("name"),
            "description": product.get("description"),
            "price": product.get("price"),
            "stock": product.get("stock"),
            "category": product.get("category"),
            "tags": product.get("tags"),
            "promotions": product.get("promotions"),
        }

    print(f"Product {product_id} indexed/updated successfully.")


def remove_product_from_index(product_id: int):
    if product_id in INDEX:
        del INDEX[product_id]
        print(f"Product {product_id} removed from index.")
    else:
        print(f"Product {product_id} is not found in the index.")


def search_products(
    query: str,
    category_id: int = None,
    tag_id: int = None,
    min_price: float = None,
    max_price: float = None,
    in_stock_only: bool = False,
) -> List[Dict]:
    results = []
    for product in INDEX.values():
        if query and query.lower() not in product.get("name", "").lower():
            continue

        if (
            category_id
            and product.get("category") != category_id
            and product.get("category") is not None
        ):
            continue

        if (
            tag_id
            and tag_id not in product.get("tags", [])
            and product.get("tags") is not None
        ):
            continue

        if tag_id and not any(t["id"] == tag_id for t in product.get("tags", [])):
            continue

            # above 2 if conditions. which one is correct?
            # we can use either of them. the first one checks if the tag_id is not in the list of tags,
            # while the second one checks if any tag in the list of tags has the same id as the tag_id.
            # both conditions will work correctly, but the second one is more efficient
            # because it uses a generator expression to check for the presence of the tag_id in the list of tags,
            # which can short-circuit and return True as soon as a match is found,
            # while the first one will check all tags in the list even if a match is found early on.

        if min_price is not None and product.get("price", 0) < min_price:
            continue

        # why we did not use tag_id is not None in the above if condition?
        # we did not use tag_id is not None because if tag_id is None, it will not enter the if condition and
        # will not filter products based on tags, which is the intended behavior.
        # If we used tag_id is not None, it would always enter the if condition and filter products based on tags, even when tag_id is None, which would not be correct.

        # can I use if min_price: instead of if min_price is not None:?
        # It is generally better to use if min_price is not None: instead of if min_price:
        # because if min_price is 0, it would evaluate to False in the if min_price: condition, which would not be the intended behavior.
        # Using if min_price is not None: ensures that we are specifically checking for the presence of a value for min_price, rather than relying on its truthiness, which can lead to unintended consequences when min_price is 0 or any other falsy value.

        if max_price is not None and product.get("price", 0) > max_price:
            continue

        if in_stock_only and product.get("stock", 0) <= 0:
            continue

        results.append(product)

    return results
