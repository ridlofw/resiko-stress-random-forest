def get_custom_css():
    """Return custom CSS styling"""
    return """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #6c757d;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .result-box {
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        }
        .result-sehat {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        .result-stres {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
        }
    </style>
    """