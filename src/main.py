from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='..')
CORS(app)

# Serve static files (React build)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Simple API endpoints for demo
@app.route('/api/content/library')
def get_content_library():
    return jsonify({
        "success": True,
        "content": [
            {
                "id": 1,
                "title": "Daily Routine",
                "level": "B1",
                "type": "text",
                "description": "Learn about daily routines in German"
            },
            {
                "id": 2,
                "title": "German Cases",
                "level": "B1", 
                "type": "grammar",
                "description": "Understanding German grammatical cases"
            },
            {
                "id": 3,
                "title": "Travel Vocabulary",
                "level": "B1",
                "type": "vocabulary",
                "description": "Essential travel vocabulary in German"
            },
            {
                "id": 4,
                "title": "Goethe B1 Preparation",
                "level": "B1",
                "type": "exam",
                "description": "Prepare for the Goethe B1 exam"
            }
        ]
    })

@app.route('/api/content/<int:content_id>')
def get_content(content_id):
    content_data = {
        1: {
            "id": 1,
            "title": "Daily Routine",
            "level": "B1",
            "type": "text",
            "german_text": "Mein Tagesablauf\n\nJeden Morgen wache ich um sieben Uhr auf. Ich gehe ins Bad und wasche mein Gesicht. Dann frühstücke ich normalerweise Müsli mit Obst. Um acht Uhr verlasse ich das Haus und fahre mit dem Bus zur Arbeit.\n\nMittags mache ich eine kurze Pause und esse ein Sandwich. Nach der Arbeit gehe ich manchmal ins Fitnessstudio oder treffe mich mit Freunden. Abends entspanne ich mich ein bisschen, lese ein Buch oder sehe fern.\n\nUm zehn Uhr bereite ich den nächsten Tag vor und gehe früh ins Bett. Das ist mein Alltag. Mir gefällt meine Routine, weil sie mir hilft, den Tag zu organisieren.",
            "english_summary": "This text describes a typical daily routine in German, covering morning activities, work, lunch break, evening activities, and bedtime preparation. It's written at B1 level with common vocabulary and simple sentence structures.",
            "vocabulary": [
                {"german": "aufwachen", "english": "to wake up", "example": "Jeden Morgen wache ich um sieben Uhr auf."},
                {"german": "das Bad", "english": "bathroom", "example": "Ich gehe ins Bad und wasche mein Gesicht."},
                {"german": "frühstücken", "english": "to have breakfast", "example": "Ich frühstücke normalerweise Müsli mit Obst."},
                {"german": "verlässt", "english": "leaves", "example": "Um acht Uhr verlasse ich das Haus."},
                {"german": "die Arbeit", "english": "work", "example": "Ich fahre mit dem Bus zur Arbeit."}
            ]
        },
        2: {
            "id": 2,
            "title": "German Cases",
            "level": "B1",
            "type": "grammar",
            "german_text": "Im Deutschen gibt es vier Fälle: Nominativ, Akkusativ, Dativ und Genitiv. Diese Fälle zeigen die Funktion eines Nomens im Satz.\n\nDer Nominativ ist der erste Fall. Er antwortet auf die Frage 'Wer oder was?' Das Subjekt steht immer im Nominativ. Beispiel: Der Mann liest ein Buch.\n\nDer Akkusativ ist der vierte Fall. Er antwortet auf die Frage 'Wen oder was?' Das direkte Objekt steht im Akkusativ. Beispiel: Ich sehe den Mann.\n\nDer Dativ ist der dritte Fall. Er antwortet auf die Frage 'Wem?' Das indirekte Objekt steht im Dativ. Beispiel: Ich gebe dem Mann das Buch.\n\nDer Genitiv ist der zweite Fall. Er zeigt Besitz oder Zugehörigkeit. Beispiel: Das Buch des Mannes ist interessant.",
            "english_summary": "This text explains the four German grammatical cases (Nominativ, Akkusativ, Dativ, Genitiv) with their functions and example sentences. It's designed for B1 level learners to understand case usage.",
            "vocabulary": [
                {"german": "der Fall", "english": "case", "example": "Im Deutschen gibt es vier Fälle."},
                {"german": "das Subjekt", "english": "subject", "example": "Das Subjekt steht immer im Nominativ."},
                {"german": "das Objekt", "english": "object", "example": "Das direkte Objekt steht im Akkusativ."},
                {"german": "der Besitz", "english": "possession", "example": "Der Genitiv zeigt Besitz oder Zugehörigkeit."},
                {"german": "die Zugehörigkeit", "english": "belonging", "example": "Der Genitiv zeigt Besitz oder Zugehörigkeit."}
            ]
        }
    }
    
    if content_id in content_data:
        return jsonify({"success": True, "content": content_data[content_id]})
    else:
        return jsonify({"success": False, "error": "Content not found"}), 404

@app.route('/api/content/anki-export/<int:content_id>')
def export_anki(content_id):
    anki_data = {
        1: [
            "aufwachen\tto wake up\n\nExample: Jeden Morgen wache ich um sieben Uhr auf.",
            "das Bad\tbathroom\n\nExample: Ich gehe ins Bad und wasche mein Gesicht.",
            "frühstücken\tto have breakfast\n\nExample: Ich frühstücke normalerweise Müsli mit Obst.",
            "verlässt\tleaves\n\nExample: Um acht Uhr verlasse ich das Haus.",
            "die Arbeit\twork\n\nExample: Ich fahre mit dem Bus zur Arbeit."
        ],
        2: [
            "der Fall\tcase\n\nExample: Im Deutschen gibt es vier Fälle.",
            "das Subjekt\tsubject\n\nExample: Das Subjekt steht immer im Nominativ.",
            "das Objekt\tobject\n\nExample: Das direkte Objekt steht im Akkusativ.",
            "der Besitz\tpossession\n\nExample: Der Genitiv zeigt Besitz oder Zugehörigkeit.",
            "die Zugehörigkeit\tbelonging\n\nExample: Der Genitiv zeigt Besitz oder Zugehörigkeit."
        ]
    }
    
    if content_id in anki_data:
        return jsonify({
            "success": True,
            "anki_cards": anki_data[content_id],
            "format": "tab_separated",
            "total_cards": len(anki_data[content_id])
        })
    else:
        return jsonify({"success": False, "error": "Content not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

