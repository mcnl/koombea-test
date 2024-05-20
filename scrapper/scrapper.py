import threading
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import transaction
from .models import Page, Link


class Scraper:
    def __init__(self):
        self.lock = threading.Lock()

    def add_page(self, user: User, link: str):
        """
        Add a link to a web page to be scraped, and create a thread to scrape the page for a specific user.

        :param user: User instance who owns the page.
        :param link: URL of the page to be scraped.
        """
        with transaction.atomic():
            page_data = {
                "user": user,
                "page_link": link,
                "name": str(link),
                "total_links": "in progress",
            }
            try:
                page, created = Page.objects.get_or_create(**page_data)

                if created:
                    thread = threading.Thread(target=self._scrape_page, args=(page,))
                    thread.start()
            except Exception as e:
                print(str(e))
                return

    def list_pages(self, user: User):
        """
        Return the list of pages for a specific user with their current scraping status.

        :param user: User instance whose pages are to be listed.
        :return: List of dictionaries containing page information.
        """
        pages = Page.objects.filter(user=user)
        return [
            {
                "id": page.id,
                "Name": page.name if page.total_links != None else str(page.page_link),
                "Total Links": (
                    page.total_links if page.total_links != None else "in progress"
                ),
                "page_link": page.page_link,
            }
            for page in pages
        ]

    def page_details(self, user: User, page_id: int):
        """
        Return the details of the links contained in the page with the specified ID for a specific user.

        :param user: User instance who owns the page.
        :param page_id: ID of the page whose details are to be retrieved.
        :return: List of dictionaries containing link information.
        """
        try:
            page = Page.objects.get(id=page_id, user=user)
            links = page.links.all()
            return [{"Name": link.name, "Total Links": link.link} for link in links]
        except Page.DoesNotExist:
            return []

    @transaction.atomic
    def _scrape_page(self, page: Page):
        """
        Scrape the page and extract all links.

        :param page: Page model instance to be scraped.
        """
        page_link = page.page_link
        try:
            response = requests.get(page_link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = []

            for tag in soup.find_all(["a", "link", "img"]):
                href = tag.get("href") or tag.get("src")
                text = tag.get_text(strip=True) or str(tag)
                if href and len(href) > 0:
                    links.append(Link(page=page, name=text, link=href))

            # Save all links in a single transaction
            Link.objects.bulk_create(links)

            page.name = soup.title.string if soup.title else page_link
            page.total_links = str(len(links))
            page.save()

        except requests.RequestException as e:
            page.total_links = str(-1)  # Indicate an error occurred
            page.save()
            print(f"Failed to scrape {page_link}: {e}")
