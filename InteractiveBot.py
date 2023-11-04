from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import ResponseSchema
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
import os
from defined_texts import intro, outline_intro

class InteractiveBot():

    def __init__(self) -> None:
        self.default_temperature = 0.7
        self.llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
            model=os.getenv("OPENAI_MODEL_NAME"),
            temperature=0.7,
            openai_api_version="2023-05-15"
        )

        outline_schema_context = ResponseSchema(name="Kontext", description="Ein Vorschlag für den Kontext der Geschichte auf Deutsch. 30 - 50 Wörter.")
        outline_schema_decisionpoint = ResponseSchema(name="Entscheidungspunkt", description="Erklärung des Entscheidungspunkts der Geschichte auf Deutsch. Circa 30 Wörter.")
        self.outline_output_parser = StructuredOutputParser.from_response_schemas([outline_schema_context, outline_schema_decisionpoint])
        self.outline_format_instructions = self.outline_output_parser.get_format_instructions()

        self.outline_prompt = ChatPromptTemplate.from_template(
            outline_intro + """
                {format_instructions}
            """
        )
        
        character_schema = ResponseSchema(name="Charaktername", description="Der Vorname des Charakters.")
        role_schema = ResponseSchema(name="Rolle", description="Die Rolle des Charakters in der Geschichte.")
        text_schema = ResponseSchema(name="Text", description="Der Textabschnitt, der vom Charakter gesagt wird. Maximal ein Satz und 50 Zeichen.")
        location_schema = ResponseSchema(name="Ort", description="Der Ort, an dem sich der Charakter befindet.")

        self.output_parser = StructuredOutputParser.from_response_schemas([character_schema, role_schema, text_schema, location_schema])
        self.format_instructions = self.output_parser.get_format_instructions()

        self.initial_prompt = ChatPromptTemplate.from_template(
            intro + """                    
                Gib einen einzelnen Textabschnitt an, \
                    sowie den Namen des Charakters und den Ort, an dem sich dieser befindet, um die Geschichte zu beginnen.\

                {format_instructions}
            """
        )
    
        self.prompt = ChatPromptTemplate.from_template(
            intro + """                    
                Gib einen einzelnen Textabschnitt an, wie ein anderer Charakter auf die Aussage reagiert oder der alte Charakter dessen Gedanken fortführt, \
                    sowie den Namen des Charakters und den Ort, an dem sich dieser befindet.

                {format_instructions}
                
                Die bisherige Geschichte lässt sich folgendermaßen zusammenfassen: {summary}\
            """
        )

        self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=200, ai_prefix="Nächster Vorschlag", human_prefix="Bisherige Konversation")
        self.conversation = []
        
        self.outline_chain = LLMChain(
            llm=self.llm,
            prompt=self.outline_prompt,
            verbose=True
        )

        self.suggestion_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True
        )

        self.initial_suggestion_chain = LLMChain(
            llm=self.llm,
            prompt=self.initial_prompt,
            verbose=True
        )

    def test_call(self):

        test_prompt = "What is 1+1?"

        return self.llm([HumanMessage(content=test_prompt)]).content
    
    def update_temperature(self, temp):

        self.temp = temp

        self.outline_chain.llm.temperature = temp
        self.suggestion_chain.llm.temperature = temp
        self.initial_suggestion_chain.llm.temperature = temp

    def handle_suggestion_request(self, setup, story_history, temp:float=None):

        if not story_history:
            return self.initial_suggestion(setup, temp)
        else:
            return self.make_suggestion(setup, story_history, temp)
        
    def handle_outline_request(self, setup, temp:float=None):
        
        if (temp == None):
            self.initial_suggestion_chain.llm.temperature = self.default_temperature
        else:
            self.initial_suggestion_chain.llm.temperature = temp

        raw_output = self.outline_chain.run({
            "workArea": setup["workArea"] if setup["workArea"] else "Reinigungsarbeiten", "employer": setup["employer"],
            "employerInfo": setup["employerInfo"], "employee": setup["employee"], "employeeInfo": setup["employeeInfo"],
            "format_instructions": self.outline_format_instructions
        })

        parsed_output = self.parse_raw_outline_output(raw_output)

        return parsed_output

    def make_suggestion(self, setup, story_history, temp:float=None):
        
        if (temp == None):
            self.initial_suggestion_chain.llm.temperature = self.default_temperature
        else:
            self.initial_suggestion_chain.llm.temperature = temp

        self.memory.clear()
        self.memory.save_context({"input": str(story_history)}, {"output": ""})

        raw_output = self.suggestion_chain.run({
            "workArea": setup["workArea"] if setup["workArea"] else "Reinigungsarbeiten", "employer": setup["employer"],
            "employerInfo": setup["employerInfo"], "employee": setup["employee"], "employeeInfo": setup["employeeInfo"],
            "outline": setup["outline"], "format_instructions": self.format_instructions, 
            "summary": self.memory.load_memory_variables({})["history"]
        })
        parsed_output = self.parse_raw_output(raw_output)

        return parsed_output
    
    def initial_suggestion(self, setup, temp:float=None):

        if (temp == None):
            self.initial_suggestion_chain.llm.temperature = self.default_temperature
        else:
            self.initial_suggestion_chain.llm.temperature = temp

        raw_output = self.initial_suggestion_chain.run({
            "workArea": setup["workArea"] if setup["workArea"] else "Reinigungsarbeiten", "employer": setup["employer"],
            "employerInfo": setup["employerInfo"], "employee": setup["employee"], "employeeInfo": setup["employeeInfo"],
            "outline": setup["outline"], "format_instructions": self.format_instructions
        })
        parsed_output = self.parse_raw_output(raw_output)

        return parsed_output
    
    def parse_raw_output(self, raw_output):
        print("1: " + raw_output)
        raw_output_split = raw_output.split("```json")
        raw_output_json = "```json" + raw_output_split[1]
        raw_output_thoughts_split = raw_output_split[1].split("}\n```")
        raw_output_thoughts = raw_output_thoughts_split[1:len(raw_output_thoughts_split)]
        print("2: " + str(raw_output_thoughts) if raw_output_thoughts is not None else "")
        parsed_output = self.output_parser.parse(raw_output_json)
        parsed_output["Gedanken"] = raw_output_thoughts
        print("3: " + str(parsed_output))

        return parsed_output
    
    def parse_raw_outline_output(self, raw_output):
        print("1: " + raw_output)
        raw_output_split = raw_output.split("}")
        raw_output_json = raw_output_split[0] + "}```"
        print("2: " + raw_output_json)
        parsed_output = self.outline_output_parser.parse(raw_output_json)

        return parsed_output