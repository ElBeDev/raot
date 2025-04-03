<?php
// Simple PHP site that will later act as a gateway to your Django app
?>
<!DOCTYPE html>
<html>
<head>
    <title>RAOT Supplements</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e12e20;
            padding-bottom: 20px;
        }
        .header h1 {
            color: #e12e20;
            margin-bottom: 10px;
        }
        .products {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin: 30px 0;
        }
        .product {
            width: 30%;
            margin-bottom: 25px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            text-align: center;
        }
        .product img {
            max-width: 100%;
            height: auto;
        }
        .product h3 {
            margin: 10px 0;
        }
        .price {
            color: #e12e20;
            font-weight: bold;
            font-size: 1.2em;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>RAOT Supplements</h1>
        <p>Premium Health & Fitness Supplements</p>
    </div>
    
    <div class="content">
        <h2>Our Featured Products</h2>
        
        <div class="products">
            <div class="product">
                <div class="product-img">📦</div>
                <h3>Whey Protein</h3>
                <p>Premium whey isolate for muscle growth</p>
                <div class="price">$49.99</div>
            </div>
            
            <div class="product">
                <div class="product-img">📦</div>
                <h3>Pre-Workout</h3>
                <p>Energy boost for intense workouts</p>
                <div class="price">$39.99</div>
            </div>
            
            <div class="product">
                <div class="product-img">📦</div>
                <h3>BCAA Complex</h3>
                <p>Essential amino acids for recovery</p>
                <div class="price">$34.99</div>
            </div>
        </div>
        
        <p>This is a placeholder site while we complete our Django application deployment.</p>
        <p>Server status: <?php echo $_SERVER['SERVER_SOFTWARE']; ?></p>
        <p>PHP version: <?php echo phpversion(); ?></p>
    </div>
    
    <div class="footer">
        <p>&copy; 2025 RAOT Supplements. All rights reserved.</p>
    </div>
</body>
</html>