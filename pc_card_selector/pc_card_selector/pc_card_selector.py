import pynecone as pc
import asyncio


class State(pc.State):
    """The app state."""

    uid: list = [0, 1, 2]
    labels: list = ["Personal", "Streaming", "Shopping"]

    bg: str = "#1b1f2d"
    clicked_bg: str = "#5970ec"

    unclicked_scale: str = "scale(0.65)"
    clicked_scale: str = "scale(0.725)"

    clicked_box: str = "2px solid #4062F6"
    unclicked_box: str = "2px solid transparent"

    off_box_bg: str = "transparent"
    on_box_bg: str = "#313a51"

    off_card_scale: str = "scale(0.65)"
    on_card_scale: str = "scale(0.70)"

    start_flash: str = "translate(15px, 0px) rotate(35deg)"
    start_opacity: str = "50%"

    end_flash: str = "translate(120px, 0px) rotate(35deg)"
    # skew(-12deg, 0deg)
    end_opacity: str = "0%"

    selected_text: str = "white"
    unselected_text: str = "lightgray"

    item_list: list[list] = []

    for i in range(len(uid)):
        item_list.append(
            [
                uid[i],
                labels[i],
                unclicked_scale,
                bg,
                unclicked_box,
                off_box_bg,
                off_card_scale,
                start_flash,
                start_opacity,
                unselected_text,
            ]
        )

    async def animate_button_start(self, values):
        index = values[0]
        new_item_list = []
        for (uid, v1, _, v2, v3, v4, _, v6, v7, v8) in self.item_list:
            new_item = [uid, v1, v2, v3, v4, v6, v7, v8]
            if index == uid:
                new_item.insert(2, self.clicked_scale)
                new_item.insert(6, self.on_card_scale)
            else:
                new_item.insert(2, self.unclicked_scale)
                new_item.insert(6, self.off_card_scale)
            new_item_list.append(new_item)

        self.item_list = new_item_list

    async def animate_button_end(self, values):
        await asyncio.sleep(0.35)

        index = values[0]
        new_item_list = []
        for (uid, v1, _, v2, v3, v4, _, v6, v7, v8) in self.item_list:
            new_item = [uid, v1, v2, v3, v4, v6, v7, v8]
            if index == uid:
                new_item.insert(2, self.unclicked_scale)
                new_item.insert(6, self.off_card_scale)
            else:
                new_item.insert(2, self.unclicked_scale)
                new_item.insert(6, self.off_card_scale)
            new_item_list.append(new_item)

        self.item_list = new_item_list

    def set_clicked_box(self, values: list):
        index = values[0]
        new_item_list = []
        for (uid, v1, v2, _, _, _, v3, _, _, _) in self.item_list:
            new_item = [uid, v1, v2, v3]
            if index == uid:
                new_item.insert(3, self.clicked_bg)
                new_item.insert(4, self.clicked_box)
                new_item.insert(5, self.on_box_bg)
                new_item.insert(7, self.end_flash)
                new_item.insert(8, self.start_opacity)
                new_item.insert(9, self.selected_text)
            else:
                new_item.insert(3, self.bg)
                new_item.insert(4, self.unclicked_box)
                new_item.insert(5, self.off_box_bg)
                new_item.insert(7, self.start_flash)
                new_item.insert(8, self.end_opacity)
                new_item.insert(9, self.unselected_text)
            new_item_list.append(new_item)

        self.item_list = new_item_list


def mini_credit_card(scale, flash, opacity):
    return pc.container(
        # mini card
        pc.container(
            pc.container(
                width="20px",
                height="100px",
                position="absolute",
                opacity=opacity,
                padding="0px",
                transform=flash,
                transition="transform 555ms cubic-bezier(0.19, 1, 0.22, 1)",
                z_index="4",
                bg="#fff",
                margin="auto",
                top="-50",
                left="-10",
            ),
            background_image="url(https://img.icons8.com/fluency/1024/null/mastercard-credit-card.png)",
            background_repeat="no-repeat",
            background_position="center",  # centers the image
            background_size="100%",
            width="55px",
            height="36px",
            border_radius="4px",
            margin="auto 0px 0px 0px",
            box_shadow="0px 2px 4px 0px rgba(0, 0, 0, 0.89)",
            z_index="2",
            transform=scale,
            transition="transform 0.35s",
            overflow="hidden",
            padding="0px",
            display="flex",
        ),
        width="100%",
        height="60px",
        padding="0px",
        padding_right="10px",
        margin="0px",
        display="flex",
        align_items="flex-end",
        flex_wrap="wrap",
        align_content="center",
        justify_content="flex-end",
    )


def click_button(scale, bg):
    return pc.button(
        transform=scale,
        transition="all 0.35s ease transform 0.35s",
        border_radius="150px",
        background=bg,
        # box_shadow="inset 4px 4px 8x #0e1017, inset -4px -4px 8px #282e43",
        # box_shadow="10px 10px 10px 10px rgba(0, 0, 0, 0.89)",
        color_scheme="None",
        border="2px solid #45485f",
    )


def card_container(values):
    return pc.container(
        pc.hstack(
            pc.hstack(
                click_button(values[2], values[3]),
                pc.text(
                    values[1],
                    color=values[9],
                    font_weight="bold",
                    transition="all 0.35s",
                ),
            ),
            mini_credit_card(values[6], values[7], values[8]),
            spacing="20px",
        ),
        min_width="320px",
        height="62px",
        padding="0 20px",
        border_radius="6px",
        border=values[4],
        background_color=values[5],
        transition="all 0.5s ease",
        position="relative",
        cursor="pointer",
        on_click=[
            lambda: State.set_clicked_box(values),
            lambda: State.animate_button_start(values),
            lambda: State.animate_button_end(values),
        ],
        _hover={
            "border_color": "#4062F6",
            "background_color": "#313a51",
        },
    )


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.foreach(
                State.item_list,
                card_container,
            ),
            transform="scale(1.45)",
            # box_shadow="0 30px 60px 0 rgba(90, 116, 148, 0.4)",
            padding="20px",
            border_radius="8px",
        ),
        bg="#313b44",
        wdith="100%",
        height="100vh",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
    )


app = pc.App(state=State)
app.add_page(index)
app.compile()
