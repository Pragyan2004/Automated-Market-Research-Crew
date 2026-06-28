import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Import the Crew AI run script
from market_resrch_crew.crew import MarketResrchCrew

load_dotenv()

app = Flask(__name__)

# Basic routing for multi-page site
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/use-cases')
def use_cases():
    return render_template('use-cases.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/api/research', methods=['POST'])
def run_research():
    data = request.json
    product_idea = data.get('product_idea')
    
    if not product_idea:
        return jsonify({'error': 'Product idea is required'}), 400
        
    try:
        inputs = {'product_idea': product_idea}
        
        # Run the crew
        # CrewAI kickoff returns a CrewOutput object.
        crew_output = MarketResrchCrew().crew().kickoff(inputs=inputs)
        
        # Extract the markdown string
        result_text = str(crew_output)
        
        # Check and print token usage to the terminal
        try:
            usage = crew_output.token_usage
            print("\n" + "="*50)
            print("🚀 CREW TASK COMPLETED")
            print(f"💰 Token Usage Metrics: {usage}")
            print("="*50 + "\n")
        except AttributeError:
            print("\n[Notice] Token usage not available in this version of CrewAI Output.\n")
        
        return jsonify({
            'success': True,
            'result': result_text
        })
    except Exception as e:
        print(f"Error during research: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # HuggingFace spaces often use port 7860
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)
