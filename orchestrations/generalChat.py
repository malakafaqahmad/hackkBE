from agents.sAgents.toolformer.fuctValidator import funct_validator
from agents.sAgents.toolformer.functCaller import function_caller
from agents.sAgents.toolformer.generalchat import general_chat



def general_chat_orchestration(patientid, user_input):

    funct = function_caller(user_input)
    

