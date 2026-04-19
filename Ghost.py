
from GameObject import GameObject
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals
from GameDefs import Pos

# Ghost AI implemented as a finite state machine (FSM).
# State transitions are handled by transition_table.
# Movement behaviour for each state is handled separately by action_table.
# This separates FSM logic from movement logic, making the code easier to extend and modify.
class Ghost(GameObject):
    # State constants
    CHASE = "CHASE"
    FLEE = "FLEE"
    RETURN_HOME = "RETURN_HOME"
    GAME_OVER = "GAME_OVER"

    # Event constants
    PILL_EATEN = "PILL_EATEN"
    PILL_EXPIRED = "PILL_EXPIRED"
    GHOST_EATEN = "GHOST_EATEN"
    PACMAN_EATEN = "PACMAN_EATEN"

    # Home position constants
    HOME_POS = Pos(1,1)

    # Define transition table
    # FSM transition rules:
    # current state + event -> next state
    # These transitions match the assignment state diagram.
    TRANSITION_TABLE = {
        CHASE: {
            PILL_EATEN: FLEE,
            PACMAN_EATEN: GAME_OVER,
        },
        FLEE: {
            GHOST_EATEN: RETURN_HOME,
            PILL_EXPIRED: CHASE,
        },
        RETURN_HOME: {
            PILL_EXPIRED: CHASE,
        },
        GAME_OVER: {
        }
    }
    def __init__(self, p):
        super().__init__(p, SpriteType.GHOST)

        # Initialise state
        self.state = Ghost.CHASE

        # Define action table
        # State action rules:
        # each state maps to a movement behaviour
        self.action_table = {
            Ghost.CHASE: self._chase_action,
            Ghost.FLEE: self._flee_action,
            Ghost.RETURN_HOME: self._return_home_action,
            Ghost.GAME_OVER: self._game_over_action
        }

    # CHASE -> move towards Pacman
    # FLEE -> move away from Pacman
    # RETURN_HOME -> move towards home position
    # GAME_OVER -> do not move
    def _chase_action(self):
        return self._move_towards(globals.pacman.position)
    def _flee_action(self):
        return self._move_away(globals.pacman.position)
    def _return_home_action(self):
        return self._move_towards(Ghost.HOME_POS)
    def _game_over_action(self):
        return Direction.NONE


    def _transition_to(self, new_state):
        # Centralise state changes in one place for easier future extension.
        self.state = new_state

    # Apply a state transition if one is defined for the current state and event.
    # Otherwise, remain in the current state.
    def _handle_event(self, event):
        next_state = Ghost.TRANSITION_TABLE.get(self.state, {}).get(event)
        if next_state is not None:
            self._transition_to(next_state)

    # Return the next movement direction based on the current FSM state.
    def move(self):
        # If an unexpected state is encountered, default to no movement.
        action = self.action_table.get(self.state, lambda: Direction.NONE)
        return action()

    def _direction_is_clear(self, direction):
        newPos = Pos(self.position.x, self.position.y)

        if direction == Direction.LEFT:
            newPos.x -= 1
        elif direction == Direction.RIGHT:
            newPos.x += 1
        elif direction == Direction.UP:
            newPos.y -= 1
        elif direction == Direction.DOWN:
            newPos.y += 1
        else:
            return True

        newPos.x = (newPos.x + globals.gameSize) % globals.gameSize
        newPos.y = (newPos.y + globals.gameSize) % globals.gameSize

        return globals.game.checkPosition(newPos) != SpriteType.WALL

    def _candidate_directions_from_delta(self, dx, dy):
        candidates = []

        # If there is no offset, there is no preferred movement.
        if dx == 0 and dy == 0:
            return [Direction.NONE]

        # Primary and secondary preferences based on the larger absolute distance.
        if abs(dx) >= abs(dy):
            if dx > 0:
                primary = Direction.RIGHT
                opposite_primary = Direction.LEFT
            else:
                primary = Direction.LEFT
                opposite_primary = Direction.RIGHT

            candidates.append(primary)

            if dy > 0:
                secondary = Direction.DOWN
                opposite_secondary = Direction.UP
                candidates.append(secondary)
            elif dy < 0:
                secondary = Direction.UP
                opposite_secondary = Direction.DOWN
                candidates.append(secondary)
            else:
                secondary = None
                opposite_secondary = None

        else:
            if dy > 0:
                primary = Direction.DOWN
                opposite_primary = Direction.UP
            else:
                primary = Direction.UP
                opposite_primary = Direction.DOWN

            candidates.append(primary)

            if dx > 0:
                secondary = Direction.RIGHT
                opposite_secondary = Direction.LEFT
                candidates.append(secondary)
            elif dx < 0:
                secondary = Direction.LEFT
                opposite_secondary = Direction.RIGHT
                candidates.append(secondary)
            else:
                secondary = None
                opposite_secondary = None

        # Add sideways / fallback directions before reversing the primary direction.
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if direction not in candidates and direction != opposite_primary:
                candidates.append(direction)

        # Try the opposite of the main direction last.
        if opposite_primary not in candidates:
            candidates.append(opposite_primary)

        return candidates

    # Choose a movement direction from the relative offset (dx, dy).
    # The ghost prioritises the axis with the larger absolute distance.
    # If the preferred direction is blocked, a secondary direction can be tried.
    def _choose_direction_from_delta(self, dx, dy):
        candidates = self._candidate_directions_from_delta(dx, dy)

        for direction in candidates:
            if self._direction_is_clear(direction):
                return direction

        return Direction.NONE

    # Move one step towards the target position.
    def _move_towards(self, targetPos):
        dx = targetPos.x - self.position.x
        dy = targetPos.y - self.position.y

        # If already at the target, do not move.
        if dx == 0 and dy == 0:
            return Direction.NONE

        return self._choose_direction_from_delta(dx, dy)

    # Move one step away from the target position
    # by reversing the relative direction vector.
    def _move_away(self, targetPos):
        dx = targetPos.x - self.position.x
        dy = targetPos.y - self.position.y
        return self._choose_direction_from_delta(-dx, -dy)

    # Event: this ghost has been eaten by Pacman.
    def eaten(self):
        self._handle_event(Ghost.GHOST_EATEN)
        print("Oh no, I have been eaten!")

    # Event: Pacman has eaten a power pill.
    def pillEaten(self):
        self._handle_event(Ghost.PILL_EATEN)
        print("Watch out for pacman!")

    # Event: the power pill effect has ended.
    def pillExpired(self):
        self._handle_event(Ghost.PILL_EXPIRED)
        print("Get that pacman!")

    # Event: this ghost has eaten Pacman.
    def pacManEaten(self):
        self._handle_event(Ghost.PACMAN_EATEN)
        print("I got pacman!")



        
        
