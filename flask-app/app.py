from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates')

def format_time(minutes):
    """Converts a time in minutes to a string 
    in the format HH:MM:SS

    Args:
        minutes (int): Time in minutes

    Returns:
        str: Time in the format HH:MM:SS
    """
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    seconds = int((minutes * 60) % 60)
    
    if hours > 0:
        return f"{hours}:{remaining_minutes:02d}:{seconds:02d}"
    return f"{remaining_minutes}:{seconds:02d}"

def parse_time(time_str):
    """Parses a time string in 
    the format HH:MM:SS or MM:SS to a float

    Args:
        time_str (str): Time string

    Returns:
        float: Time in minutes. 
    """
    try:
        # Handle decimal format
        return float(time_str)
    except ValueError:
        # Handle MM:SS format
        parts = time_str.split(':')
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes + seconds/60
        return 0

def calculate_race_times(pace_per_km):
    """Calculates the time to complete
    a 5K, 10K, half marathon, and marathon
    at the given pace.

    Args:
        pace_per_km (float): Pace in minutes per kilometer

    Returns:
        dict: Dictionary containing the time to complete a 
            5K, 10K, half marathon, and marathon
    """

    distances = {
        '5K': 5,
        '10K': 10,
        'Half Marathon': 21.0975,
        'Marathon': 42.195
    }
    
    return {distance: format_time(pace_per_km * km) 
            for distance, km in distances.items()}

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    pace = parse_time(data['pace'])
    input_unit = data['unit']
    
    if input_unit == 'mile':
        km_pace = pace * 1.60934
        race_times = calculate_race_times(km_pace)
        return jsonify({
            'converted_pace': format_time(km_pace),
            'race_times': race_times
        })
    else:
        mile_pace = pace / 1.60934
        race_times = calculate_race_times(pace)
        return jsonify({
            'converted_pace': format_time(mile_pace),
            'race_times': race_times
        })

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)