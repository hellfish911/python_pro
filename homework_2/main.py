"""Flask app with generate password view and get average parameters."""

import string
import random
import pandas as pd

from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/generate_password")
def generate_password():
    """
    Generate a random password meeting the following requirements:
    1. At least one lowercase ASCII letter
    2. At least one uppercase ASCII letter
    3. At least one digit
    4. At least one special symbol
    5. Random length between 10 and 20 characters (inclusive)

    Returns:
        str: A randomly generated password
    """
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Generate random password length
    length = random.randint(10, 20)

    # Ensure at least one character from each set
    password_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill remaining characters with random choices from all sets
    all_chars = lowercase + uppercase + digits + symbols
    password_chars += [random.choice(all_chars) for _ in range(length - 4)]

    # Shuffle to avoid predictable patterns
    random.shuffle(password_chars)

    return ''.join(password_chars)


@app.route("/get_average_parameters")
def get_average_parameters():
    """
    Calculate averages from hw.csv with robust column name handling.
    Handle potential leading/trailing spaces in column names.
    """
    try:
        df = pd.read_csv('hw.csv')

        # Clean column names by stripping whitespace
        df.columns = df.columns.str.strip()

        return jsonify({
            'average_weight': float(df['Weight(Pounds)'].mean()),
            'average_height': float(df['Height(Inches)'].mean())
        })

    except FileNotFoundError:
        return jsonify({'error': 'File hw.csv not found'}), 404
    except KeyError as e:
        return jsonify({
            'error': f'Missing required column: {str(e)}',
            'detected_columns': list(df.columns),  # Show actual columns found
            'expected_columns': ['Weight(Pounds)', 'Height(Inches)']
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(
        'localhost', debug=False
    )
