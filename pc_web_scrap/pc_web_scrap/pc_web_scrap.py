"""
Web scrapping with Python and Pynecone
"""

# the modules used in this project ...
import pynecone as pc
import requests
from bs4 import BeautifulSoup

# setup the options list for the intrested programming lang:
options = ["Rust", "Python", "JavaScript", "C++", "Go"]


class State(pc.State):
    lang: str = ""

    # set up the main root URL:
    url: str = "https://github.com/trending/" + lang

    # create an empty list that'll store the repo details
    repositories: list[list[str]]

    def search_repo(self):
        if self.lang != "":
            # first clear the list for a new set of repos ...
            self.repositories = []

            url = self.url + self.lang.lower()

            # Make the HTTP request
            response = requests.get(url)

            # createa  beautifulsoup object
            soup = BeautifulSoup(response.content, "html.parser")

            repositories = soup.find_all("article", class_="Box-row")

            # now we loop over the parsed HTML 5 times to get the top 5 repo's corresponding to the selected language
            for repo in repositories[:5]:
                span_element = repo.find("span", class_="text-normal")

                # what we do here is use the set element and strip it to get the inner text. the replace() method is to remove any whitespaces
                title_1 = span_element.text.strip().replace(" ", "")
                title_2 = span_element.next_sibling.text.strip().replace(" ", "")

                name = title_1 + title_2

                subtitle = repo.find("p", "col-9 color-fg-muted my-1 pr-4").text.strip()

                # now for the star and fork numbers
                stars_element = repo.find(
                    "a", href=lambda href: href and "/stargazers" in href
                )

                stars_count = stars_element.text.strip()

                forks_element = repo.find(
                    "a", href=lambda href: href and "/forks" in href
                )

                forks_count = forks_element.text.strip()

                # now, we can append these to the repo list we created in the State class
                self.repositories.append([name, subtitle, stars_count, forks_count])


def create_options(name):
    return pc.radio(name)


# to use the data, we need to reusable UI and place it inside the pc.foreach logic


def create_repo_details(data):
    return pc.hstack(
        pc.vstack(
            pc.container(
                pc.image(
                    src="https://img.icons8.com/material-rounded/384/github.png",
                    width="28px",
                    height="auto",
                ),
                padding="0",
                display="flex",
            )
        ),
        pc.vstack(
            pc.container(
                pc.tooltip(
                    data[0],
                    label=data[1],
                    gutter=50,
                ),
                padding="0",
            ),
            pc.container(
                pc.hstack(
                    pc.image(
                        src="https://img.icons8.com/ios-filled/100/star--v1.png",
                        width="12px",
                        height="auto",
                    ),
                    pc.text(data[2], align="left"),
                    pc.image(
                        src="https://img.icons8.com/ios/100/wishbone.png",
                        width="12px",
                        height="auto",
                    ),
                    pc.text(data[3], align="left"),
                ),
                padding="0",
            ),
        ),
        box_shadow="lg",
        padding="12px",
        border_radius="6px",
        bg="white",
    )


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading(
                "Find Trending Repositories",
                size="2xl",
                font_weight="bold",
            ),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.radio_group(
                pc.hstack(
                    pc.foreach(
                        options,
                        create_options,
                    ),
                    spacing="2.5rem",
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                on_change=State.set_lang,
            ),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.button(
                "Search",
                w="230px",
                height="45px",
                color_scheme="blue",
                on_click=lambda: State.search_repo,
            ),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.hstack(
                # forloop logic here ...
                pc.foreach(
                    State.repositories,
                    create_repo_details,
                ),
                spacing="1.5rem",
            ),
        ),
        w="100%",
        height="100vh",
        bg="lightblue",
        display="flex",
        align_items="center",
        justify_content="center",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
