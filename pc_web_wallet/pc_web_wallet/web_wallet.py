import pynecone as pc
from cryptography.fernet import Fernet


# Generate a key for encrypting passwords
# key = Fernet.generate_key()
key: bytes = b"HB0GspC55x2P-PwV1-K-WUkY-pVsYzOaAmIIrMC54Kc="
fernet = Fernet(key)


# storage model for data
class Vault(pc.Model, table=True):
    website: str
    username: str
    password: bytes


def encrypt_password(password):
    return fernet.encrypt(password.encode())


def decrypt_password(password):
    return fernet.decrypt(password).decode()


def add_login_info(website, username, password):
    # Encrypt the password before storing it in the database
    encrypted_password = encrypt_password(password)

    # store final data into vault table
    with pc.session() as session:
        session.add(
            Vault(
                website=website,
                username=username,
                password=encrypted_password,
            )
        )
        session.commit()


class State(pc.State):
    # drawer settings
    show_left: bool = False

    # overlay settings
    show_pass: bool = False

    # input settings
    email: str
    password: str

    # data list
    data_list: list[list]

    def set_email(self, email):
        self.email = email

    def set_pasword(self, password):
        self.password = password

    def toggle_left_drawer(self):
        self.show_left = not (self.show_left)

    def toggle_overlay_passwords(self):
        self.show_pass = not (self.show_pass)

    def save_user_data(self):
        add_login_info("Google", self.email, self.password)
        self.email, self.password = "", ""

    @pc.var
    def display_listed_passwords(self):
        with pc.session() as session:
            data_row = session.query(
                Vault.website, Vault.username, Vault.password
            ).all()

            data_row = [
                [website, email, decrypt_password(encoded_password)]
                for website, email, encoded_password in data_row
            ]

            self.data_list = data_row


def display_data(data):
    return pc.container(
        pc.vstack(
            pc.text(
                data[0],
                font_size="0.75rem",
                color="#bbbbbb",
                font_weight="400",
            ),
            pc.text(
                data[1],
                font_size="1.25rem",
                font_weight="bold",
            ),
        ),
        w="250px",
        h="70px",
        border_radius="8px",
        bg="#3c4661",
        display="flex",
        align_items="center",
        justify_content="center",
        color="white",
        cursor="pointer",
        transition="all 500ms",
        _hover={"box_shadow": "0 5px 10px 0 rgba(0, 0, 0, 0.45)"},
        on_click=lambda: State.toggle_overlay_passwords,
    )


def index() -> pc.Component:
    return pc.vstack(
        pc.drawer(
            pc.drawer_overlay(
                pc.drawer_content(
                    pc.container(
                        pc.heading(
                            "Pass Lite Form",
                            text_align="center",
                        ),
                        w="100%",
                        h="100px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    pc.container(
                        pc.form_control(
                            pc.text("Email", font_size="md"),
                            pc.input(
                                value=State.email,
                                border="None",
                                border_bottom="1px solid black",
                                border_radius="0px",
                                padding="0px",
                                focus_border_color="None",
                                on_change=lambda: State.set_email(),
                            ),
                            is_required=True,
                        ),
                        w="100%",
                        h="100px",
                    ),
                    pc.container(
                        pc.form_control(
                            pc.text("Password", font_size="md"),
                            pc.input(
                                value=State.password,
                                border="None",
                                border_bottom="1px solid black",
                                border_radius="0px",
                                padding="0px",
                                focus_border_color="None",
                                type_="password",
                                on_change=lambda: State.set_password(),
                            ),
                            is_required=True,
                        ),
                        w="100%",
                        h="100px",
                    ),
                    pc.drawer_footer(
                        pc.button(
                            "Close",
                            on_click=State.toggle_left_drawer,
                        ),
                        pc.spacer(),
                        pc.button(
                            "Submit",
                            on_click=[
                                lambda: State.save_user_data(),
                                State.toggle_left_drawer,
                            ],
                        ),
                    ),
                    # bg="rgba(0, 0, 0, 0.3)",
                    display="flex-start",
                    display_direction="column",
                    align_items="start",
                    justify_content="center",
                )
            ),
            placement="left",
            is_open=State.show_left,
            is_full_height=True,
            is_centered=True,
            close_on_esc=True,
        ),
        pc.vstack(
            pc.container(
                pc.heading(
                    "Welcome to ",
                    pc.span(
                        "Pass Lite",
                        background="linear-gradient(to top right,  #b97186 0%, #ee7d84 100%)",
                        background_clip="text",
                        transition="all 600ms",
                    ),
                    transition="all 600ms",
                    size="3xl",
                    color="white",
                    text_align="center",
                    line_height="4.5rem",
                ),
                pc.heading(
                    "Password Manager.",
                    text_align="center",
                    color="white",
                    size="3xl",
                    transition="all 600ms",
                ),
                pc.text(
                    "Keep your passwords safe with our easy-to-use application.",
                    color="white",
                    line_height="5rem",
                    font_size="md",
                    text_align="center",
                    transition="all 600ms",
                ),
                min_width="600px",
                w="100%",
            ),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.container(
                pc.icon(
                    tag="add",
                    color="white",
                    font_size="1.25rem",
                ),
                border="1px dashed white",
                w="250px",
                h="70px",
                border_radius="8px",
                cursor="pointer",
                display="flex",
                align_items="center",
                justify_content="center",
                _hover={"bg": "#3c4661"},
                on_click=State.toggle_left_drawer,
            ),
            pc.hstack(
                pc.foreach(
                    State.data_list,
                    display_data,
                ),
                min_width="1000px",
                width="100%",
                h="200px",
                display="flex",
                align_items="center",  # Set to center
                justify_content="center",
                direction="row",
            ),
        ),
        bg="#2d374e",
        width="100%",
        height="100vh",
        display="flex",
        display_direction="column",
        align_items="center",
        justify_content="start",
        padding_top="10rem",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
