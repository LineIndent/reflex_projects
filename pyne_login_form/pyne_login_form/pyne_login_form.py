import pynecone as pc


def get_input_fields(icon: str, placeholder: str, _type: str):
    return pc.container(
        pc.hstack(
            pc.icon(
                tag=icon,
                color="white",
                fontSize="11px",
            ),
            pc.input(
                placeholder=placeholder,
                border="0px",
                focus_border_color="None",
                color="white",
                fontWeight="semibold",
                fontSize="11px",
                type_=_type,
            ),
        ),
        borderBottom="0.01px solid grey",
        width="300px",
        height="45px",
    )


def index():
    login_container = pc.container(
        pc.vstack(
            pc.container(height="65px"),
            pc.container(
                pc.text(
                    "Sign In",
                    fontSize="28",
                    fontWeight="bold",
                    color="white",
                    letterSpacing="2px",
                ),
                width="250px",
                center_content=True,
            ),
            pc.container(
                pc.text(
                    "Pynecone UI Concept Using Python",
                    fontSize="12",
                    fontWeight="bold",
                    color="gray",
                    letterSpacing="0.25px",
                ),
                width="250px",
                center_content=True,
            ),
            pc.container(height="50px"),
            get_input_fields("email", "Email", ""),
            pc.container(height="5px"),
            get_input_fields("lock", "Password", "password"),
            pc.container(height="5px"),
            pc.container(
                pc.text(
                    "Forgot Password?",
                    color="white",
                    fontSize=11,
                    textAlign="end",
                ),
            ),
            pc.container(height="55px"),
            pc.container(
                pc.button(
                    pc.text(
                        "Sign In",
                        color="white",
                        fontSize=11,
                        weight="bold",
                    ),
                    width="300px",
                    height="45px",
                    color_scheme="blue",
                ),
            ),
        ),
        width="400px",
        height="75vh",
        center_content=True,
        bg="#1D2330",
        borderRadius="15px",
        boxShadow=" 41px -41px 82px #0d0f15,-41px 41px 82px #2d374b",
    )

    # main bg stack
    _main_stack_ = pc.container(
        login_container,
        center_content=True,
        justifyContent="center",
        maxWidth="auto",
        height="100vh",
        bg="#1D2330",
    )

    return _main_stack_


app = pc.App()
app.add_page(index)
app.compile()
