import re

from app.services.skill_normalizer import SkillNormalizer


class SkillExtractor:
    def __init__(self, normalizer: SkillNormalizer) -> None:
        self.normalizer = normalizer

    def extract(self, text: str) -> list[str]:
        found_skills: set[str] = set()

        for alias in self.normalizer.ALIASES:
            pattern = rf"\b{re.escape(alias)}\b"

            if re.search(pattern, text, re.IGNORECASE):
                normalized_skill = self.normalizer.normalize(alias)

                if normalized_skill is not None:
                    found_skills.add(normalized_skill)

        return sorted(found_skills)
