""" Pynecone Memory Match Game """
# modules
import pynecone as pc
import random
import asyncio


class State(pc.State):
    # to set the opacity, we need to create states for all the tiles/emojies
    # now initially this was meant to be a 6x6 grid, but I've made it a little smaller for demo puposes.

    # get opacity states
    # it's important to define the object type
    # the range num can be changed, I've set it to 36 from the original 6x6 grid
    emoji_list: list[list] = [[i, "0%"] for i in range(36)]

    # now we can work a little more on the states
    count: int = 0
    track: list = []
    score: int = 0
    result: str  # we don't need to set it to anything, but make sure the type is defined.

    # first we need a function that reveals the emoji
    def reveal_emoji(self, emoji, emoji_type):
        # this function gets two main paramters, the index of the emoji, i,e where it is in the list, and the actual paramters of it's opacity
        index = emoji[0]
        # now, we want to update the emoji_list to reflect the changes, which are turning the clicked emoji's opacity back to 100 percent
        self.emoji_list = [
            # this is not too complex to read but it simply says that if the index, i.e. what we clicked is equal or is the same to i, which is the contents of the self.emoji_list, if so change the opacity to 100, otherwise, just keep everything else the same
            [i, "100%"] if i == index else [i, opacity]
            for i, opacity in self.emoji_list
        ]

        # increment the count which tracks the number of visible emojis in the grid
        self.count += 1
        # append the track list for comparision later
        self.track.append((emoji_type, emoji))

    # great, so now we can show what;s being clicked.
    # next we need a function that checks two clicked emojis and determines if they are identical or not.
    # we'll need a async func since I will use sleep for some delay effects
    async def check_emoji(self):
        # recall that we have a count that keeps track of the clicks.
        if self.count == 2:
            # if it's two we know that the players clicked two emojies
            # we then need to check first if the two emojies are identical
            # notes: self.track is a tuple!
            if self.track[0][0] == self.track[1][0]:
                # if they are identical we'll finish this later..
                # so finally, let's keep track of the identical flips
                # it's simple here, all we need to do is keep track of the scores and check to see if the player has won
                self.score += 1
                if (
                    self.score == 8
                ):  # again, these can be changes to make hte game flexiable
                    self.result = "Congrats! You matched all the Emojies!!"
            else:
                # if they're not the same, we want to hide them again
                # so we need a list of indicies like we did before in the above function
                # note: we are extracting the second item of the tuple
                indicies = [e[1][0] for e in self.track]
                # now, just like before, we update the main list of opacities
                self.emoji_list = [
                    [i, "0%"] if i in indicies else [i, opacity]
                    for i, opacity in self.emoji_list
                ]

            # finally, reset the count and empty the list
            self.count = 0
            self.track = []

        # sleep
        await asyncio.sleep(2)


# so before we get to the state class, let's crete a game class where we load the grid and emojies.
# this class can be scaled and changed easily, espec. iwth regards to the levels and such.
class MemoryMatchGame:
    def __init__(self):
        # we need to create several instances up front
        # these get created when we instantized the class
        self.stage: int = 2  # i've set this to 2, it can be changed later
        self.emojis: list = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎"]
        # our main game grid
        self.game_grid = pc.vstack(spacing="15px")
        # the create function goes here...
        self.create_board()

    def create_board(self):
        # we want to make sure we have pairs of emojies in the grid
        emojis = self.emojis[: self.stage * 2] * self.stage * 2
        # randomize the list, i.e. shuffle
        random.shuffle(emojis)
        # set a counter to track some paramters
        count = 0
        items = []
        # now we can create the grid
        for _ in range(self.stage * 2):
            row = pc.hstack(spacing="15px")
            for __ in range(self.stage * 2):
                row.children.append(
                    pc.container(
                        pc.text(
                            # get the emoji from the list
                            emojis[count],
                            font_size="32px",
                            cursor="pointer",
                            transition="opacity 0.55s ease 0.35s",
                            # now we can set each opacity from the state class
                            # recall that the list is a nested list, therefore we need to index it
                            opacity=State.emoji_list[count][1],
                            # here we need event chains, i.e list of events becuase that's how the pynecone states work
                            on_click=lambda: [
                                State.reveal_emoji(
                                    # pass in the paramters
                                    State.emoji_list[count],
                                    emojis[count],
                                ),
                                # make sure to add the function in the event chain
                                State.check_emoji(),
                            ],
                        ),
                        width="58px",
                        height="58px",
                        bg="#1e293b",
                        border_radius="4px",
                        justify_content="center",
                        center_content=True,
                        cursor="pointer",
                    )
                )

                count += 1
            items.append(row)

        self.game_grid.children = items
        return self.game_grid


def index() -> pc.Component:
    # our main UI component
    return pc.container(
        pc.vstack(
            # title
            # pc.text(
            #     "Emoji Memory Match",
            #     font_size="55px",
            #     font_weight="extrabold",
            #     color="black",
            # ),
            pc.spacer(),
            # our game instance here...
            game.game_grid,  # call the game grid since we have access to it
            pc.spacer(),
            # result text
            pc.text(
                State.result,
                font_size="25px",
                font_weight="extrabold",
                color="black",
            ),
            spacing="25px",
        ),
        bg="#0284c7",
        height="100vh",
        max_width="auto",
        display="grid",
        position="relative",
        overlay="hidden",
        place_items="center",
    )


# instantize the class
game = MemoryMatchGame()

app = pc.App(state=State)
app.add_page(index)
app.compile()

# so the game is working well. Some adjustments can def. be made, but over all it's scalable and playable. Cheers!
