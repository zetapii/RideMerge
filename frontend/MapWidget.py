from gui import sg
import staticmaps
import threading
import time


class MapWidget:

    def __init__(self, name: str, show_controls=True):
        self.name = name
        self.context = staticmaps.Context()
        self.context.set_tile_provider(staticmaps.tile_provider_OSM)
        self.graph = sg.Graph(
            key=name,
            background_color='white',
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            canvas_size=(400, 400),
            pad=(10, 10),
            enable_events=True,
            drag_submits=True,
            change_submits=True,
        )
        self.element = [
            self.graph,
            sg.Column([
                [sg.Button('+', key=f'{name}+ZOOM_IN')],
                [sg.Button('-', key=f'{name}+ZOOM_OUT')],
                [
                    sg.Button('Set Pickup',
                              key=f'{name}+SET_FROM',
                              button_color=('white', 'blue'))
                ],
                [
                    sg.Button('Set Drop',
                              key=f'{name}+SET_TO',
                              button_color=('white', 'lime'))
                ],
            ])
        ] if show_controls else [self.graph]
        self.dragging = False
        self.curr_point = None
        self.prev_point = None
        self.location = [17.4263, 78.4307]  # Hyderabad
        self.location_from = None
        self.location_to = None
        self.zoom = 12

        self.rendering = False
        self.image = None

        # directions
        self.directions = {}

        self.init_markers()

    def init_markers(self):
        # markers
        self.from_marker = staticmaps.Marker(
            staticmaps.create_latlng(*self.location), color=staticmaps.BLUE)
        self.context.add_object(self.from_marker)
        self.to_marker = staticmaps.Marker(
            staticmaps.create_latlng(*self.location), color=staticmaps.GREEN)
        self.context.add_object(self.to_marker)

        # hide markers initially
        self.from_marker._size = 0
        self.to_marker._size = 0

    def setup(self):
        self.set_center(self.location)
        self.set_zoom(self.zoom)
        self.graph.bind("<MouseWheel>", "MouseWheel")
        self.render_thread()
        self.render()

    def draw_crosshair(self):
        # draw a plus sign at the center
        w, h = self.graph.CanvasSize
        dw, dh = 50, 50
        line1 = ((w - dw) // 2, h // 2), ((w + dw) // 2, h // 2)
        line2 = (w // 2, (h - dh) // 2), (w // 2, (h + dh) // 2)
        color = 'black'
        width = 3
        self.graph.draw_line(line1[0], line1[1], color=color, width=width)
        self.graph.draw_line(line2[0], line2[1], color=color, width=width)

    def set_zoom(self, zoom):
        # clip
        zoom = max(0, min(20, zoom))
        self.zoom = zoom
        self.context.set_zoom(self.zoom)

    def set_center(self, location: list):
        self.context.set_center(staticmaps.create_latlng(*location))

    def render_thread(self):
        if self.rendering:
            return
        self.rendering = True
        image = self.context.render_cairo(400, 400)
        self.image = image
        self.rendering = False

    def render(self, deadline=None):
        render_task = threading.Thread(target=self.render_thread)
        render_task.start()

        if deadline == 'soft':
            time.sleep(0.1)
        elif deadline == 'hard':
            render_task.join()

        if self.image is None:
            return

        # save image to temp file
        import tempfile
        temp_filename = tempfile.mkstemp(suffix='.png')[1]
        self.image.write_to_png(temp_filename)
        self.graph.draw_image(temp_filename, location=(0, 400))

        self.draw_crosshair()

        # return self.render_thread()

    def update_marker(self, marker, location):
        marker._latlng = staticmaps.create_latlng(*location)
        marker._size = 10

    def handle_event(self, event, values):
        # print(f'event: {event}')

        if event == "MouseWheel:Down":
            event = self.name + "+ZOOM_OUT"
        elif event == "MouseWheel:Up":
            event = self.name + "+ZOOM_IN"

        if event != self.name and not event.startswith(self.name + "+"):
            return False

        event = event[len(self.name) + 1:]  # remove widget name

        x, y = values[self.name]

        if event == "" and x and y:  # mouse move
            # print(f'x: {x}, y: {y}')
            self.curr_point = (x, y)
            if self.prev_point is None:
                self.prev_point = self.curr_point
            else:
                # move location to the new point
                delta_x = self.curr_point[0] - self.prev_point[0]
                delta_y = self.curr_point[1] - self.prev_point[1]
                # scale delta to zoom level
                canvas_size = 400
                tile_size = 256

                # delta_x = delta_x * 1 / 2**self.zoom
                # delta_y = delta_y * 1 / 2**self.zoom

                import numpy as np
                delta_x = delta_x * np.cos(np.radians(
                    self.location[0])) * 360 / tile_size / 2**self.zoom
                delta_y = delta_y * 360 / tile_size / 2**self.zoom

                self.location[0] -= delta_y
                self.location[1] -= delta_x
                self.prev_point = self.curr_point
                if abs(delta_x) > 0 or abs(delta_y) > 0:
                    self.dragging = True
                self.set_center(self.location)
                self.render()
        elif event == "UP":
            if not self.dragging:
                print(f'clicked at {(x, y)}')
            else:
                print(f'dragged to {(x, y)}')
                self.dragging = False
            self.curr_point = self.prev_point = None
        elif event == "ZOOM_IN":
            self.set_zoom(self.zoom + 1)
            self.render('soft')
        elif event == "ZOOM_OUT":
            self.set_zoom(self.zoom - 1)
            self.render('soft')
        elif event == "SET_FROM":
            self.location_from = self.location.copy()
            print(f'Set from: {self.location_from}')
            self.update_marker(self.from_marker, self.location_from)
            self.render('hard')
            return 'location_from_set'
        elif event == "SET_TO":
            self.location_to = self.location.copy()
            print(f'Set to: {self.location_to}')
            self.update_marker(self.to_marker, self.location_to)
            self.render('hard')
            return 'location_to_set'
        elif event == "MouseWheel":
            delta = values[self.name]
            if delta > 0:
                self.set_zoom(self.zoom + 1)
            else:
                self.set_zoom(self.zoom - 1)
            self.render('soft')

        return True

    def get_address(self, location):
        if location is None:
            return "Unknown location"
        # get the address from the location
        import requests
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={location[0]}&lon={location[1]}"
        )
        data = response.json()
        # print(data)
        address = data['display_name']
        return address

    def get_directions(self):
        if self.location_from is None or self.location_to is None:
            return "Please set pickup and drop locations"

        # get directions from the backend
        import requests
        headers = {
            'Accept':
            'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        response = requests.get(
            f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248b5ad15cee8604d4980a4d6b6a5880760&start={self.location_from[1]},{self.location_from[0]}&end={self.location_to[1]},{self.location_to[0]}",
            headers=headers)
        data = response.json()
        # print(data)
        return data

    def clear_directions(self):
        self.context._objects = [
            obj for obj in self.context.objects
            if obj not in self.directions.values()
        ]
        self.directions = {}
        self.render('hard')

    def remove_direction(self, key):
        if key in self.directions:
            if self.directions[key] in self.context._objects:
                self.context._objects.remove(self.directions[key])
                del self.directions[key]
                self.render('hard')

    def update_direction(self, source, dest, data):
        key = f'{source}->{dest}'
        if key in self.directions:
            if self.directions[key] in self.context._objects:
                self.context._objects.remove(self.directions[key])
        self.draw_directions(data, key)
        self.render('hard')

    def draw_directions(self, data, key):
        if 'features' not in data:
            return

        for feature in data['features']:
            geometry = feature['geometry']
            if geometry['type'] == 'LineString':
                coords = geometry['coordinates']
                # print(coords)
                list_of_latlng = [
                    staticmaps.create_latlng(
                        *coord[::-1]  # reverse the coordinates for latlng
                    ) for coord in coords
                ]
                line = staticmaps.Line(list_of_latlng,
                                       color=staticmaps.BLUE,
                                       width=5)
                self.context.add_object(line)
                self.directions[key] = line
                self.render('hard')
