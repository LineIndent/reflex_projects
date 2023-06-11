""" Pynecone animated signin form """
# modules
import pynecone as pc

# import pyrebase

# I'll be using pyrebase for a simple authentication with python.
# I'm asuming pyrebase is already installed via pip, and a account on firebase console google is already made.

# get the config path for the firebase
config = {
    "apiKey": "AIzaSyBtQmghGjtHk6iLYtMFuP8ChIODXVf2GGk",
    "authDomain": "pynecone-auth.firebaseapp.com",
    "projectId": "pynecone-auth",
    "storageBucket": "pynecone-auth.appspot.com",
    "messagingSenderId": "183383982441",
    "appId": "1:183383982441:web:226b9db6fad2be3dcb7df8",
    "databaseURL": "",
}

# initilize the pyrebase module
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()


# create the main state class
class State(pc.State):
    # define email properties
    email_width = "0px"
    email = "What's your email?"
    email_value = ""
    email_underline = "0px solid white"

    # define checkbox email properties
    email_check_opacity = "0%"
    email_status = False
    email_check_pos = "translate(5px, 0px)"

    # define password properties
    password_width = "0px"
    password = "Enter your password."
    password_value = ""
    password_underline = "0px solid white"

    # define checkbox password properties
    password_check_opacity = "0%"
    password_status = False
    password_check_pos = "translate(5px, 0px)"

    # define box dimensions
    box_width = "60px"
    box_height = "60px"

    # define the singin result proeprties
    result_sign_in = ""
    result_pos = "transform(0px, 0px)"
    result_opacity = "0%"
    result_color = ""

    # function to open the sign in form
    def open_box(self):
        self.box_width = "350px"
        self.email_width = "300px"
        self.email_underline = "2px solid white"
        # condition so that email underline doesnt change color
        if self.email_status:
            # this means that if the status is True, it means that the email is correct and we should keep the underline green
            self.email_underline = "2px solid green"

    # function to check email
    def on_check_email(self, email_value):
        self.email_value = email_value
        # we want to check to see if several mail domains are in the email value in order to show the password input
        if any(
            domain in self.email_value
            for domain in ("@gmail.com", "@hotmail.com", "@aol.com")
        ):
            self.email_underline = "2px solid green"
            self.box_height = "110px"
            # so once we expand, we can show the password input
            self.password_width = "300px"
            self.password_underline = "2px solid white"
            # highlight correct email
            self.email_check_pos = "trasnform(-250px, 0)"
            self.email_check_opacity = "100%"
            self.email_status = True

    def on_check_password(self, password_value):
        self.password_value = password_value
        # now we check the password
        # this is just a basic password check.
        # in real production, other factors need to be taken into consideration
        if len(self.password_value) >= 8:
            self.box_height = "250px"
            self.password_underline = "2px solid green"
            self.password_check_pos = "transform(-250px, 0px)"
            self.password_check_opacity = "100%"
            self.password_status = True

    def user_sign_in(self):
        # now in the firebase auth, I have already created a user with a password. Let me deosntrate this again.
        # so now I have a user with the email and pass I gave it.
        # let's try and authenticate it now
        try:
            user = auth.sign_in_with_email_and_password(
                # we pass in the values of the input texts
                # not dot value, underscroe value!
                self.email_value,
                self.password_value,
            )
            # now if user is registered:
            if user["registered"]:
                self.result_color = "green"
                self.result_sign_in = "Sign In Successful!"
                self.result_pos = "transform(0px, 10px)"
                self.result_opacity = "100%"
            pass
        except Exception as e:
            # if an exception is raised:
            self.result_color = "red"
            self.result_sign_in = "Invalid Email and/or Password. Try Again!"
            self.result_pos = "transform(0px, 10px)"
            self.result_opacity = "100%"


# we'll be using 2 inputs, so let's c reate a function to minimze the code clutter
def input_field(input_width, text_value, holder, func_change, _type):
    return pc.input(
        width=input_width,
        value=text_value,
        transition="width 0.5s ease 0.65s",
        placeholder=holder,
        color="white",
        border="None",
        font_size="13px",
        letter_spacing="0.5px",
        focus_border_color="None",
        type_=_type,
        on_change=func_change,
    )


# create a function for the main signin component
def input_box():
    return pc.container(
        pc.vstack(
            pc.spacer(),
            pc.hstack(
                pc.container(
                    input_field(
                        State.email_width,
                        State.email_value,
                        State.email,
                        lambda: State.on_check_email(),
                        "text",
                    ),
                    padding="0px",
                    width=State.email_width,
                    border_bottom=State.email_underline,
                    transition="width 0.65s ease 0.65s",
                ),
                # now for the checkmark
                pc.checkbox(
                    color_scheme="green",
                    opacity=State.email_check_opacity,
                    is_checked=State.email_status,
                    transform=State.email_check_pos,
                    transition="opacity 0.8s, transform 0.65s ease",
                ),
            ),
            pc.spacer(),
            # repeate the same for the password
            # but first let's handle some logic for the email.
            pc.hstack(
                pc.container(
                    input_field(
                        State.password_width,
                        State.password_value,
                        State.password,
                        lambda: State.on_check_password(),
                        "password",
                    ),
                    padding="0px",
                    width=State.password_width,
                    border_bottom=State.password_underline,
                    transition="width 0.65s ease 0.65s",
                ),
                # now for the checkmark
                pc.checkbox(
                    color_scheme="green",
                    opacity=State.password_check_opacity,
                    is_checked=State.password_status,
                    transform=State.password_check_pos,
                    transition="opacity 0.8s, transform 0.65s ease",
                ),
            ),
            pc.spacer(),
            # finally, a button where we can submit our info to firebase to be authenticated
            pc.container(
                pc.button(
                    "Sign In",
                    width="250px",
                    height="45px",
                    color_scheme="blue",
                    on_double_click=lambda: State.user_sign_in(),
                ),
                min_width="auto",
                height="50px",
                justify_content="center",
                center_content=True,
            ),
            pc.spacer(),
        ),
        width=State.box_width,
        height=State.box_height,
        bg="#1D2330",
        border_radius="5px",
        padding="8px",
        display="grid",
        position="relative",
        overflow="hidden",
        transition="width 0.65s, height 0.65s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
        on_click=lambda: State.open_box(),
    )


# create the main index page for the signin
def index():
    # our mani UI goes in here
    return pc.container(
        # we'll need a certical stack because the form will have two main sections.
        pc.vstack(
            # we'll add the main form here later
            input_box(),
            # here we'll add the result component
            pc.container(
                pc.text(
                    # the paramters that can change with each event should be variables set in the state class.
                    State.result_sign_in,
                    transform=State.result_pos,
                    opacity=State.result_opacity,
                    color=State.result_color,
                    font_size="20px",
                    font_weight="bold",
                    transition="opacity 0.55, transform 0.55 ease",
                ),
                min_width="auto",
                height="60px",
                display="grid",
                place_items="center",
            ),
        ),
        height="100vh",
        display="grid",
        position="relative",
        overflow="hidden",
        place_items="center",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
