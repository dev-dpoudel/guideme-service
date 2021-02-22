# Provides Pagination Services as a Dependencies to API


# Declared as async def to support ASGI architecture
async def page_info(page: int = 0, size: int = 100):
    return {"page": page, "size": size}
