from dataclasses import dataclass


@dataclass(frozen=True)
class UseCase:
    id: str
    name: str
    description: str


USE_CASES = {
    "workshop-knowledge": UseCase(
        "workshop-knowledge", "Workshop knowledge assistant", "Answers from the workshop guide corpus."
    ),
    "policy-handbook": UseCase(
        "policy-handbook", "Policy and handbook assistant", "Answers from a selected policy corpus."
    ),
    "technical-troubleshooting": UseCase(
        "technical-troubleshooting",
        "Technical troubleshooting assistant",
        "Answers from a selected troubleshooting corpus.",
    ),
}
