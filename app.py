from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dock_scheduler import DockScheduler
from fulfillment_engine import FulfillmentEngine
from carbon_calculator import CarbonCalculator
from recommendation_engine import EmotionAwareRecommendation

app = Flask(__name__)
CORS(app)

# Initialize components
dock_scheduler = DockScheduler()
fulfillment_engine = FulfillmentEngine()
carbon_calculator = CarbonCalculator()
recommendation_engine = EmotionAwareRecommendation()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dock-scheduler', methods=['POST'])
def api_dock_scheduler():
    data = request.json
    result = dock_scheduler.schedule_truck(data)
    return jsonify(result)

@app.route('/api/fulfillment-engine', methods=['POST'])
def api_fulfillment_engine():
    data = request.json
    result = fulfillment_engine.select_optimal_warehouse(
        data['customer_location'], 
        data.get('order_items', [])
    )
    return jsonify({
        'warehouse': result['warehouse']['location'],
        'estimated_delivery': result['estimated_delivery_time']
    })

@app.route('/api/carbon-calculator', methods=['POST'])
def api_carbon_calculator():
    data = request.json
    emissions = carbon_calculator.calculate_delivery_emissions(data)
    suggestions = carbon_calculator.suggest_eco_friendly_options(data)
    
    return jsonify({
        'carbon_footprint': f"{emissions['emissions_kg_co2']} kg CO2",
        'eco_friendly_options': len(suggestions) > 0,
        'suggestions': suggestions
    })

@app.route('/api/product-recommendation', methods=['POST'])
def api_product_recommendation():
    data = request.json
    user_input = {'type': 'text', 'content': data.get('user_input', '')}
    result = recommendation_engine.recommend_products(
        user_input, 
        data.get('user_data', {})
    )
    
    return jsonify({
        'recommendations': [prod['name'] for prod in result['recommendations']],
        'emotion_detected': result['emotion_detected']
    })

if __name__ == '__main__':
    app.run(debug=True)
