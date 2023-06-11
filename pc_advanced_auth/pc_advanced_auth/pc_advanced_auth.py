# Pynecone Modules
import pynecone as pc

# Google 2.0 Authentication Modules
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

# Firebase API Modlues
import firebase_admin
from firebase_admin import credentials, auth

# Python Modules
import asyncio

CLIENT_SECRET = "./client_secret.json"
REDIRECT_URI: str = "http://localhost:3000/auth-user"
SCOPES: list = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)


class State(pc.State):
    # State mgmt: user's email address
    email: str

    # Function generates an authorization url that redirects user's to Google's sign in page
    def route_to_authorization_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file=CLIENT_SECRET, scopes=SCOPES
        )

        flow.redirect_uri = REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )

        return pc.redirect(authorization_url)

    # Second part of authorization with Google => get's user data (email + sub claim ID token) and creates an entry in Firebase Authentication system.
    def get_authorized_response(self):
        # Get the query paramters of the response URL => need the state and code
        authorization_response = self.get_query_params()
        state = authorization_response["state"]
        code = authorization_response["code"]

        # Construct the URL string from the authorization response dictionary
        authorization_response_url = f"https://localhost:3000/auth-user?state={state}&code={code}&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=consent"

        # Create another Flow instnace but passing in the state this time
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file=CLIENT_SECRET,
            scopes=SCOPES,
            state=state,
        )

        # Construct the redirect URI again
        flow.redirect_uri = REDIRECT_URI

        # Completes the Authorization Flow and obtains an access token.
        flow.fetch_token(authorization_response=authorization_response_url)

        try:
            credentials = flow.credentials

        except ValueError as ex:
            # Handle the ValueError exception
            print("ValueError: {}".format(str(ex)))

        try:
            idinfo = id_token.verify_oauth2_token(
                credentials._id_token, requests.Request(), None
            )

            userid = idinfo["sub"]
            useremail = idinfo["email"]

            try:
                auth.get_user_by_email(email=useremail)
                self.email = useremail

            except auth.UserNotFoundError as ex:
                auth.create_user(uid=userid, email=useremail, email_verified=True)
                self.email = useremail

            asyncio.sleep(1)

            return pc.redirect(
                f"http://localhost:3000/auth-user?state={state}&code={code}&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=consent"
            )

        except GoogleAuthError as ex:
            # Handle the GoogleAuthError exception
            print("Error: {}".format(str(ex)))

        except ValueError as ex:
            # Handle the ValueError exception
            print("ValueError: {}".format(str(ex)))


# UI components for signin form


# method to create a input field
def create_input_field(card_title):
    return pc.container(
        pc.vstack(
            pc.text(
                card_title,
                color="black",
                font_size="0.85rem",
                width="80%",
            ),
            pc.input(
                width="80%",
                height="45px",
                bg="None",
                font_size="1rem",
                color="white",
                font_family="Source Sans Pro, sans-serif",
                _focus={
                    "box_shadow": "0px 10px 20px -13px rgba(32, 56, 117, 0.35)",
                },
            ),
        ),
    )


@pc.route(route="/auth-user", on_load=State.get_authorized_response)
def login():
    return pc.vstack(
        pc.heading(
            "Signed In As: ",
            pc.span(State.email, as_="mark"),
            font_size="3rem",
            font_weight="bold",
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        w="100%",
        h="100vh",
    )


@pc.route(route="/")
def index() -> pc.Component:
    return pc.center(
        pc.container(
            pc.vstack(
                pc.spacer(),
                pc.text(
                    "Pynecone Advanced Authentication",
                    font_size="2rem",
                    color="black",
                    text_align="center",
                    font_weight="bold",
                ),
                pc.spacer(),
                pc.spacer(),
                pc.spacer(),
                pc.container(
                    pc.hstack(
                        pc.image(
                            src="https://img.icons8.com/color/480/null/google-logo.png",
                            width="28px",
                            height="auto",
                        ),
                        pc.spacer(),
                        pc.text("Log in with Google"),
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        font_weight="500",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border="1px solid #bbbbbb",
                    border_radius="8px",
                    w="70%",
                    h="45px",
                    cursor="pointer",
                    transition="all 350ms ease",
                    on_click=State.route_to_authorization_url,
                    _hover={
                        "box_shadow": "0px 10px 20px -13px rgba(32, 56, 117, 0.35)"
                    },
                ),
                pc.spacer(),
                pc.spacer(),
                pc.container(
                    pc.hstack(
                        pc.divider(
                            width="150px",
                            orientation="horizontal",
                            border_color="#bbbbbb",
                        ),
                        pc.text("or", color="gray"),
                        pc.divider(
                            width="150px",
                            orientation="horizontal",
                            border_color="#bbbbbb",
                        ),
                    ),
                    width="70%",
                    height="45px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                pc.spacer(),
                create_input_field("Email"),
                create_input_field("Password"),
                pc.spacer(),
                pc.spacer(),
                pc.spacer(),
                pc.button(
                    "Log In", bg="black", width="75%", height="45px", color="white"
                ),
            ),
            min_width=["200px", "200px", "200px", "200px", "250px"],
            w="100%",
            h="550px",
            box_shadow="0 0 10px 10px rgba(0, 0, 0, 0.25)",
            border_radius="10px",
            bg="#fff",
            display="flex",
            align_items="start",
            justify_content="center",
            padding="20px",
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        w="100%",
        h="100vh",
        background="url(https://source.unsplash.com/E8Ufcyxz514/2400x1823) center / cover no-repeat fixed",
        padding="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.compile()
