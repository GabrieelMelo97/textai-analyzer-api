from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    summary: str


class TextAnalysisService:
    def __init__(self, deepseek_api_key: str):
        self.llm = ChatOpenAI(api_key=deepseek_api_key, model="deepseek-chat", temperature=0, base_url="https://api.deepseek.com")
        self.workflow = self._create_workflow()

    def _classification_node(self, state: State):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Classifique o seguinte texto em uma das categorias: Notícias, Blog, Pesquisa ou Outro.\n\nTexto:{text}\n\nCategoria:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        classification = self.llm.predict_messages([message]).content.strip()
        return {"classification": classification}

    def _entity_extraction_node(self, state: State):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Extraia todas as entidades (Pessoa, Organização, Local) do seguinte texto. Forneça o resultado como uma lista separada por vírgulas.\n\nTexto:{text}\n\nEntidades:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        entities = self.llm.predict_messages([message]).content.strip().split(", ")
        return {"entities": entities}

    def _summarization_node(self, state: State):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Resuma o seguinte texto em uma frase curta.\n\nTexto:{text}\n\nResumo:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        summary = self.llm.predict_messages([message]).content.strip()
        return {"summary": summary}

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(State)
        
        # Adicionar nós ao grafo
        workflow.add_node("classification_node", self._classification_node)
        workflow.add_node("entity_extraction", self._entity_extraction_node)
        workflow.add_node("summarization", self._summarization_node)
        
        # Adicionar arestas ao grafo
        workflow.set_entry_point("classification_node")
        workflow.add_edge("classification_node", "entity_extraction")
        workflow.add_edge("entity_extraction", "summarization")
        workflow.add_edge("summarization", END)
        
        return workflow.compile()

    def analyze_text(self, text: str) -> dict:
        state_input = {"text": text}
        result = self.workflow.invoke(state_input)
        return result 