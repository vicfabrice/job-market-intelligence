class SkillNormalizer:
    ALIASES = {
        "python": "python",
        "fastapi": "fastapi",
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "spring boot": "spring_boot",
        "springboot": "spring_boot",
        "aws": "aws",
        "amazon web services": "aws",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "k8s": "kubernetes",
    }

    def normalize(self, skill: str) -> str | None:
        normalized_input = skill.strip().lower()
        return self.ALIASES.get(normalized_input)
