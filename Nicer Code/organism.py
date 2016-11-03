class Organism(object):
    def __init__(self, pos, envdims):
        self.pos = pos
        self.envdims = envdims
        self.cull = False
        self.size = 5
        self.brain = ANN(ORGANISM_BRAIN, Perceptron)

    def draw(self, canvas):
        canvas.create_line(
                self.pos[0], self.pos[1],
                self.pos[0] - ORGANISM_TAILSIZE * cos(self.orientation),
                self.pos[1] - ORGANISM_TAILSIZE * sin(self.orientation),
                fill = "black"
            )

        canvas.create_oval(
                self.pos[0] - ORGANISM_HEADSIZE, self.pos[1] - ORGANISM_HEADSIZE,
                self.pos[0] + ORGANISM_HEADSIZE, self.pos[1] + ORGANISM_HEADSIZE,
                fill = "red"
            )

    def feed(self, food):
        self.size += food

    def update(self, inputs):
        self.size += PHOTOSYNTHESIS_RATE
        self.size *= ORGANISM_SIZE_LOSS

        if self.size = 0:
            cull = True

        [turn, direction] = self.brain.run(inputs)

        delta_angle = turn*(2*direction - 1)*ORGANISM_TURN_AMOUNT

        self.move(delta_angle)

    def seed(self):
        self.brain.seed_network()

    def move(self, angle):
        """ turns and moves forward by a set distance """
        self.orientation += angle

        new_x = self.x + ORGANISM_SPEED * cos(self.orientation)
        new_y = self.y + ORGANISM_SPEED * sin(self.orientation)

        """ bounce off the walls """
        if new_x <= 0 or new_x >= ENV_WIDTH - 1:
            self.orientation = pi - self.orientation
            new_x = 0 if new_x <= 0 else ENV_WIDTH - 1

        if new_y <= 0 or new_y >= ENV_HEIGHT - 1:
            self.orientation *= -1
            new_y = 0 if new_y <= 0 else ENV_HEIGHT - 1

        self.x = new_x
        self.y = new_y
