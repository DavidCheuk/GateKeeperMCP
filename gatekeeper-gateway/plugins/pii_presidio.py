from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import json
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
def before_request(request, json_body):
    params = json_body.get("parameters", {})
    text = json.dumps(params)
    results = analyzer.analyze(text=text, language="en")
    if results:
        anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
        json_body["parameters"] = json.loads(anonymized.text)
