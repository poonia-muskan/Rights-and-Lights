from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_stories():
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('SELECT id, title FROM stories')
    stories = c.fetchall()
    conn.close()

    image_map = {
        'Don’t Bully Me 🚫': 'child_right.jpg',
        'Pink Football Shoes 👟': 'football_girl.jpg',
        'Boy at the Tea Stall 🫖': 'tea_stall.jpg',
        'The Empty Bench 🌳': 'bench_girl.jpg',
        'The Torn Notebook 📒': 'bully_notebook.jpg',
        'The Invisible Stage 🎤': 'stage_fear.jpg',
        'The School Gate 🚪': 'school_rights.jpg',
        'No More Secrets 🔒': 'protection_abuse.jpg',
        'Respect My Space ✋': 'my_body.jpg',
        'Born to Shine ✨🌱': 'born_to_shine.jpg',
        'There is No Shame 💙': 'boy_supports_periods.jpg',
        'Speak Up 💭': 'mental_health_support.jpg',
        'School Bell Rings for Me Too 🔔': 'school_bell.jpg',
        'She’s a Kid. Not a Bride 🚨': 'friend_marriage.jpg',
        'Not All Offers Are Safe 💬': 'protection_alert.jpg',
        'The Secret ? Not Anymore 🌸': 'menstrual_health.jpg'
    }
    story_data = []
    for s in stories:
        story_data.append({
            'id': s[0],
            'title': s[1],
            'image': image_map.get(s[1], 'default.jpg')  
        })
    return story_data

@app.route('/')
def index():
    stories = get_stories()
    return render_template('index.html', stories=stories)

@app.route('/story/<int:story_id>/step/<int:step_number>')
def story_step(story_id, step_number):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()

    c.execute(''' 
        SELECT content, option1, option2, next1, next2 
        FROM steps 
        WHERE story_id = ? AND step_number = ?
    ''', (story_id, step_number))
    step = c.fetchone()

    c.execute('SELECT title FROM stories WHERE id = ?', (story_id,))
    title_result = c.fetchone()
    story_title = title_result[0] if title_result else 'Story'

    conn.close()

    if step:
        content, option1, option2, next1, next2 = step
        return render_template(
            'story.html',
            story_id=story_id,
            step_number=step_number,
            content=content,
            option1=option1,
            option2=option2,
            next1=next1,
            next2=next2,
            title=story_title
        )
    else:
        return "Story step not found", 404

if __name__ == '__main__':
    app.run(debug=True)