import pytest
from unittest.mock import Mock
from app.services.text_analysis_service import TextAnalysisService, State

def test_analyze_text_integration(mocker):
    # Mock do ChatOpenAI
    mock_llm = Mock()
    mock_llm.predict_messages.side_effect = [
        Mock(content="Notícias"),
        Mock(content="Pessoa1, Organização1, Local1"),
        Mock(content="Resumo do texto")
    ]
    
    # Criar instância do serviço com o mock
    service = TextAnalysisService("fake_api_key")
    service.llm = mock_llm
    
    # Executar análise
    result = service.analyze_text("Texto de exemplo")
    
    # Verificar resultado
    assert isinstance(result, dict)
    assert "classification" in result
    assert "entities" in result
    assert "summary" in result
    assert result["classification"] == "Notícias"
    assert result["entities"] == ["Pessoa1", "Organização1", "Local1"]
    assert result["summary"] == "Resumo do texto"

def test_classification_node():
    service = TextAnalysisService("fake_api_key")
    service.llm = Mock()
    service.llm.predict_messages.return_value = Mock(content="Notícias")
    
    state = {"text": "Texto de exemplo"}
    result = service._classification_node(state)
    
    assert result["classification"] == "Notícias"

def test_entity_extraction_node():
    service = TextAnalysisService("fake_api_key")
    service.llm = Mock()
    service.llm.predict_messages.return_value = Mock(content="Pessoa1, Organização1, Local1")
    
    state = {"text": "Texto de exemplo"}
    result = service._entity_extraction_node(state)
    
    assert result["entities"] == ["Pessoa1", "Organização1", "Local1"]

def test_summarization_node():
    service = TextAnalysisService("fake_api_key")
    service.llm = Mock()
    service.llm.predict_messages.return_value = Mock(content="Resumo do texto")
    
    state = {"text": "Texto de exemplo"}
    result = service._summarization_node(state)
    
    assert result["summary"] == "Resumo do texto" 