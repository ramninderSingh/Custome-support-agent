from src.router.classifier import QueryRouter

router = QueryRouter()

def router_node(state):
    query = state['user_query']
    route = router.classify(query)

    print("\n[ROUTER]")
    print(route.model_dump())

    return {
        "route": route
    }
