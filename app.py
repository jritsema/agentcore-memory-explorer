import boto3
from flask import Flask, render_template, request, jsonify
from botocore.exceptions import ClientError, NoCredentialsError
from log import debug, info, warn, error
import logging
from datetime import datetime
import json
from config import Config
from dateutil import parser as date_parser

app = Flask(__name__)
app.config.from_object(Config)


def get_datetime_sort_key(item, field_name):
    """Helper function to extract datetime for sorting, handling various formats"""
    dt_value = item.get(field_name)
    if dt_value is None:
        return datetime.min
    if isinstance(dt_value, str):
        try:
            return date_parser.parse(dt_value)
        except:
            return datetime.min
    if isinstance(dt_value, datetime):
        return dt_value
    return datetime.min

# Add custom template filters


@app.template_filter('format_datetime')
def format_datetime(dt):
    """Format datetime for display"""
    if dt is None:
        return "N/A"
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    if isinstance(dt, str):
        try:
            parsed_dt = date_parser.parse(dt)
            return parsed_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except:
            return dt
    return str(dt)


@app.template_filter('format_json')
def format_json(data):
    """Format JSON data for display"""
    try:
        return json.dumps(data, indent=2, default=str)
    except:
        return str(data)


# Initialize AWS clients
try:
    session_kwargs = {'region_name': app.config['AWS_REGION']}
    if app.config['AWS_PROFILE']:
        session_kwargs['profile_name'] = app.config['AWS_PROFILE']

    session = boto3.Session(**session_kwargs)
    control_client = session.client('bedrock-agentcore-control')
    data_client = session.client('bedrock-agentcore')
    info({"message": "AWS clients initialized successfully",
         "region": app.config['AWS_REGION']})
except NoCredentialsError:
    warn({"message": "AWS credentials not found. Please configure your credentials."})
    control_client = None
    data_client = None
except Exception as e:
    error({"message": "Failed to initialize AWS clients", "error": str(e)})
    control_client = None
    data_client = None


@app.route('/')
def index():
    """Main dashboard showing memory overview"""
    return render_template('index.html')


@app.route('/memories')
def list_memories():
    """Get list of all memories"""
    if not control_client:
        return render_template('error.html', message="AWS client not initialized")

    try:
        response = control_client.list_memories(maxResults=50)
        memories = response.get('memories', [])

        # Sort memories by createdAt in reverse chronological order (newest first)
        memories.sort(key=lambda x: get_datetime_sort_key(
            x, 'createdAt'), reverse=True)

        info({"message": "Retrieved memories", "count": len(memories)})
        return render_template('memories.html', memories=memories)
    except ClientError as e:
        error({"message": "Failed to list memories", "error": str(e)})
        return render_template('error.html', message=f"Error: {e}")


@app.route('/memory/<memory_id>/actors')
def list_actors(memory_id):
    """Get list of actors for a specific memory"""
    if not data_client:
        return render_template('error.html', message="AWS client not initialized")

    try:
        response = data_client.list_actors(memoryId=memory_id, maxResults=50)
        actors = response.get('actorSummaries', [])
        info({"message": "Retrieved actors",
             "memory_id": memory_id, "count": len(actors)})
        return render_template('actors.html', actors=actors, memory_id=memory_id)
    except ClientError as e:
        error({"message": "Failed to list actors",
              "memory_id": memory_id, "error": str(e)})
        return render_template('error.html', message=f"Error: {e}")


@app.route('/memory/<memory_id>/actor/<actor_id>/sessions')
def list_sessions(memory_id, actor_id):
    """Get list of sessions for a specific actor"""
    if not data_client:
        return render_template('error.html', message="AWS client not initialized")

    try:
        response = data_client.list_sessions(
            memoryId=memory_id,
            actorId=actor_id,
            maxResults=50
        )
        sessions = response.get('sessionSummaries', [])

        # Since sessions don't have createdAt, get the earliest event timestamp for each session
        for session in sessions:
            try:
                events_response = data_client.list_events(
                    memoryId=memory_id,
                    actorId=actor_id,
                    sessionId=session['sessionId'],
                    includePayloads=False,  # Don't need payloads, just timestamps
                    maxResults=100  # Get more events to find the earliest
                )
                events = events_response.get('events', [])
                if events:
                    # Find the earliest event timestamp
                    earliest_timestamp = min(
                        event.get('eventTimestamp', datetime.max)
                        for event in events
                        if event.get('eventTimestamp')
                    )
                    session['createdAt'] = earliest_timestamp
                else:
                    session['createdAt'] = None
            except Exception as e:
                # If we can't get events, set createdAt to None
                session['createdAt'] = None
                debug({"message": "Failed to get events for session",
                      "sessionId": session['sessionId'], "error": str(e)})

        # Sort sessions by createdAt in reverse chronological order (newest first)
        sessions.sort(key=lambda x: get_datetime_sort_key(
            x, 'createdAt'), reverse=True)

        info({"message": "Retrieved sessions", "memory_id": memory_id,
             "actor_id": actor_id, "count": len(sessions)})
        return render_template('sessions.html', sessions=sessions, memory_id=memory_id, actor_id=actor_id)
    except ClientError as e:
        error({"message": "Failed to list sessions",
              "memory_id": memory_id, "actor_id": actor_id, "error": str(e)})
        return render_template('error.html', message=f"Error: {e}")


@app.route('/memory/<memory_id>/actor/<actor_id>/session/<session_id>/events')
def list_events(memory_id, actor_id, session_id):
    """Get list of events for a specific session"""
    if not data_client:
        return render_template('error.html', message="AWS client not initialized")

    try:
        response = data_client.list_events(
            memoryId=memory_id,
            actorId=actor_id,
            sessionId=session_id,
            includePayloads=True,
            maxResults=100
        )
        events = response.get('events', [])

        # Sort events by eventTimestamp in reverse chronological order (newest first)
        events.sort(key=lambda x: get_datetime_sort_key(
            x, 'eventTimestamp'), reverse=True)

        info({"message": "Retrieved events", "memory_id": memory_id,
             "actor_id": actor_id, "session_id": session_id, "count": len(events)})
        return render_template('events.html', events=events, memory_id=memory_id, actor_id=actor_id, session_id=session_id)
    except ClientError as e:
        error({"message": "Failed to list events", "memory_id": memory_id,
              "actor_id": actor_id, "session_id": session_id, "error": str(e)})
        return render_template('error.html', message=f"Error: {e}")


@app.route('/api/memory/<memory_id>/details')
def get_memory_details(memory_id):
    """Get detailed information about a specific memory"""
    if not control_client:
        return jsonify({"error": "AWS client not initialized"}), 500

    try:
        response = control_client.get_memory(memoryId=memory_id)
        return jsonify(response)
    except ClientError as e:
        error({"message": "Failed to get memory details",
              "memory_id": memory_id, "error": str(e)})
        return jsonify({"error": str(e)}), 400


@app.route('/api/memory/<memory_id>/actor/<actor_id>/session/<session_id>/event/<event_id>')
def get_event_details(memory_id, actor_id, session_id, event_id):
    """Get detailed information about a specific event"""
    if not data_client:
        return jsonify({"error": "AWS client not initialized"}), 500

    try:
        response = data_client.get_event(
            memoryId=memory_id,
            actorId=actor_id,
            sessionId=session_id,
            eventId=event_id
        )
        return jsonify(response)
    except ClientError as e:
        error({"message": "Failed to get event details",
              "event_id": event_id, "error": str(e)})
        return jsonify({"error": str(e)}), 400


@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "control_client": control_client is not None,
        "data_client": data_client is not None,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(status)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Internal server error"), 500


if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
