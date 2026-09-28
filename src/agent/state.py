from typing import  TypedDict
from src.router.schema import QueryRoute
from src.models.customer import Customer
from src.models.subscription import Subscription
#from src.models.ticket import ticket
from src.models.subscription import Subscription
from src.models.transaction import Transaction

class AgentState(TypedDict, total = False):
    #original user input
    user_query: str
    # result frm the intent router
    route: QueryRoute

    # structured_data
    customer_data: Customer | None
    Subscription_data: Subscription | None
    Transaction_data: Transaction | None
    #ticket_data: ticket_data | None

    #Rag
    rag_context: list

    #combined result
    tool_result: list

    #futureaction
    action: dict|None
    response:str | None

