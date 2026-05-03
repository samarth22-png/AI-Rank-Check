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

def generate_report_card(user_product, product_list, score):
    # Determine Grade
    if score >= 80:
        grade = "A 🏆"
    elif score >= 50:
        grade = "B ⭐"
    elif score > 0:
        grade = "C ⚠️"
    else:
        grade = "F ❌"

    # Determine Rank and Competitors
    rank = "Unranked"
    competitors = []
    
    for i, product in enumerate(product_list):
        if user_product.lower() in product.lower():
            if rank == "Unranked": # Only take the highest rank if mentioned multiple times
                rank = f"#{i + 1}"
        else:
            competitors.append(product)

    return {
        "grade": grade,
        "rank": rank,
        "competitors": competitors
    }
