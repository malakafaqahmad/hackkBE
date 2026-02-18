from medgemma.medgemmaClient import MedgemmaClient



def fucntion_caller(function_name, args):
    """
    Calls a function by name with the provided arguments.
    """

    systemPrompt = """
"""

    # Create an instance of MedgemmaClient
    client = MedgemmaClient()

    # Call the function using the client
    result = client.call_function(function_name, args)

    return result