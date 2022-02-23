from json import JSONDecoder, JSONDecodeError
import level
def create_level(level_data):
    rooms = level_data.get("rooms")
    hallways = level_data.get("hallways")
    objects = level_data.get("objects")

    key_pos = None
    exit_pos = None
    for obj in objects:
        t = obj["type"]
        p = obj["position"]

        if t == "exit":
            exit_pos = p
        elif t == "key":
            key_pos = p
    

    l = {"rooms" : [], "hallways" : []}
    for room_data in rooms:
        origin = room_data.get("origin")
        bounds = room_data.get("bounds")
        layout = room_data.get("layout")

        room = {}
        room["position"] = (origin[1], origin[0])
        room["size"] = (bounds["columns"], bounds["rows"])
        room["walls"] = [(col, row) for row in range(bounds["rows"]) for col in range(bounds["columns"]) if layout[row][col] == 0]
        room["doors"] = [(col, row) for row in range(bounds["rows"]) for col in range(bounds["columns"]) if layout[row][col] == 2]
        room["objects"] = {}

        if key_pos:
            if origin[0] <= key_pos[0] < origin[0] + bounds["rows"] and origin[1] <= key_pos[1] < origin[1] + bounds["columns"]:
                room["objects"]["key"] = (key_pos[1] - origin[1], key_pos[0] - origin[0])
        if exit_pos:
            if origin[0] <= exit_pos[0] < origin[0] + bounds["rows"] and origin[1] <= exit_pos[1] < origin[1] + bounds["columns"]:
                room["objects"]["exit"] = (exit_pos[1] - origin[1], exit_pos[0] - origin[0])

        l["rooms"].append(room)

    for hallway_data in hallways:
        from_ = hallway_data.get("from")
        to = hallway_data.get("to")
        waypoints = hallway_data.get("waypoints")

        hallway = {}
        hallway["posFrom"] = (from_[1], from_[0])
        hallway["posTo"] = (to[1], to[0])
        hallway["waypoints"] = [(wp[1], wp[0]) for wp in waypoints]

        l["hallways"].append(hallway)

    return level.Level(l)


# method that takes a string as input
# and return a list of JSON string that is correctly formatted
# for example '12 [2, "foo", 4]' would return [12, [2, "foo", 4]]
def decode_json(jsonstring):
    decoder = JSONDecoder()
    pos = 0
    json_list = []
    while True:
        try:
            while pos < len(jsonstring) and jsonstring[pos].isspace():
                pos += 1

            obj, pos = decoder.raw_decode(jsonstring, pos)
            json_list.append(obj)
        except JSONDecodeError:
            break
    return json_list