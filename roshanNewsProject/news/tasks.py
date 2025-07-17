from celery import shared_task
import subprocess, os

@shared_task
def crawling():
    print("start crawling")
    if os.environ.get("DOCKER_ENV") == "true":
        project_dir = "/app/zoomit"
    else:
        project_dir = "/home/amir-hakimi/Desktop/roshan_project/roshanNewsProject/zoomit"
    subprocess.run(['scrapy','crawl','zoomit'], cwd=project_dir)
    print("end")
