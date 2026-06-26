from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from engine.analyzer import MathAnalyzer
from data.sequences import (
    PerfectNumbers,
    MersenneNumbers,
    PrimeNumbers,
    FibonacciNumbers,
    TriangularNumbers,
    AmicableNumbers,
    HighlyCompositeNumbers,
)

app = FastAPI(title="MathDiscoveryAI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = MathAnalyzer()

class CustomSequence(BaseModel):
    numbers: list[int]

DATA_SETS = {
    "perfect": {
        "name": "Perfect Numbers",
        "description": "Known perfect numbers",
        "numbers": lambda: PerfectNumbers.get_all(),
    },
    "mersenne": {
        "name": "Mersenne Exponents",
        "description": "Known Mersenne prime exponents",
        "numbers": lambda: MersenneNumbers.get_exponents(),
    },
    "primes": {
        "name": "Prime Numbers",
        "description": "First 50 prime numbers",
        "numbers": lambda: PrimeNumbers.get_first(50),
    },
    "fibonacci": {
        "name": "Fibonacci Numbers",
        "description": "First 25 Fibonacci numbers",
        "numbers": lambda: FibonacciNumbers.get_sequence(25),
    },
    "triangular": {
        "name": "Triangular Numbers",
        "description": "First 25 triangular numbers",
        "numbers": lambda: TriangularNumbers.get_sequence(25),
    },
    "amicable": {
        "name": "Amicable Numbers",
        "description": "Known amicable numbers",
        "numbers": lambda: AmicableNumbers.get_numbers(10),
    },
    "highly_composite": {
        "name": "Highly Composite Numbers",
        "description": "Known highly composite numbers",
        "numbers": lambda: HighlyCompositeNumbers.get_all(25),
    },
}

@app.get("/api/sets")
def list_sets():
    return [
        {
            "key": key,
            "name": value["name"],
            "description": value["description"],
        }
        for key, value in DATA_SETS.items()
    ]

@app.get("/api/analyze/{set_key}")
def analyze_set(set_key: str):
    if set_key not in DATA_SETS:
        raise HTTPException(status_code=404, detail="Data set not found")

    numbers = DATA_SETS[set_key]["numbers"]()
    if not numbers:
        raise HTTPException(status_code=400, detail="Number set is empty")

    analysis = analyzer.analyze_number_set(numbers, DATA_SETS[set_key]["name"])
    return {
        "set_key": set_key,
        "set_name": DATA_SETS[set_key]["name"],
        "description": DATA_SETS[set_key]["description"],
        "numbers": analysis["numbers"],
        "patterns": analysis["patterns"],
        "conjectures": analysis["conjectures"],
        "feature_count": analysis["total_features_extracted"],
    }

@app.post("/api/analyze/custom")
def analyze_custom(custom_sequence: CustomSequence):
    if not custom_sequence.numbers:
        raise HTTPException(status_code=400, detail="Numbers list cannot be empty")

    analysis = analyzer.analyze_number_set(custom_sequence.numbers, "Custom Sequence")
    return {
        "set_key": "custom",
        "set_name": "Custom Sequence",
        "numbers": analysis["numbers"],
        "patterns": analysis["patterns"],
        "conjectures": analysis["conjectures"],
        "feature_count": analysis["total_features_extracted"],
    }

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "MathDiscoveryAI backend is running"}

@app.get("/health", response_class=HTMLResponse)
def health_check():
    return """<html><head><title>MathDiscoveryAI Health Check</title></head><body style='font-family:Helvetica,Arial,sans-serif;background:#09101a;color:#e2e8f0;padding:2rem;'><h1>MathDiscoveryAI Backend Health</h1><p>Status: <strong>OK</strong></p><p>The API is available at <code>/api</code>.</p><ul><li><a style='color:#7dd3fc;' href='/api/ping'>/api/ping</a></li><li><a style='color:#7dd3fc;' href='/api/sets'>/api/sets</a></li></ul><p>Use the React frontend to analyze datasets and visualize conjectures.</p></body></html>"""
