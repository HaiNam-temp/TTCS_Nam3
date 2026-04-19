from backend.repositories import (
    ConversationRepository,
    MessageRepository,
    PlatformRepository,
    ProductRepository,
    StatsRepository,
    UserRepository,
)
from backend.services import AdminService, AuthService, ConversationService, CrawlService, ProductService

user_repository = UserRepository()
conversation_repository = ConversationRepository()
message_repository = MessageRepository()
platform_repository = PlatformRepository()
stats_repository = StatsRepository()
product_repository = ProductRepository()

auth_service = AuthService(user_repository=user_repository)
conversation_service = ConversationService(
    conversation_repository=conversation_repository,
    message_repository=message_repository,
)
admin_service = AdminService(
    user_repository=user_repository,
    conversation_repository=conversation_repository,
    message_repository=message_repository,
    platform_repository=platform_repository,
    stats_repository=stats_repository,
)
product_service = ProductService(product_repository=product_repository)
crawl_service = CrawlService(product_service=product_service)
