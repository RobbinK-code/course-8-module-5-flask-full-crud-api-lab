from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

def find_event(event_id):
    """Helper to locate an event by its ID in the in-memory list."""
    return next((event for event in events if event.id == event_id), None)

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    request_data = request.get_json(silent=True)

    if not request_data:
        return jsonify({"error": "JSON body is required."}), 400

    title = request_data.get("title")
    if not title:
        return jsonify({"error": "Event title is required."}), 400

    next_id = max([event.id for event in events], default=0) + 1
    new_event = Event(next_id, title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    request_data = request.get_json(silent=True)

    if not request_data:
        return jsonify({"error": "JSON body is required."}), 400

    title = request_data.get("title")
    if not title:
        return jsonify({"error": "Event title is required."}), 400

    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found."}), 404

    event.title = title
    return jsonify(event.to_dict()), 200

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found."}), 404

    events.remove(event)
    return jsonify({"message": "Event deleted."}), 204

if __name__ == "__main__":
    app.run(debug=True)
