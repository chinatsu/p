# define a center line in the image, 4 is an arbitrary number
#
# alternatively, two thresholds should be defined, where
# one marks off the top region and the other marks off a bottom region
# potentially making anything between not count as top or bottom
Y_THRESHOLD = 4

# the valid states of a person object are these 4.
STATES = ["entering", "exiting", "entered", "exited"]


class Person:
    def __init__(self, coordinate):
        self.state = self._determine_state(coordinate)
        self.coords = [coordinate]
        self.value = 0

    def _determine_state(self, coordinate):
        """
        _determine_state() is a method meant only to be used
        during creation of a new object. It ensures that,
        based on the first registered coordinate,
        the object is either entering or exiting.
        """
        if coordinate[1] >= Y_THRESHOLD:
            return STATES[1]
        else:
            return STATES[0]

    def _update_state(self):
        """
        _update_state() is a method meant to only be used from
        within update(). It is only called when a person object
        is no longer visible in the frame, so there is no valid
        coordinate to be reported.
        In this method a ruleset determines whether a
        person has entered or exited the area based on
        where the person was last seen in the frame.
        """
        seen = self.last_seen()

        # if entering and last seen near the top,
        # has a value of +1 to the person counter.
        if self.state == STATES[0] and seen[1] >= Y_THRESHOLD:
            self.state = STATES[2]
            self.value = 1

        # if entering and last seen near the bottom,
        # has no value to the person counter
        elif self.state == STATES[0] and seen[1] < Y_THRESHOLD:
            self.state = STATES[3]
            self.value = 0

        # if exiting, and last seen near the top,
        # has no value to the person counter
        elif self.state == STATES[1] and seen[1] >= Y_THRESHOLD:
            self.state = STATES[2]
            self.value = 0

        # if exiting, and last seen near the bottom,
        # has a value of -1 to the person counter
        elif self.state == STATES[1] and seen[1] < Y_THRESHOLD:
            self.state = STATES[3]
            self.value = -1

    def update(self, coordinate=(-1, -1)):
        """
        update() is a method which adds a new coordinate tuple to the
        coordinate history of the object. coordinate has a default
        value of (0, 0), which should mean that the object was not seen
        in the picture, and _update_state() will act based on
        the previously registered state. (0, 0) will be
        registered as a coordinate in the history, for checking by
        external classes to be certain whether the object is to have
        its value taken, and then be discarded.
        """
        if coordinate == (-1, -1):
            self._update_state()
        self.coords.append(coordinate)

    def last_seen(self):
        """
        last_seen() is a simple method which returns the last element
        of self.coords.
        """
        return self.coords[-1]


if __name__ == "__main__":
    p = Person((3, 4))  # person with initial coordinates registered
    print(
        "Initial:\nstate: {}, value: {}, last coordinate: {}\n".format(
            p.state, p.value, p.last_seen()
        )
    )

    p.update((3, 1))  # an update call for a person which is still in view
    print(
        "After move:\nstate: {}, value: {}, last coordinate: {}\n".format(
            p.state, p.value, p.last_seen()
        )
    )  # the state has not been updated here yet

    p.update()  # the person is not seen, so we call update on it without coordinates
    print(
        "After disappearing\nstate: {}, value: {}, last coordinate: {}\n".format(
            p.state, p.value, p.last_seen()
        )
    )  # the state has updated now
