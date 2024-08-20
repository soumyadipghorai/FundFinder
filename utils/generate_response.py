import os
from dotenv import main
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from schema.LLM_output import FundManagerDetails
from _temp.config import FUND_MANAGER_PROMPT

_ = main.load_dotenv(main.find_dotenv())
api_key, llama_model = os.getenv("GROQ_API_KEY"), os.getenv("GROQ_LLama")

class GenerateResponse:
    """
    A class to generate AI-based responses about mutual fund performance based on given parameters.
    """

    def __init__(self, expense_ratio: float, fund_manager_experience: list, fund_manager_prev_funds: list, 
                 fund_type: str, category: str, risk: str, nav: float, fund_size: float, 
                 overall_return: float, rank: int, AUM: float, fund_manager_prev_total_funds: list) -> None:
        self.llm = ChatGroq(temperature=0, model=llama_model, api_key=api_key) 
        self.expense_ratio = expense_ratio
        self.fund_manager_experience = fund_manager_experience
        self.fund_manager_prev_funds = fund_manager_prev_funds 
        self.fund_type = fund_type
        self.category = category
        self.risk = risk
        self.nav = nav
        self.fund_size = fund_size
        self.overall_return = overall_return
        self.rank = rank
        self.AUM = AUM
        self.fund_manager_prev_total_funds = fund_manager_prev_total_funds
        
    def __preprocess_manager_details(self):
        """
        Prepares and formats the fund manager details for the response generation.
        
        Returns:
            tuple: A list of dictionaries containing fund manager details and the average experience of the fund manager.
        """
        output = []
        for experience, prev_fund in zip(self.fund_manager_experience, self.fund_manager_prev_funds):
            output.append({
                "experience": experience, 
                "previous funds": prev_fund
            })

        avg_experience = round(sum(self.fund_manager_prev_total_funds) / len(self.fund_manager_prev_total_funds))
        return output, avg_experience
    
    def __fill_template(self, template, **kwargs):
        """
        Fills a template with the provided keyword arguments.
        
        Args:
            template (str): The template string to be filled.
            **kwargs: The keyword arguments to fill in the template.
        
        Returns:
            str: The formatted template string.
        """
        return template.format(**kwargs)

    def generate_respone(self):
        """
        Generates a response using the LLM based on the provided mutual fund data.
        
        Returns:
            dict: The generated response parsed into a dictionary format.
        """
        fund_manager_details, avg_experience = self.__preprocess_manager_details()
        values = {
            "expense_ratio": self.expense_ratio,
            "fund_manager_details": fund_manager_details, 
            "fund_type": self.fund_type, 
            "category": self.category, 
            "risk": self.risk, 
            "nav": self.nav,
            "fund_size": self.fund_size, 
            "overall_return": self.overall_return, 
            "rank": self.rank, 
            "AUM": self.AUM, 
            "avg_fund_manager_experience": avg_experience
        }
        
        template = self.__fill_template(FUND_MANAGER_PROMPT, **values)
        schema = FundManagerDetails
        parser = JsonOutputParser(pydantic_object=schema)

        prompt = PromptTemplate(
            template="\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        result = chain.invoke({"query": template})
        return result
