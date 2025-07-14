class Atestado:
    def __init__(self, nomePaciente, nomeMedico, dataAtendimento, crmMedico, diasAtestado, cid=None):
        self.nomePaciente = nomePaciente
        self.nomeMedico = nomeMedico
        self.dataAtendimento = dataAtendimento
        self.crmMedico = crmMedico
        self.diasAtestado = diasAtestado
        self.cid = cid

    def __str__(self):
        return (f"Nome do Paciente: {self.nomePaciente}\n" +
                f"Nome do Médico: {self.nomeMedico}\n" +
                f"Data do Atendimento: {self.dataAtendimento}\n" +
                f"CRM do Médico: {self.crmMedico}\n" +
                f"Dias de Atestado: {self.diasAtestado}\n" +
                f"CID: {self.cid if self.cid else "Não possui CID"}"
                )

    def to_dict(self) -> dict:
        """
        Converte a instância do atestado em um dicionário.
        Usa 'self' para acessar os atributos da própria instância.
        """
        return {
            "nome_paciente": self.nomePaciente,
            "nome_medico": self.nomeMedico,
            "data_atendimento": self.dataAtendimento,
            "crm_medico": self.crmMedico,
            "dias_atestado": self.diasAtestado,
            "cid": self.cid
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nomePaciente=data.get("nome_paciente"),
            nomeMedico=data.get("nome_medico"),
            dataAtendimento=data.get("data_atendimento"),
            crmMedico=data.get("crm_medico"),
            diasAtestado=data.get("dias_atestado"),
            cid=data.get("cid")
        )



# class Atestado:
#     def __init__(self, nomePaciente, nomeMedico, dataAtendimento, crmMedico, diasAtestado, cid=None):
#         self.nomePaciente = nomePaciente
#         self.nomeMedico = nomeMedico
#         self.dataAtendimento = dataAtendimento
#         self.crmMedico = crmMedico
#         self.diasAtestado = diasAtestado
#         self.cid = cid

#     def __str__(self):
#         return (f"Nome do Paciente: {self.nomePaciente}\n" +
#                 f"Nome do Médico: {self.nomeMedico}\n" +
#                 f"Data do Atendimento: {self.dataAtendimento}\n" +
#                 f"CRM do Médico: {self.crmMedico}\n" +
#                 f"Dias de Atestado: {self.diasAtestado}\n" +
#                 f"CID: {self.cid if self.cid else "Não possui CID"}"
#                 )

#     @classmethod
#     def from_dict(cls, data: dict):
#         return cls(
#             nomePaciente=data.get("nome_paciente"),
#             nomeMedico=data.get("nome_medico"),
#             dataAtendimento=data.get("data_atendimento"),
#             crmMedico=data.get("crm_medico"),
#             diasAtestado=data.get("dias_atestado"),
#             cid=data.get("cid")
#         )

#     def to_dict(cls, atestado) -> dict:
#         return {
#             "nome_paciente": atestado.nomePaciente,
#             "nome_medico": atestado.nomeMedico,
#             "data_atendimento": atestado.dataAtendimento,
#             "crm_medico": atestado.crmMedico,
#             "dias_atestado": atestado.diasAtestado,
#             "cid": atestado.cid
#         }