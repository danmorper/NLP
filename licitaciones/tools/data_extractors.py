import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

# Define the Pydantic models for the data extracted
class CompanyData(BaseModel):
    company: str = Field(..., title="Company", description="The name of the company involved in the contract")

class FinancialData(BaseModel):
    amount: float = Field(..., title="Amount", description="The total amount of the contract")
    currency: str = Field(..., title="Currency", description="The currency of the contract amount")

# Define the DataExtractor class
class DataExtractor:
    def __init__(self, api_key: str ='ollama', base_url="http://localhost:11434/v1", text: str = None):
        self.text = text
        self.client = instructor.patch(
            OpenAI(
                base_url=base_url,
                api_key=api_key,
            ),
            mode=instructor.Mode.JSON,
        )

        # Initialize the extracted data
        self.company_name = None
        self.amount = None
        self.currency = None

    def extract_company(self):
        content = f"""
        Extract the name of the company from the following text:
        {self.text}
        """
        response = self.client.chat.completions.create(
            model="llama3",
            messages=[{"role": "user", "content": content}],
            response_model=CompanyData,
            max_retries=10
        )
        self.company_name = response.company
        

    def extract_amount(self):
        content = f"""
        Extract the total contract amount and its currency from the following text:
        {self.text}
        """
        response = self.client.chat.completions.create(
            model="llama3",
            messages=[{"role": "user", "content": content}],
            response_model=FinancialData,
            max_retries=10
        )
        self.amount = response.amount
        self.currency = response.currency