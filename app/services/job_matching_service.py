from dataclasses import dataclass


@dataclass
class JobMatchResult:
    matched_skills: list[str]
    missing_skills: list[str]
    score: float


class JobMatchingService:
    def match(
        self,
        candidate_skills: list[str],
        job_offer_skills: list[str],
    ) -> JobMatchResult:
        candidate_set = set(candidate_skills)
        job_set = set(job_offer_skills)

        matched = sorted(candidate_set & job_set)
        missing = sorted(job_set - candidate_set)

        score = 0.0
        if job_set:
            score = len(matched) / len(job_set) * 100

        return JobMatchResult(
            matched_skills=matched,
            missing_skills=missing,
            score=score,
        )
