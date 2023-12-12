from datetime import datetime


class RepositoryModel:
    def __init__(self, name, owner, description, language, stars_total, stars_today, duration, repository_url,
                 last_updated):
        self.name = name
        self.owner = owner
        self.description = description
        self.language = language
        self.stars_total = stars_total
        self.stars_today = stars_today
        self.duration = duration
        self.repository_url = repository_url
        self.last_updated = last_updated

    @classmethod
    def from_html(cls, html):
        name_element = html.select_one('.h3 a')
        name = name_element.text.strip() if name_element else 'N/A'

        repository_url = name_element['href'].strip() if name_element and 'href' in name_element.attrs else 'N/A'
        repository_url = "https://github.com" + repository_url;

        owner_element = html.select_one('.text-normal')
        owner = owner_element.text.strip() if owner_element else 'N/A'

        description_element = html.select_one('.col-9')
        description = description_element.text.strip() if description_element else 'N/A'

        language_element = html.select_one('[itemprop="programmingLanguage"]')
        language = language_element.text.strip() if language_element else 'N/A'

        stars_total_element = html.select_one('.Link.Link--muted.d-inline-block.mr-3')
        stars_total = stars_total_element.text.strip() if stars_total_element else '0'

        stars_today_element = html.select_one('.d-inline-block.float-sm-right')
        stars_today = stars_today_element.text.strip() if stars_today_element else '0'

        # Assuming 'html' is the BeautifulSoup object containing the HTML structure
        stars_duration_element = html.select_one('.float-sm-right')
        stars_duration_text = stars_duration_element.text.strip() if stars_duration_element else 'N/A'

        # Extracting the duration from the text
        if 'stars today' in stars_duration_text:
            duration = 'daily'
        elif 'stars this week' in stars_duration_text:
            duration = 'weekly'
        elif 'stars this month' in stars_duration_text:
            duration = 'monthly'
        else:
            duration = 'N/A'

        return cls(name, owner, description, language, stars_total, stars_today, duration, repository_url,
                   datetime.now())
