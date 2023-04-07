from entities.pre_diagnostic_entities import PreDiagnosticResponse


class PreDiagnosticService:

    def __init__(self):
        self.symptons = [
            "Febre",
            "Tosse seca",
            "Fadiga",
            "Dificuldade para respirar",
            "Dores musculares",
            "Dor de cabeça",
            "Perda do paladar ou olfato",
            "Dor de garganta",
            "Congestão nasal",
            "Náuseas ou vômitos",
            "Diarreia",
        ]

    def get_pre_diagnostic(self, input_request):
        for sympton in self.symptons:
            if sympton.lower() in input_request.lower():
                return "Você apresenta diversos sintomas de Covid"
        return "Você não apresenta sintomas de Covid"

    def process_diagnostic(self, request):
        symptons = request.text
        diagnostic = self.get_pre_diagnostic(symptons)
        return PreDiagnosticResponse(
            name=request.name,
            diagnostic=diagnostic
        )