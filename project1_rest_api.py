# =============================================================================
#  Project 1: REST API Fundamentals - The "Goldfish" Server
#  Framework  : Flask (Python)
#  Paradigm   : Stateless REST API
#  Resource   : /products (example plural noun resource)
# =============================================================================

# ----------------------------- 1. IMPORTS ------------------------------------
from flask import Flask, jsonify, request
# flask         → Core web framework
# jsonify       → Converts Python dicts to JSON responses
# request       → Access incoming HTTP request data (body, headers, method)

# =============================================================================
# =================== APPLICATION INITIALIZATION ==============================
# =============================================================================

# Create the Flask application instance
app = Flask(__name__)

# In-memory data store (a simple list acting as our "database")
# Note: This is a NEW empty list for every server restart (stateless behavior)
products = [
    {"id": 1, "name": "Laptop",  "price": 75000},
    {"id": 2, "name": "Headphones", "price": 2500},
    {"id": 3, "name": "Smartphone", "price": 45000},
]

# Auto-incrementing ID counter
# Note: In a real-world app, the database handles this, not memory
next_id = 4

# =============================================================================
# =========================== ROOT ENDPOINT ===================================
# =============================================================================

@app.route("/", methods=["GET"])
def home():
    """
    Welcome/Health check endpoint.
    Helps developers verify the server is running.
    """
    return jsonify({
        "message": "🌟 Welcome to the Goldfish Server (Project 1)",
        "framework": "Flask",
        "endpoints": {
            "GET_all_products":   "GET    /products",
            "GET_one_product":    "GET    /products/<id>",
            "POST_new_product":   "POST   /products",
            "NotFound_handler":   "ANY    /<unknown>"
        }
    }), 200   # HTTP 200 OK — server is alive

# =============================================================================
# =========================== GET ALL PRODUCTS ================================
# =============================================================================

@app.route("/products", methods=["GET"])
def get_products():
    """
    READ operation: Retrieve the full list of products.
    
    HTTP Method : GET (Safe, Idempotent, No request body)
    Status Code : 200 OK
    Returns     : JSON array of all product objects
    """
    # No body parsing needed for GET requests — pure retrieval
    return jsonify({
        "status":  "success",
        "count":   len(products),
        "data":    products
    }), 200   # HTTP 200 OK — Request succeeded

# =============================================================================
# =========================== GET SINGLE PRODUCT ==============================
# =============================================================================

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    READ operation: Retrieve a single product by its ID.
    
    HTTP Method : GET
    Status Code : 200 OK (found) | 404 Not Found (missing)
    """
    # Search for the product in our in-memory list
    product = next((p for p in products if p["id"] == product_id), None)
    
    if product is None:
        # Product not found → return 404
        return jsonify({
            "status":  "error",
            "message": f"Product with ID {product_id} not found"
        }), 404   # HTTP 404 Not Found
    
    # Product found → return it
    return jsonify({
        "status": "success",
        "data":   product
    }), 200   # HTTP 200 OK

# =============================================================================
# =========================== CREATE NEW PRODUCT ==============================
# =============================================================================

@app.route("/products", methods=["POST"])
def create_product():
    """
    CREATE operation: Add a new product to the collection.
    
    HTTP Method : POST (Non-idempotent, Requires JSON body)
    Status Code : 201 Created (success) | 400 Bad Request (invalid input)
    Body Format : {"name": "Tablet", "price": 30000}
    """
    global next_id   # We modify the outer counter
    
    # ------------------------------------------------------------------
    # Step 1: Parse the incoming JSON body
    # ------------------------------------------------------------------
    try:
        data = request.get_json(force=True, silent=False)
    except Exception:
        return jsonify({
            "status":  "error",
            "message": "Invalid JSON syntax in request body"
        }), 400   # HTTP 400 Bad Request
    
    # ------------------------------------------------------------------
    # Step 2: Validate the payload (Error Validation Boundary)
    # ------------------------------------------------------------------
    if not data:
        return jsonify({
            "status":  "error",
            "message": "Request body cannot be empty"
        }), 400   # HTTP 400 Bad Request
    
    if "name" not in data or "price" not in data:
        return jsonify({
            "status":  "error",
            "message": "Both 'name' and 'price' fields are required"
        }), 400   # HTTP 400 Bad Request
    
    # ------------------------------------------------------------------
    # Step 3: Create the new product object
    # ------------------------------------------------------------------
    new_product = {
        "id":    next_id,
        "name":  data["name"],
        "price": data["price"]
    }
    
    # Add to the collection
    products.append(new_product)
    next_id += 1   # Increment for the next insertion
    
    # ------------------------------------------------------------------
    # Step 4: Return 201 Created with the new resource
    # ------------------------------------------------------------------
    return jsonify({
        "status":  "success",
        "message": "Product created successfully",
        "data":    new_product
    }), 201   # HTTP 201 Created

# =============================================================================
# =========================== ERROR HANDLERS ==================================
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """
    Global 404 handler: Catches any unmapped/unknown routes.
    Returns a clean JSON response instead of HTML error page.
    """
    return jsonify({
        "status":  "error",
        "message": "The requested resource was not found on this server",
        "hint":    "Check the URL path or HTTP method"
    }), 404   # HTTP 404 Not Found

@app.errorhandler(405)
def method_not_allowed_error(error):
    """
    Global 405 handler: Catches wrong HTTP methods on valid routes.
    Example: Sending POST to /products/1 (which only accepts GET)
    """
    return jsonify({
        "status":  "error",
        "message": "HTTP method not allowed for this endpoint"
    }), 405   # HTTP 405 Method Not Allowed

@app.errorhandler(500)
def internal_server_error(error):
    """
    Global 500 handler: Catches unexpected server-side crashes.
    """
    return jsonify({
        "status":  "error",
        "message": "Internal server error occurred"
    }), 500   # HTTP 500 Internal Server Error

# =============================================================================
# =========================== SERVER STARTUP ==================================
# =============================================================================

if __name__ == "__main__":
    # Development server block — runs locally on port 5000
    # debug=True enables auto-reload and detailed error messages
    print("=" * 60)
    print("🚀 Starting the Goldfish Server (Stateless REST API)")
    print("=" * 60)
    print("📡 Base URL : http://127.0.0.1:5000")
    print("📖 Endpoints:")
    print("   GET    /              → Welcome message")
    print("   GET    /products      → Get all products")
    print("   GET    /products/<id> → Get one product")
    print("   POST   /products      → Create new product")
    print("=" * 60)
    app.run(debug=True, host="127.0.0.1", port=5000)
