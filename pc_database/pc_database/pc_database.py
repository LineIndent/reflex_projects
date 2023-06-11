from pcconfig import config
import pynecone as pc
import datetime
import uuid
import asyncio


def generate_id():
    return str(uuid.uuid4())


class Task(pc.Model, table=True):
    uuid: str
    date: str
    task: str


def add_task_to_db(uid, date, task):
    with pc.session() as session:
        session.add(
            Task(
                uuid=uid,
                date=date,
                task=task,
            )
        )
        session.commit()


class State(pc.State):
    task: str
    task_list: list[list]

    on_delete: str = "translate(-20px, 0px)"
    off_delete: str = "translate(0px, 0px)"

    on_opacity_delete: str = "100%"
    off_opacity_delete: str = "0%"

    def update_task_field(self, task):
        self.task = task

    async def show_delete(self, task):
        uuid = task[0]
        self.task_list = [
            [uid, date, task, self.on_delete, self.on_opacity_delete]
            if uid == uuid
            else [uid, date, task, delete_pos_x, delete_opacity]
            for uid, date, task, delete_pos_x, delete_opacity in self.task_list
        ]
        await asyncio.sleep(0.01)

    async def hide_delete(self, task):
        uuid = task[0]
        self.task_list = [
            [uid, date, task, self.off_delete, self.off_opacity_delete]
            if uid == uuid
            else [uid, date, task, delete_pos_x, delete_opacity]
            for uid, date, task, delete_pos_x, delete_opacity in self.task_list
        ]
        await asyncio.sleep(0.01)

    async def delete_task(self, task):
        uuid = task[0]
        with pc.session() as session:
            task_to_delete = session.query(Task).filter_by(uuid=uuid).first()
            session.delete(task_to_delete)
            session.commit()

        self.task_list = [
            [uid, date, task, delete_pos_x, delete_opacity]
            for uid, date, task, delete_pos_x, delete_opacity in self.task_list
            if uid != uuid
        ]

    async def add_task_to_list(self):
        self.task_list += [
            [
                generate_id(),
                datetime.datetime.now().strftime("%B %d, %Y  %H:%M"),
                self.task,
                self.off_delete,
                self.off_opacity_delete,
            ]
        ]

        add_task_to_db(
            generate_id(),
            datetime.datetime.now().strftime("%B %d, %Y  %H:%M"),
            self.task,
        )

        self.task = ""

    @pc.var
    def get_tasks_from_db(self):
        with pc.session() as session:
            tasks = session.query(Task.uuid, Task.date, Task.task).all()

            task_list = [
                [
                    task.uuid,
                    task.date,
                    task.task,
                    self.off_delete,
                    self.off_opacity_delete,
                ]
                for task in tasks
            ]

            self.task_list = task_list


def create_delete_button(transform, opacity, delete_func):
    return pc.container(
        pc.button(
            pc.icon(
                tag="delete",
                color="red",
            ),
            width="28px",
            height="28px",
            color_scheme="None",
            on_click=delete_func,
        ),
        width="24px",
        justify_content="center",
        center_content=True,
        transform=transform,
        opacity=opacity,
        transition="transform 0.65s, opacity 0.55s ease",
    )


def display_task(task):
    return pc.container(
        pc.hstack(
            pc.container(
                pc.vstack(
                    pc.container(
                        pc.text(
                            task[1],
                            font_size="8px",
                            font_weight="bold",
                            color="#374151",
                        ),
                    ),
                    pc.container(
                        pc.text(
                            task[2],
                            font_size="14px",
                            font_weight="bold",
                        ),
                    ),
                    spacing="1px",
                ),
                padding="0px",
            ),
            create_delete_button(task[3], task[4], lambda: State.delete_task(task)),
            width="320px",
            padding="0px",
        ),
        width="320px",
        height="60px",
        border_bottom="1px solid #9ca3af",
        padding="0px",
        border_raidus="0px",
        display="flex",
        justify_content="space-between",
        align_items="center",
        overflow="hidden",
        on_mouse_over=lambda: State.show_delete(task),
        on_mouse_leave=lambda: State.hide_delete(task),
    )


def task_input_field() -> pc.Component:
    return pc.container(
        pc.vstack(
            pc.container(
                pc.text(
                    "Full-Stack To-Do App With Pynecone",
                    font_size="24px",
                    font_weight="900",
                    style={
                        "background-clip": "text",
                        "background-image": "linear-gradient(to right, #4b79a1, #283e51, #4b79a1)",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    },
                ),
                justify_content="center",
                center_content=True,
            ),
            pc.spacer(),
            pc.hstack(
                pc.input(
                    value=State.task,
                    border="None",
                    width="300px",
                    height="45px",
                    border_bottom="1px solid black",
                    border_radius="0px",
                    focus_border_color="None",
                    on_change=lambda: State.update_task_field(),
                ),
                pc.button(
                    pc.icon(tag="arrow_right", color="black", font_size="14px"),
                    font_size="21px",
                    width="45px",
                    height="45px",
                    color_scheme="None",
                    padding_top="1%",
                    border_radius="0px",
                    border_bottom="1px solid black",
                    on_click=lambda: State.add_task_to_list(),
                ),
                spacing="0px",
            ),
        ),
    )


def index() -> pc.Component:

    return pc.center(
        pc.vstack(
            pc.container(
                task_input_field(),
            ),
            pc.spacer(),
            pc.spacer(),
            pc.spacer(),
            pc.container(
                pc.vstack(
                    pc.foreach(
                        State.task_list,
                        display_task,
                    ),
                    width="450px",
                    hieght="500px",
                    overflow="hidden",
                ),
                width="450px",
                height="500px",
                overflow="auto",
                padding_top="5%",
                padding_bottom="5%",
                border_radius="10px",
                box_shadow=" 5px -5px 3px #cacccd, -5px 5px 3px #ffffff",
            ),
        ),
        background="#ebedee",
        max_width="auto",
        height="100vh",
        display="grid",
        place_items="center",
    )


style = {
    pc.Text: {
        "color": "black",
    },
    pc.Input: {
        "color": "black",
    },
}

# Add state and page to the app.
app = pc.App(state=State, style=style)
app.add_page(index)
app.compile()
