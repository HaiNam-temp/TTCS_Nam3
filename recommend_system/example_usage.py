from recommend_system import ContentBasedRecommendationService, ItemContent, UserInteraction


def run_example() -> None:
    items = [
        ItemContent(
            item_id="ip15-128",
            title="iPhone 15 128GB",
            description="Apple A16, camera 48MP, OLED",
            categories=["smartphone", "apple"],
            tags=["iphone", "5g", "ios"],
        ),
        ItemContent(
            item_id="ip15-256",
            title="iPhone 15 256GB",
            description="Apple A16, camera 48MP, OLED, storage 256gb",
            categories=["smartphone", "apple"],
            tags=["iphone", "5g", "ios"],
        ),
        ItemContent(
            item_id="ss-s24",
            title="Samsung Galaxy S24",
            description="Snapdragon, AMOLED, camera 50MP",
            categories=["smartphone", "samsung"],
            tags=["android", "5g"],
        ),
    ]

    interactions = [
        UserInteraction(item_id="ip15-128", weight=1.0),
    ]

    service = ContentBasedRecommendationService()
    recommendations = service.recommend(items=items, interactions=interactions, top_k=2)

    for rec in recommendations:
        print(f"item_id={rec.item_id} score={rec.score:.4f} reason={rec.reason}")


if __name__ == "__main__":
    run_example()
