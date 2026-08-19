from app.integrations.greenhouse.client import GreenhouseClient


def main() -> None:
    client = GreenhouseClient()

    try:
        jobs = client.get_jobs("temporaltechnologies")

        print(f"Jobs found: {len(jobs)}")

        for job in jobs[:5]:
            print(
                job.id,
                job.title,
                job.location.name,
                job.absolute_url,
            )
    finally:
        client.close()


if __name__ == "__main__":
    main()
