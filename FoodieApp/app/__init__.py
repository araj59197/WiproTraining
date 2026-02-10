"""
Flask Application Initialization
"""

from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from app.routes.restaurant_routes import restaurant_bp
    from app.routes.dish_routes import dish_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.user_routes import user_bp
    from app.routes.order_routes import order_bp
    
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(dish_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    # Reset endpoint for testing
    @app.route('/reset', methods=['POST'])
    def reset_data_endpoint():
        from app.models.data_store import reset_data
        reset_data()
        return jsonify({"message": "Data reset successfully"}), 200
    
    return app
