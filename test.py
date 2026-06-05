from app.services.rag import retrieve_context

result = retrieve_context(
    "Fractions",
    5
)

print(result)