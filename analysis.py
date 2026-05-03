def extract_products(text):
    if not text:
        return []
    lines = text.split("\n")
    products = []
    for line in lines:
        if "." in line and "-" in line:
            product = line.split("-")[0].split(".")[-1].strip()
            if product:
                products.append(product)
    return products

def calculate_visibility(user_product, all_results):
    if not all_results or not all_results[0]:
        return 0
    count = 0
    results = all_results[0]
    for item in results:
        if user_product.lower() in item.lower():
            count += 1
    if len(results) == 0:
        return 0
    return round((count / len(results)) * 100, 2)
